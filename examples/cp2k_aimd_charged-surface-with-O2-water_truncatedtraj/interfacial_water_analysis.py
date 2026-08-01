#!/usr/bin/env python3


"""
This script implements Steps 63-65 of the Nature Protocols paper (https://doi.org/10.1038/s41596-022-00782-8)
for solid-liquid interfaces. It detects the interface dynamically (via density
crossover / Gibbs dividing surface) or statically (fixed Z coordinate), separates
interfacial and bulk water, and computes orientation and H-bonding profiles.

Usage:
    python interfacial_water_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --mode dynamic
    python interfacial_water_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --mode static --static-z-surface 15.0
"""


import sys
import argparse
from pathlib import Path
import json

# Add parent directory to path for development/execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from hbond_topology.io.trajectory_parser import TrajectoryParser
from hbond_topology.analysis.interfacial import InterfacialAnalyzer, InterfacialVisualizer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interfacial Water Analysis (Protocol Steps 63-65)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Trajectory options
    parser.add_argument(
        "--xyz",
        type=str,
        default="trajectory.xyz",
        help="Path to CP2K XYZ trajectory file.",
    )
    parser.add_argument(
        "--cell-file",
        type=str,
        default="trajectory.cell",
        help="Path to CP2K .cell file.",
    )
    parser.add_argument(
        "--timestep",
        type=float,
        default=0.5,
        help="Simulation timestep in femtoseconds.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=298.0,
        help="Simulation temperature in Kelvin.",
    )
    parser.add_argument(
        "--sample-interval",
        type=int,
        default=1,
        help="Process every N-th frame.",
    )

    # Surface options
    parser.add_argument(
        "--mode",
        choices=["dynamic", "static"],
        default="dynamic",
        help="Surface detection mode. Use 'dynamic' for polymer/soft surfaces (density crossover) and 'static' for metal/rigid surfaces.",
    )
    parser.add_argument(
        "--static-z-surface",
        type=float,
        default=None,
        help="Fixed surface Z coordinate (Å) required when --mode=static.",
    )
    parser.add_argument(
        "--interface-cutoff",
        type=float,
        default=None,
        help="Interfacial layer thickness cutoff (Å). If omitted, automatically detected from the first valley of the water O density profile.",
    )
    parser.add_argument(
        "--z-axis",
        type=int,
        default=2,
        help="Cartesian axis normal to the interface (0=X, 1=Y, 2=Z).",
    )

    # Algorithm options
    parser.add_argument(
        "--n-bins",
        type=int,
        default=200,
        help="Number of bins for density profiles.",
    )
    parser.add_argument(
        "--density-sigma",
        type=float,
        default=0.5,
        help="Gaussian smoothing standard deviation (Å) for density profiles.",
    )
    parser.add_argument(
        "--r-oh-max",
        type=float,
        default=1.2,
        help="Maximum O-H distance (Å) for water identification.",
    )
    parser.add_argument(
        "--r-oo-hbond",
        type=float,
        default=3.5,
        help="Maximum O...O distance (Å) for H-bond definition.",
    )
    parser.add_argument(
        "--angle-ooh-hbond",
        type=float,
        default=35.0,
        help="Maximum O...O-H angle (deg) for H-bond definition.",
    )

    # Output options
    parser.add_argument(
        "--output-dir",
        type=str,
        default="interfacial_analysis_results",
        help="Directory to save figures and JSON data.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI resolution for output plots.",
    )

    parser.add_argument(
        "--cp2k-out",
        nargs="+",
        type=str,
        default=None,
        help="CP2K .out log files (e.g. aimd_nofield-R1.out aimd_nofield-R2.out aimd_nofield-R3.out) for Mulliken spin extraction",
    )
    parser.add_argument(
        "--mulliken-cache",
        type=str,
        default=None,
        help="Path to Mulliken spin cache npz file (default: mulliken_spins_cache.npz in output dir)",
    )
    import equilibration_utils
    parser = equilibration_utils.add_equilibration_args(parser)
    return parser.parse_args()


def natural_sort_key(s: str) -> list:
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

