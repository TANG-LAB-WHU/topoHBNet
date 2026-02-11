#!/usr/bin/env python
"""
Analyze reactive species (H₂O, H*, *OH, H₂O₂, O₂, etc.) from CP2K AIMD
trajectory files (XYZ format).

Core algorithm:
    1. Read multi-frame XYZ trajectory (CP2K -pos-1.xyz)
    2. For each frame, compute all pairwise distances (PBC-aware)
    3. Apply distance thresholds to determine bonds (O-H, O-O, H-H)
    4. Find connected components → molecular fragments
    5. Classify each fragment by atom composition
    6. Record species populations over time

Usage:
    python cp2k_species_analysis.py                        # uses trajectory.xyz + trajectory.cell
    python cp2k_species_analysis.py --cell 22.0 19.08 46.35
    python cp2k_species_analysis.py --xyz system-pos-1.xyz --cell 10 10 10 \\
           --roh 1.3 --stride 10 --output-dir results/ --plot
"""

import argparse
import sys
from pathlib import Path
from collections import defaultdict
from typing import Optional
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.lib.distances import distance_array
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


# ─── Species classification ─────────────────────────────────────────────────
SPECIES_RULES = {
    # key: (n_H, n_O) → species name
    # Additional rules may use bond topology
    (0, 1): "O*",
    (1, 0): "H*",
    (2, 0): "H2",
    (0, 2): "O2",
    (1, 1): "*OH",
    (2, 1): "H2O",
    (3, 1): "H3O+",
    (1, 2): "HO2*",
    (2, 2): "H2O2",
    (3, 2): "H3O2-",    # Zundel-like
    (4, 2): "(H2O)2",   # water dimer
}

# Species that always appear in the output CSV, even if count is 0.
# Auto-generated from SPECIES_RULES to stay in sync.
TRACKED_SPECIES = list(SPECIES_RULES.values())


def classify_fragment(elements: list[str]) -> str:
    """Classify a molecular fragment by its atomic composition.

    Only considers H and O atoms. Fragments containing other elements
    (Si, C, etc.) are classified separately.

    Parameters
    ----------
    elements : list of str
        Element symbols for each atom in the fragment.

    Returns
    -------
    str
        Species name.
    """
    n_H = elements.count("H")
    n_O = elements.count("O")
    n_other = len(elements) - n_H - n_O

    if n_other > 0:
        # Fragment contains non-H/O atoms (e.g., Si, C) — surface/substrate
        return f"other({len(elements)})"

    species = SPECIES_RULES.get((n_H, n_O))
    if species is not None:
        return species

    # Fallback: larger clusters
    return f"H{n_H}O{n_O}"


# ─── Core analysis ───────────────────────────────────────────────────────────

# Default bond distance thresholds (Å) for substrate bond types
# These ensure substrate atoms (Si, C) are properly grouped into fragments
# so they get excluded from H/O species counting.
SUBSTRATE_BOND_THRESHOLDS = {
    ("C", "H"): 1.2,    # C-H covalent bond
    ("Si", "O"): 2.0,   # Si-O covalent bond
    ("Si", "C"): 2.0,   # Si-C covalent bond
    ("Si", "H"): 1.7,   # Si-H covalent bond (rare)
    ("C", "C"): 1.7,    # C-C covalent bond
    ("C", "O"): 1.6,    # C-O covalent bond
}


def _detect_pair_bonds(
    idx_a: np.ndarray,
    idx_b: np.ndarray,
    positions: np.ndarray,
    box: Optional[np.ndarray],
    threshold: float,
    same_group: bool = False,
) -> list[tuple[int, int]]:
    """Detect bonds between two sets of atoms.

    Parameters
    ----------
    idx_a, idx_b : ndarray of int
        Global atom indices for the two groups.
    positions : ndarray, shape (N, 3)
    box : ndarray or None
    threshold : float
        Bond distance threshold in Å.
    same_group : bool
        If True, idx_a == idx_b; only report i < j pairs.

    Returns
    -------
    bonds : list of (int, int)
    """
    if len(idx_a) == 0 or len(idx_b) == 0:
        return []

    dists = distance_array(positions[idx_a], positions[idx_b], box=box)

    if same_group:
        pairs = np.argwhere((dists < threshold) & (dists > 0.01))
        return [(idx_a[i], idx_b[j]) for i, j in pairs if i < j]
    else:
        pairs = np.argwhere(dists < threshold)
        return [(idx_a[i], idx_b[j]) for i, j in pairs]