def extract_or_load_mulliken_spins(
    out_files: list[str],
    cache_path: str,
    n_atoms: int = 823,
    verbose: bool = True,
) -> tuple:
    import numpy as np
    from pathlib import Path
    cache_file = Path(cache_path)
    if cache_file.exists():
        if verbose:
            print(f"  [Mulliken] Loading spin/charge cache: {cache_file}")
        data = np.load(cache_file)
        return data["spins"], data["charges"]

    valid_out_files = sorted([f for f in out_files if Path(f).exists()], key=natural_sort_key)
    if not valid_out_files:
        if verbose:
            print("  [Mulliken] No CP2K .out log files found for spin extraction.")
        return np.zeros((0, n_atoms), dtype=np.float32), np.zeros((0, n_atoms), dtype=np.float32)

    if verbose:
        print(f"  [Mulliken] Extracting spin/charge data from {len(valid_out_files)} CP2K .out log(s)...")

    all_spins = []
    all_charges = []
    seen_steps = set()

    for out_idx, out_file in enumerate(valid_out_files):
        if verbose:
            print(f"    Parsing {Path(out_file).name}...")

        with open(out_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        idx = 0
        n_lines = len(lines)
        file_frames = 0
        current_step = None
        first_mulliken_in_file = True

        while idx < n_lines:
            line = lines[idx]
            if "MD| Step number" in line:
                try:
                    current_step = int(line.split()[-1])
                except (ValueError, IndexError):
                    pass
                idx += 1
            elif "Mulliken Population Analysis" in line:
                if out_idx > 0 and first_mulliken_in_file:
                    first_mulliken_in_file = False
                    idx += 1
                    continue

                first_mulliken_in_file = False

                if current_step is not None and current_step in seen_steps:
                    idx += 1
                    continue

                idx += 1
                while idx < n_lines and not lines[idx].strip().startswith("#"):
                    idx += 1
                if idx < n_lines and lines[idx].strip().startswith("#"):
                    idx += 1

                frame_spins = np.zeros(n_atoms, dtype=np.float32)
                frame_charges = np.zeros(n_atoms, dtype=np.float32)
                atom_count = 0

                while idx < n_lines and atom_count < n_atoms:
                    l = lines[idx].strip()
                    if not l or l.startswith("!") or l.startswith("#") or "Integrated" in l:
                        break
                    tokens = l.split()
                    if len(tokens) >= 7 and tokens[0].isdigit():
                        try:
                            atom_idx = int(tokens[0]) - 1
                            net_charge = float(tokens[5])
                            spin_moment = float(tokens[6])
                            if 0 <= atom_idx < n_atoms:
                                frame_spins[atom_idx] = spin_moment
                                frame_charges[atom_idx] = net_charge
                                atom_count += 1
                        except (ValueError, IndexError):
                            pass
                    idx += 1

                if atom_count == n_atoms:
                    all_spins.append(frame_spins)
                    all_charges.append(frame_charges)
                    if current_step is not None:
                        seen_steps.add(current_step)
                    file_frames += 1
            else:
                idx += 1

        if verbose:
            print(f"      Extracted {file_frames} unique frames from {Path(out_file).name}")

    if not all_spins:
        if verbose:
            print("  [Mulliken] Warning: No complete Mulliken blocks found in logs.")
        return np.zeros((0, n_atoms), dtype=np.float32), np.zeros((0, n_atoms), dtype=np.float32)

    spins_arr = np.array(all_spins, dtype=np.float32)
    charges_arr = np.array(all_charges, dtype=np.float32)

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache_file, spins=spins_arr, charges=charges_arr)
    if verbose:
        print(f"  [Mulliken] Extracted total {len(spins_arr)} frames. Saved cache to: {cache_file}")

    return spins_arr, charges_arr

def inverse_langevin(x):
    """Accurate Cohen approximation for the Inverse Langevin function L^-1(x).

    Prevents overflow/divergence at saturation boundaries.
    """
    import numpy as np
    x_clipped = np.clip(x, -0.99, 0.99)
    return x_clipped * (3.0 - x_clipped**2) / (1.0 - x_clipped**2)