def detect_bonds_frame(
    positions: np.ndarray,
    elements: np.ndarray,
    box: Optional[np.ndarray],
    r_oh: float = 1.2,
    r_oo: float = 1.6,
    r_hh: float = 0.9,
) -> np.ndarray:
    """Detect bonds based on distance thresholds for a single frame.

    Detects both reactive bonds (O-H, O-O, H-H) and substrate bonds
    (C-H, Si-O, Si-C, etc.) so that substrate atoms are properly
    grouped into fragments and excluded from species classification.

    Parameters
    ----------
    positions : ndarray, shape (N, 3)
        Atom positions in Angstrom.
    elements : ndarray of str, shape (N,)
        Element symbols.
    box : ndarray or None
        Box dimensions [Lx, Ly, Lz, 90, 90, 90] for PBC, or None.
    r_oh : float
        O-H bond distance threshold (Å).
    r_oo : float
        O-O bond distance threshold (Å).
    r_hh : float
        H-H bond distance threshold (Å).

    Returns
    -------
    bonds : ndarray, shape (M, 2)
        Array of bonded atom index pairs.
    """
    # Build index lookup for all element types present
    unique_elems = set(elements)
    elem_indices = {e: np.where(elements == e)[0] for e in unique_elems}

    bonds = []

    # --- Reactive bonds (user-tunable thresholds) ---
    # O-H bonds
    bonds.extend(_detect_pair_bonds(
        elem_indices.get("O", np.array([], dtype=int)),
        elem_indices.get("H", np.array([], dtype=int)),
        positions, box, r_oh,
    ))

    # O-O bonds (for H2O2, O2, etc.)
    bonds.extend(_detect_pair_bonds(
        elem_indices.get("O", np.array([], dtype=int)),
        elem_indices.get("O", np.array([], dtype=int)),
        positions, box, r_oo, same_group=True,
    ))

    # H-H bonds (for H2)
    bonds.extend(_detect_pair_bonds(
        elem_indices.get("H", np.array([], dtype=int)),
        elem_indices.get("H", np.array([], dtype=int)),
        positions, box, r_hh, same_group=True,
    ))

    # --- Substrate bonds (fixed thresholds for correct fragment grouping) ---
    for (elem_a, elem_b), threshold in SUBSTRATE_BOND_THRESHOLDS.items():
        if elem_a not in unique_elems or elem_b not in unique_elems:
            continue
        same = (elem_a == elem_b)
        bonds.extend(_detect_pair_bonds(
            elem_indices[elem_a], elem_indices[elem_b],
            positions, box, threshold, same_group=same,
        ))

    if bonds:
        return np.array(bonds, dtype=int)
    else:
        return np.empty((0, 2), dtype=int)


def find_fragments(n_atoms: int, bonds: np.ndarray) -> list[list[int]]:
    """Find connected molecular fragments using graph analysis.

    Parameters
    ----------
    n_atoms : int
        Total number of atoms.
    bonds : ndarray, shape (M, 2)
        Bonded atom index pairs.

    Returns
    -------
    fragments : list of list of int
        Each sublist contains atom indices belonging to one fragment.
    """
    if len(bonds) == 0:
        # Every atom is isolated
        return [[i] for i in range(n_atoms)]

    # Build sparse adjacency matrix
    row = np.concatenate([bonds[:, 0], bonds[:, 1]])
    col = np.concatenate([bonds[:, 1], bonds[:, 0]])
    data = np.ones(len(row), dtype=int)
    adj = csr_matrix((data, (row, col)), shape=(n_atoms, n_atoms))

    n_components, labels = connected_components(adj, directed=False)

    fragments = defaultdict(list)
    for atom_idx, comp_id in enumerate(labels):
        fragments[comp_id].append(atom_idx)

    return list(fragments.values())


def analyze_frame(
    positions: np.ndarray,
    elements: np.ndarray,
    box: Optional[np.ndarray],
    r_oh: float,
    r_oo: float,
    r_hh: float,
    ho_only: bool = True,
) -> dict[str, int]:
    """Analyze species composition for a single trajectory frame.

    Parameters
    ----------
    positions : ndarray, shape (N, 3)
        Atom positions.
    elements : ndarray of str, shape (N,)
        Element symbols.
    box : ndarray or None
        PBC box.
    r_oh, r_oo, r_hh : float
        Bond distance thresholds.
    ho_only : bool
        If True, only analyze fragments composed purely of H and O atoms.

    Returns
    -------
    species_count : dict
        Mapping of species name → count.
    """
    bonds = detect_bonds_frame(positions, elements, box, r_oh, r_oo, r_hh)
    frags = find_fragments(len(positions), bonds)

    species_count = defaultdict(int)
    for frag_indices in frags:
        frag_elements = [elements[i] for i in frag_indices]

        # Filter: skip non-H/O fragments if ho_only
        if ho_only:
            has_other = any(e not in ("H", "O") for e in frag_elements)
            if has_other:
                continue

        species = classify_fragment(frag_elements)
        species_count[species] += 1

    return dict(species_count)


def parse_cp2k_xyz_time(comment_line: str) -> tuple[Optional[int], Optional[float]]:
    """Parse CP2K XYZ comment line for step index and time.

    Expected format: " i =        0, time =        0.000, E = ..."

    Parameters
    ----------
    comment_line : str

    Returns
    -------
    step : int or None
    time_fs : float or None
    """
    step = None
    time_fs = None
    try:
        parts = comment_line.split(",")
        for part in parts:
            part = part.strip()
            if part.startswith("i =") or part.startswith("i="):
                step = int(part.split("=")[1].strip())
            elif part.startswith("time =") or part.startswith("time="):
                time_fs = float(part.split("=")[1].strip())
    except (ValueError, IndexError):
        pass
    return step, time_fs