def analyze_and_plot_electric_field(
    frames, charges_arr, box_z, n_bins, sigma, output_dir, analyzer, temperature=298.0, dpi=300
):
    """Compute electric field via double methods and calculate effective interfacial dielectric constant:

    1. Poisson Integration (Macro-scale Maxwell field E_Poisson from Mulliken net charges)
    2. Langevin Dipole Inversion (Micro-scale local effective field E_Langevin from H2O dipoles)

    Physics & Dielectric Saturation:
        The ratio eps_eff = E_Poisson / E_Langevin defines the interfacial effective dielectric constant.
        
        Under strong intrinsic fields (~10^9 V/m), interfacial water undergoes severe dielectric saturation,
        reducing eps_eff from bulk value (~80) down to ~2-6, in agreement with literature benchmarks:
        - Fumagalli et al., Science 360, 259-262 (2018), DOI: 10.1126/science.aat4491 [eps_perp ~ 2.1]
        - Bonthuis et al., Phys. Rev. Lett. 107, 166104 (2011), DOI: 10.1103/PhysRevLett.107.166104 [eps_interfacial ~ 2-6]
        - Kornyshev & Sutmann, Phys. Rev. Lett. 79, 3435-3438 (1997), DOI: 10.1103/PhysRevLett.79.3435 [Nonlocal Dielectric Saturation]
        - Fabregas et al., Chem. Sci. 15, 1450-1458 (2024), DOI: 10.1039/D3SC05164B [Polarization Suppression in Water]
    """
    import numpy as np
    from scipy.ndimage import gaussian_filter1d
    from scipy.integrate import cumulative_trapezoid
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd
    import os

    n_frames = min(len(frames), len(charges_arr))
    if n_frames == 0:
        print("  [E-Field] No frames available for electric field analysis.")
        return

    # 1. --- Grid Setup ---
    z_edges = np.linspace(0, box_z, n_bins + 1)
    z_centers = (z_edges[:-1] + z_edges[1:]) / 2.0
    dz = z_centers[1] - z_centers[0]  # Ang

    # Box area calculation
    box_x = frames[0].box_lengths[0] if hasattr(frames[0], "box_lengths") else 20.21
    box_y = frames[0].box_lengths[1] if hasattr(frames[0], "box_lengths") else 17.53
    area = box_x * box_y

    # 2. --- Method 1: Poisson Integration (Macro) ---
    Q_bin = np.zeros(n_bins)
    for i in range(n_frames):
        pos = frames[i].positions[:, 2]
        q = charges_arr[i]
        hist, _ = np.histogram(pos, bins=z_edges, weights=q)
        Q_bin += hist
    Q_bin /= n_frames

    rho_z = Q_bin / (area * dz)  # e/Å³
    rho_z_smooth = gaussian_filter1d(rho_z, sigma=sigma / dz)

    E_CONV = 1.8095e12  # V/m per e/Å²
    E_Poisson = cumulative_trapezoid(rho_z_smooth, x=z_centers, initial=0) * E_CONV  # V/m
    Phi_z = -cumulative_trapezoid(E_Poisson, x=z_centers * 1e-10, initial=0)  # V

    # 3. --- Method 2: Langevin Dipole Inversion (Micro) ---
    cos_sum = np.zeros(n_bins)
    water_count = np.zeros(n_bins)

    z_axis = analyzer.z_axis
    z_hat = np.zeros(3)
    z_hat[z_axis] = 1.0

    for i in range(n_frames):
        frame = frames[i]
        box_lengths = frame.box_lengths
        water_mols, _, _ = analyzer._partition_atoms(frame)

        for wm in water_mols:
            # Minimum image convention to get bonds
            oh1 = wm.h1_position - wm.o_position
            oh1 -= box_lengths * np.round(oh1 / box_lengths)
            oh2 = wm.h2_position - wm.o_position
            oh2 -= box_lengths * np.round(oh2 / box_lengths)

            # Dipole bisector pointing from O to HH midpoint
            bisector = oh1 + oh2
            norm = np.linalg.norm(bisector)
            if norm < 1e-10:
                continue
            bisector_u = bisector / norm

            cos_phi = np.dot(bisector_u, z_hat)

            # Wrap oxygen Z coordinate
            z_o = wm.o_position[z_axis] % box_lengths[z_axis]

            idx = np.searchsorted(z_edges, z_o) - 1
            if 0 <= idx < n_bins:
                cos_sum[idx] += cos_phi
                water_count[idx] += 1

    # Planar-averaged dipole orientation profile
    cos_theta_avg = np.zeros(n_bins)
    valid_mask = water_count > 0
    cos_theta_avg[valid_mask] = cos_sum[valid_mask] / water_count[valid_mask]
    cos_theta_avg_smooth = gaussian_filter1d(cos_theta_avg, sigma=sigma / dz)

    # Langevin inversion: E = (kBT / mu) * L^-1(<cos theta>)
    kB = 1.380649e-23
    mu_water = 2.29 * 3.33564e-30  # 2.29 Debye in C*m
    E_0 = (kB * temperature) / mu_water  # V/m
    E_Langevin = E_0 * inverse_langevin(cos_theta_avg_smooth)  # V/m

    # Effective Dielectric Constant calculation: eps_eff = E_Poisson / E_Langevin
    eps_eff = np.zeros_like(E_Poisson)
    valid_e = np.abs(E_Langevin) > 1e7
    eps_eff[valid_e] = np.abs(E_Poisson[valid_e]) / np.abs(E_Langevin[valid_e])

    # Interfacial peak dielectric constant
    idx_peak_langevin = np.argmax(np.abs(E_Langevin))
    eps_eff_interfacial = np.abs(E_Poisson[idx_peak_langevin]) / np.abs(E_Langevin[idx_peak_langevin])

    # 4. --- Advanced 4-Panel Visualization ---
    fig, axs = plt.subplots(4, 1, figsize=(8, 15), sharex=True)

    # Panel 0: Charge Density
    axs[0].plot(z_centers, rho_z_smooth, color='royalblue', lw=1.5)
    axs[0].set_ylabel(r"Charge density $\rho(z)$ ($e/\mathrm{\AA}^3$)")
    axs[0].set_title("Interfacial Electrostatics & Local Fields Dual Analysis")
    axs[0].axhline(0, color='grey', ls='--', lw=0.5)

    # Panel 1: Electrostatic Potential
    axs[1].plot(z_centers, Phi_z, color='seagreen', lw=1.5)
    axs[1].set_ylabel(r"Electrostatic potential $\Phi(z)$ (V)")
    axs[1].axhline(0, color='grey', ls='--', lw=0.5)

    # Panel 2: Water Dipole Orientation Profile
    axs[2].plot(z_centers, cos_theta_avg_smooth, color='purple', lw=1.5)
    axs[2].set_ylabel(r"Water dipole orientation $\langle\cos\theta\rangle$")
    axs[2].axhline(0, color='grey', ls='--', lw=0.5)

    # Panel 3: E-field Dual-comparison
    axs[3].plot(z_centers, E_Poisson / 1e8, color='crimson', lw=1.8, label="Poisson (Macro)")
    axs[3].plot(z_centers, E_Langevin / 1e8, color='darkorange', lw=1.5, ls='--', label="Langevin (Micro)")
    axs[3].set_ylabel(r"Electric field $E(z)$ ($10^8$ V/m)")
    axs[3].set_xlabel(r"$z$ coordinate ($\mathrm{\AA}$)")
    axs[3].axhline(0, color='grey', ls='--', lw=0.5)
    axs[3].legend(loc="best", frameon=True)

    plt.tight_layout()
    out_png = os.path.join(output_dir, "electric_field_profile.png")
    plt.savefig(out_png, dpi=dpi, bbox_inches='tight')
    plt.close()

    # 5. --- Save CSV data for cross-case comparison ---
    df = pd.DataFrame({
        "z_Ang": z_centers,
        "rho_e_per_Ang3": rho_z_smooth,
        "E_Poisson_V_per_m": E_Poisson,
        "Phi_V": Phi_z,
        "cos_theta_avg": cos_theta_avg_smooth,
        "E_Langevin_V_per_m": E_Langevin,
        "eps_eff": eps_eff,
    })
    csv_path = os.path.join(output_dir, "electric_field_data.csv")
    df.to_csv(csv_path, index=False, float_format="%.6e")

    # 6. --- Save JSON summary & full profiles for automated cross-case comparison ---
    json_path = os.path.join(output_dir, "electric_field_results.json")
    results_dict = {
        "metadata": {
            "temperature_K": float(temperature),
            "n_frames": int(n_frames),
            "n_bins": int(n_bins),
            "box_z_Ang": float(box_z),
            "area_Ang2": float(area),
        },
        "poisson_summary": {
            "peak_electric_field_V_per_m": float(np.max(np.abs(E_Poisson))),
            "peak_z_Ang": float(z_centers[np.argmax(np.abs(E_Poisson))]),
            "potential_drop_V": float(np.abs(Phi_z[-1] - Phi_z[0])),
        },
        "langevin_summary": {
            "peak_electric_field_V_per_m": float(np.max(np.abs(E_Langevin))),
            "peak_z_Ang": float(z_centers[idx_peak_langevin]),
            "peak_cos_theta_avg": float(np.max(np.abs(cos_theta_avg_smooth))),
        },
        "dielectric_saturation_summary": {
            "interfacial_eps_eff_at_dipole_peak": float(eps_eff_interfacial),
            "eps_eff_global_peak_ratio": float(np.max(np.abs(E_Poisson)) / np.max(np.abs(E_Langevin))),
            "benchmark_literature_range": "~1.6 - 6.0 (Fumagalli et al. Science 2018, Bonthuis et al. PRL 2011)",
        },
        "profiles": {
            "z_Ang": [float(x) for x in z_centers],
            "rho_e_per_Ang3": [float(x) for x in rho_z_smooth],
            "E_Poisson_V_per_m": [float(x) for x in E_Poisson],
            "Phi_V": [float(x) for x in Phi_z],
            "cos_theta_avg": [float(x) for x in cos_theta_avg_smooth],
            "E_Langevin_V_per_m": [float(x) for x in E_Langevin],
            "eps_eff": [float(x) for x in eps_eff],
        }
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2)

    print(f"  [E-Field] Peak Poisson E-Field:       {np.max(np.abs(E_Poisson)):.4e} V/m (Macro Maxwell Field)")
    print(f"  [E-Field] Peak Langevin E-Field:      {np.max(np.abs(E_Langevin)):.4e} V/m (Micro Local Field)")
    print(f"  [E-Field] Interfacial Effective eps:  {eps_eff_interfacial:.2f} (Dielectric Saturation Benchmark: ~2-6)")
    print(f"  [E-Field] Total Potential Drop:       {np.abs(Phi_z[-1] - Phi_z[0]):.4f} V")
    print(f"  [E-Field] Figure saved: {out_png}")
    print(f"  [E-Field] CSV saved:    {csv_path}")
    print(f"  [E-Field] JSON saved:   {json_path}")