def parse_cp2k_cell_file(cell_path: str, verbose: bool = True) -> list[float]:
    """Read cell dimensions from a CP2K trajectory.cell file.

    Parses the first data line to extract diagonal cell vectors (Ax, By, Cz)
    for an orthorhombic box.

    Expected header:
      #   Step   Time [fs]  Ax  Ay  Az  Bx  By  Bz  Cx  Cy  Cz  Volume

    Parameters
    ----------
    cell_path : str
        Path to CP2K .cell file.
    verbose : bool
        Print parsed cell info.

    Returns
    -------
    cell : list of float
        [Lx, Ly, Lz] in Angstrom.

    Raises
    ------
    FileNotFoundError
        If the cell file does not exist.
    ValueError
        If the file cannot be parsed.
    """
    with open(cell_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # First data line: Step Time Ax Ay Az Bx By Bz Cx Cy Cz Volume
            cols = line.split()
            if len(cols) < 12:
                raise ValueError(
                    f"Expected >=12 columns in cell file, got {len(cols)}: {line}"
                )
            # Ax=cols[2], By=cols[6], Cz=cols[10]
            Ax = float(cols[2])
            By = float(cols[6])
            Cz = float(cols[10])

            if verbose:
                print(f"  Cell from {cell_path}: Ax={Ax:.4f}, By={By:.4f}, Cz={Cz:.4f} Å")

            return [Ax, By, Cz]

    raise ValueError(f"No data lines found in cell file: {cell_path}")


def run_analysis(
    xyz_path: str,
    cell: Optional[list[float]] = None,
    r_oh: float = 1.2,
    r_oo: float = 1.6,
    r_hh: float = 0.9,
    stride: int = 1,
    timestep: Optional[float] = None,
    ho_only: bool = True,
    verbose: bool = True,
) -> pd.DataFrame:
    """Run species analysis on a CP2K XYZ trajectory.

    Parameters
    ----------
    xyz_path : str
        Path to XYZ trajectory file.
    cell : list of float, optional
        Box dimensions [Lx, Ly, Lz]. If None, no PBC applied.
    r_oh : float
        O-H bond distance threshold (Å).
    r_oo : float
        O-O bond distance threshold (Å).
    r_hh : float
        H-H bond distance threshold (Å).
    stride : int
        Analyze every N-th frame.
    timestep : float, optional
        Override timestep (fs) between frames. If None, parse from XYZ.
    ho_only : bool
        Only analyze H/O fragments.
    verbose : bool
        Print progress.

    Returns
    -------
    df : pandas.DataFrame
        Columns: frame, step, time_fs, and one column per species.
    """
    # Set up PBC box
    box = None
    if cell is not None:
        box = np.array([cell[0], cell[1], cell[2], 90.0, 90.0, 90.0],
                       dtype=np.float32)

    # Load trajectory with MDAnalysis
    if verbose:
        print(f"Loading trajectory: {xyz_path}")

    u = mda.Universe(xyz_path)

    n_frames_total = u.trajectory.n_frames
    if verbose:
        print(f"  Total frames: {n_frames_total}")
        print(f"  Atoms per frame: {u.atoms.n_atoms}")
        print(f"  Elements: {sorted(set(u.atoms.names))}")
        print(f"  Stride: every {stride} frame(s)")
        print()

    # Element array (constant across frames for CP2K)
    elements = np.array(u.atoms.names)

    # Collect results
    records = []
    all_species = set()
    frames_to_analyze = range(0, n_frames_total, stride)
    n_analyze = len(frames_to_analyze)

    for count, frame_idx in enumerate(frames_to_analyze):
        ts = u.trajectory[frame_idx]
        positions = ts.positions.copy()

        # Try to parse step/time from the comment line
        # MDAnalysis stores the raw data; we read it separately
        step_i = frame_idx
        time_fs_i = frame_idx * (timestep or 0.5)  # default 0.5 fs

        # Analyze species
        species_count = analyze_frame(
            positions, elements, box,
            r_oh=r_oh, r_oo=r_oo, r_hh=r_hh,
            ho_only=ho_only,
        )

        record = {
            "frame": frame_idx,
            "step": step_i,
            "time_fs": time_fs_i,
        }
        record.update(species_count)
        records.append(record)
        all_species.update(species_count.keys())

        if verbose and (count + 1) % max(1, n_analyze // 20) == 0:
            pct = 100 * (count + 1) / n_analyze
            print(f"  Progress: {count + 1}/{n_analyze} ({pct:.0f}%)")

    # Build DataFrame
    df = pd.DataFrame(records)

    # Fill missing species columns with 0
    for sp in all_species:
        if sp not in df.columns:
            df[sp] = 0
    # Ensure all tracked species columns are present
    for sp in TRACKED_SPECIES:
        if sp not in df.columns:
            df[sp] = 0
    df = df.fillna(0)

    # Sort columns for consistent output
    meta_cols = ["frame", "step", "time_fs"]
    species_cols = sorted([c for c in df.columns if c not in meta_cols])
    df = df[meta_cols + species_cols]

    # Convert species columns to int
    for col in species_cols:
        df[col] = df[col].astype(int)

    if verbose:
        print(f"\n  Analysis complete — {len(df)} frames analyzed")
        print(f"  Species detected: {species_cols}")
        # Summary statistics
        print(f"\n  Average species counts:")
        for sp in species_cols:
            mean_val = df[sp].mean()
            if mean_val > 0.01:
                print(f"    {sp:10s}: {mean_val:.2f} ± {df[sp].std():.2f}")

    return df


# ─── Plotting ────────────────────────────────────────────────────────────────

def plot_species_evolution(
    df: pd.DataFrame,
    output_path: str,
    title: str = "CP2K AIMD Species Evolution",
):
    """Plot species populations over simulation time.

    Parameters
    ----------
    df : DataFrame
        Output from run_analysis.
    output_path : str
        Path to save figure.
    title : str
        Plot title.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not available. Skipping plots.")
        return

    meta_cols = {"frame", "step", "time_fs"}
    species_cols = [c for c in df.columns if c not in meta_cols]

    # Filter species with nonzero average
    species_to_plot = [
        sp for sp in species_cols if df[sp].mean() > 0.01
    ]

    if not species_to_plot:
        print("  No species detected — nothing to plot.")
        return

    # Separate major (high-count) and minor (low-count) species
    means = {sp: df[sp].mean() for sp in species_to_plot}
    max_mean = max(means.values())
    major = [sp for sp in species_to_plot if means[sp] > max_mean * 0.05]
    minor = [sp for sp in species_to_plot if means[sp] <= max_mean * 0.05]

    n_panels = 1 + (1 if minor else 0)
    fig, axes = plt.subplots(
        n_panels, 1, figsize=(12, 4 * n_panels),
        sharex=True, squeeze=False,
    )

    x = df["time_fs"] / 1000.0  # Convert to ps

    # Color palette
    colors = plt.cm.tab10.colors

    # Major species panel
    ax = axes[0, 0]
    for i, sp in enumerate(sorted(major)):
        ax.plot(x, df[sp], label=sp, color=colors[i % len(colors)],
                linewidth=0.8, alpha=0.85)
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=9, ncol=min(4, len(major)))
    ax.grid(True, alpha=0.3)

    # Minor species panel (reactive intermediates)
    if minor:
        ax2 = axes[1, 0]
        for i, sp in enumerate(sorted(minor)):
            ax2.plot(x, df[sp], label=sp,
                     color=colors[(len(major) + i) % len(colors)],
                     linewidth=1.0, alpha=0.9, marker=".", markersize=2)
        ax2.set_ylabel("Count")
        ax2.set_title("Reactive Intermediates")
        ax2.legend(loc="upper right", fontsize=9, ncol=min(4, len(minor)))
        ax2.grid(True, alpha=0.3)

    axes[-1, 0].set_xlabel("Time (ps)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved: {output_path}")


def plot_species_pie(
    df: pd.DataFrame,
    output_path: str,
    title: str = "Average Species Distribution",
):
    """Plot pie chart of average species distribution.

    Parameters
    ----------
    df : DataFrame
        Output from run_analysis.
    output_path : str
        Path to save figure.
    title : str
        Plot title.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    meta_cols = {"frame", "step", "time_fs"}
    species_cols = [c for c in df.columns if c not in meta_cols]
    means = {sp: df[sp].mean() for sp in species_cols if df[sp].mean() > 0.01}

    if not means:
        return

    labels = list(means.keys())
    values = list(means.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%",
        textprops={"fontsize": 10},
    )
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Pie chart saved: {output_path}")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Analyze reactive species from CP2K AIMD trajectory (XYZ format).\n"
            "Identifies H₂O, H*, *OH, H₂O₂, O₂, H₂, etc. per frame."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s                                        # auto-read trajectory.xyz + trajectory.cell\n"
            "  %(prog)s --cell 22 19.08 46.35                  # manually specify cell\n"
            "  %(prog)s --xyz traj.xyz --cell 10 10 10 --plot  # custom xyz with plotting\n"
            "  %(prog)s --stride 5 --output-dir results/       # every 5th frame\n"
        ),
    )

    parser.add_argument(
        "--xyz", type=str, default="trajectory.xyz",
        help="Path to CP2K XYZ trajectory file (default: trajectory.xyz)",
    )
    parser.add_argument(
        "--cell", nargs=3, type=float, default=None,
        metavar=("Lx", "Ly", "Lz"),
        help="Simulation box dimensions in Å (Lx Ly Lz) for PBC. "
             "Overrides --cell-file if both specified.",
    )
    parser.add_argument(
        "--cell-file", type=str, default="trajectory.cell",
        help="CP2K .cell file to auto-read box dimensions (default: trajectory.cell). "
             "Ignored if --cell is specified.",
    )
    parser.add_argument(
        "--roh", type=float, default=1.2,
        help="O-H bond distance threshold in Å (default: 1.2)",
    )
    parser.add_argument(
        "--roo", type=float, default=1.6,
        help="O-O bond distance threshold in Å (default: 1.6)",
    )
    parser.add_argument(
        "--rhh", type=float, default=0.9,
        help="H-H bond distance threshold in Å (default: 0.9)",
    )
    parser.add_argument(
        "--stride", type=int, default=1,
        help="Analyze every N-th frame (default: 1)",
    )
    parser.add_argument(
        "--timestep", type=float, default=None,
        help="Timestep between frames in fs (default: parse from XYZ or 0.5)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="trajectory_species_results",
        help="Output directory (default: trajectory_species_results/)",
    )
    parser.add_argument(
        "--no-plot", action="store_true",
        help="Skip generating plots",
    )
    parser.add_argument(
        "--include-substrate", action="store_true",
        help="Include non-H/O fragments (Si, C, etc.) in analysis",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress progress output",
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve cell dimensions: --cell (manual) > --cell-file (auto)
    cell = args.cell
    if cell is None and args.cell_file:
        cell_path = Path(args.cell_file)
        if cell_path.exists():
            if not args.quiet:
                print(f"Auto-reading cell from: {cell_path}")
            cell = parse_cp2k_cell_file(str(cell_path), verbose=not args.quiet)
        else:
            if not args.quiet:
                print(f"  Warning: Cell file '{cell_path}' not found. Running without PBC.")

    if not args.quiet:
        print("=" * 60)
        print("CP2K AIMD Reactive Species Analysis")
        print("=" * 60)
        print(f"\n  Trajectory:  {args.xyz}")
        print(f"  PBC box:     {cell if cell else 'None (no PBC)'}")
        print(f"  Thresholds:  O-H < {args.roh} Å, O-O < {args.roo} Å, H-H < {args.rhh} Å")
        print(f"  Stride:      every {args.stride} frame(s)")
        print(f"  Output:      {output_dir}")
        print()

    # Run analysis
    df = run_analysis(
        xyz_path=args.xyz,
        cell=cell,
        r_oh=args.roh,
        r_oo=args.roo,
        r_hh=args.rhh,
        stride=args.stride,
        timestep=args.timestep,
        ho_only=not args.include_substrate,
        verbose=not args.quiet,
    )

    # Save CSV
    csv_path = output_dir / "species_counts.csv"
    df.to_csv(csv_path, index=False)
    if not args.quiet:
        print(f"\n  CSV saved: {csv_path}")

    # Save summary statistics
    meta_cols = {"frame", "step", "time_fs"}
    species_cols = [c for c in df.columns if c not in meta_cols]
    summary = {}
    for sp in species_cols:
        summary[sp] = {
            "mean": float(df[sp].mean()),
            "std": float(df[sp].std()),
            "min": int(df[sp].min()),
            "max": int(df[sp].max()),
        }

    import json
    summary_path = output_dir / "species_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    if not args.quiet:
        print(f"  Summary saved: {summary_path}")

    # Plot
    if not args.no_plot:
        if not args.quiet:
            print("\n  Generating plots...")

        plot_species_evolution(
            df,
            output_path=str(output_dir / "species_evolution.png"),
        )
        plot_species_pie(
            df,
            output_path=str(output_dir / "species_distribution.png"),
        )

    if not args.quiet:
        print(f"\nDone! Results in: {output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