def main():
    args = parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("CP2K AIMD Interfacial Water Analysis (Protocol Steps 63-65)")
    print("=" * 70)
    print(f"Trajectory:       {args.xyz}")
    print(f"Cell file:        {args.cell_file}")
    print(f"Mode:             {args.mode}")
    if args.mode == "static":
        print(f"Static Z surface: {args.static_z_surface} Å")
    print(f"Sample interval:  every {args.sample_interval} frame(s)")
    print(f"Output directory: {output_dir}")
    print("-" * 70)

    # 1. Parse trajectory
    print("\n[1/4] Parsing trajectory file...")
    traj_path = Path(args.xyz)
    cell_path = Path(args.cell_file) if args.cell_file else None

    if not traj_path.exists():
        print(f"Error: Trajectory file not found: {traj_path}")
        sys.exit(1)

    if cell_path and not cell_path.exists():
        print(f"Warning: Cell file not found: {cell_path}. Running without box/PBC cell file.")
        cell_path = None

    parser = TrajectoryParser(str(traj_path), cell_filepath=cell_path)
    frames = parser.parse()
    print(f"    Total frames loaded: {len(frames)}")

    # Equilibration detection — cut BEFORE analysis
    import equilibration_utils
    import numpy as np
    base_dir = traj_path.parent
    t0_raw, g, Neff, actual_obs, ts_signal = equilibration_utils.resolve_equilibration_start(
        args, fallback_timeseries=None, fallback_observable="n_atoms",
        sample_interval=args.sample_interval, base_dir=base_dir
    )
    if ts_signal is not None and len(ts_signal) > 0:
        if actual_obs in {"potential_energy", "temperature", "kinetic_energy", "conserved_quantity"}:
            time_arr_fs = np.arange(len(ts_signal)) * args.timestep
        else:
            time_arr_fs = np.arange(len(ts_signal)) * args.sample_interval * args.timestep
    else:
        time_arr_fs = np.array([])
    equilibration_utils.generate_equilibration_report_and_plot(
        t0_raw, g, Neff, ts_signal, time_arr_fs, actual_obs, output_dir
    )
    if t0_raw > 0:
        print(f"    [Equilibration] Discarding first {t0_raw} raw frames as equilibration phase.")
        frames = frames[t0_raw:]
        print(f"    [Equilibration] Production phase raw frames: {len(frames)}")

    # 2. Run analysis
    print("\n[2/4] Initializing InterfacialAnalyzer and running pipeline...")
    try:
        analyzer = InterfacialAnalyzer(
            mode=args.mode,
            interface_cutoff=args.interface_cutoff,
            z_axis=args.z_axis,
            n_bins=args.n_bins,
            density_sigma=args.density_sigma,
            static_z_surface=args.static_z_surface,
            r_oh_max=args.r_oh_max,
            r_oo_hbond=args.r_oo_hbond,
            angle_ooh_hbond=args.angle_ooh_hbond,
            verbose=True,
        )
    except ValueError as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)

    # Process subset/stride
    result = analyzer.run_full_analysis(
        frames,
        start=0,
        stop=None,
        step=args.sample_interval,
    )

    # 3. Save JSON and generate plots
    print("\n[3/4] Saving results and generating plots...")
    json_path = output_dir / "interfacial_analysis_results.json"
    result.to_json(json_path)
    print(f"    JSON results saved to: {json_path}")

    visualizer = InterfacialVisualizer(dpi=args.dpi)
    # The analyzer computes stride dynamics, but timestep needs to be scaled by sample_interval
    effective_timestep = args.timestep * args.sample_interval
    start_time_fs = t0_raw * args.timestep
    visualizer.plot_all(
        result,
        save_dir=output_dir,
        timestep_fs=effective_timestep,
        start_time_fs=start_time_fs,
    )


    # 4. Electric Field Analysis
    print("\n[4/4] Extracting Mulliken charges and quantifying Electric Field...")
    
    # Auto-detect CP2K out files if not explicitly provided
    cp2k_outs = args.cp2k_out
    if cp2k_outs is None:
        default_outs = sorted([str(p) for p in base_dir.glob("*.out") if not p.name.startswith("slurm")], key=natural_sort_key)
        if default_outs:
            cp2k_outs = default_outs

    mulliken_cache_path = args.mulliken_cache
    if mulliken_cache_path is None:
        mulliken_cache_path = str(output_dir / "mulliken_spins_cache.npz")

    if cp2k_outs:
        spins_arr, charges_arr = extract_or_load_mulliken_spins(
            cp2k_outs,
            cache_path=mulliken_cache_path,
            n_atoms=len(frames[0].positions),
            verbose=True
        )
        # Apply equilibration cut
        if t0_raw > 0 and len(charges_arr) > t0_raw:
            charges_arr = charges_arr[t0_raw:]
            
        box_lengths = frames[0].box_lengths if hasattr(frames[0], "box_lengths") else None
        box_z = box_lengths[2] if box_lengths is not None else 63.77
        analyze_and_plot_electric_field(
            frames, charges_arr, box_z, args.n_bins, args.density_sigma, output_dir, analyzer, args.temperature, args.dpi
        )
    else:
        print("  [E-Field] No --cp2k-out files provided or auto-detected. Skipping electric field quantification.")

    print("\n" + "=" * 70)
    print("Interfacial water analysis completed successfully!")
    print(f"Results available in: {output_dir}/")
    print("=" * 70)


if __name__ == "__main__":
    main()

