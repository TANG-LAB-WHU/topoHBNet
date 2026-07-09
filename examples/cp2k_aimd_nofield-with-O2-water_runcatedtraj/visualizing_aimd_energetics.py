#!/usr/bin/env python3
"""
Generates line-style plots with gradient fills for:
  - Temperature vs. simulation time
  - Kinetic energy vs. simulation time
  - Potential energy vs. simulation time
  - Total (conserved) energy vs. simulation time

Usage:
    python visualizing_aimd_energetics.py [--input INPUT] [--output OUTPUT]
"""

import argparse
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Visualize AIMD energetics from CP2K trajectory.ener"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default="trajectory.ener",
        help="Path to trajectory.ener file (default: trajectory.ener)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="visualization_aimd_energetics",
        help="Output directory name (default: visualization_aimd_energetics)"
    )
    parser.add_argument(
        "--target-temp", "-t",
        type=float,
        default=298.0,
        help="Target temperature in Kelvin to display (default: 298.0 K)"
    )
    parser.add_argument(
        "--save-csv",
        action="store_true",
        default=True,
        help="Export raw data to CSV (default: True)"
    )
    parser.add_argument(
        "--no-csv",
        action="store_false",
        dest="save_csv",
        help="Disable CSV export"
    )
    import equilibration_utils
    parser = equilibration_utils.add_equilibration_args(parser)
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_ener(filepath: str) -> dict:
    """Load CP2K .ener file and return a dict of numpy arrays."""
    steps, times, kin, temp, pot, cons_qty = [], [], [], [], [], []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            steps.append(int(parts[0]))
            times.append(float(parts[1]))
            kin.append(float(parts[2]))
            temp.append(float(parts[3]))
            pot.append(float(parts[4]))
            cons_qty.append(float(parts[5]))

    return {
        "step": np.array(steps),
        "time_fs": np.array(times),
        "kinetic_au": np.array(kin),
        "temperature_K": np.array(temp),
        "potential_au": np.array(pot),
        "conserved_au": np.array(cons_qty),
    }


# ---------------------------------------------------------------------------
# Gradient fill helper
# ---------------------------------------------------------------------------

def gradient_fill(ax, x, y, color_top, color_bottom="white", alpha=0.45, n_bands=120):
    """
    Create a smooth vertical gradient fill between y=min and the curve.

    Parameters
    ----------
    ax : matplotlib Axes
    x, y : array-like
    color_top : str or tuple – colour at the curve
    color_bottom : str or tuple – colour at the baseline (default white)
    alpha : float – maximum alpha of the fill
    n_bands : int – number of horizontal bands for the gradient
    """
    y_min = np.min(y)
    y_max = np.max(y)
    margin = (y_max - y_min) * 0.02
    levels = np.linspace(y_min - margin, y_max + margin, n_bands)

    # Build a custom colormap from bottom to top colour
    cmap = LinearSegmentedColormap.from_list(
        "grad", [color_bottom, color_top], N=256
    )

    for i in range(len(levels) - 1):
        band_lo = levels[i]
        band_hi = levels[i + 1]
        frac = i / (len(levels) - 1)
        band_alpha = alpha * frac  # fade from transparent at bottom to alpha at top
        clipped_y = np.clip(y, band_lo, band_hi)
        ax.fill_between(
            x, band_lo, clipped_y,
            color=cmap(frac),
            alpha=band_alpha,
            linewidth=0,
        )


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

# Soft, premium pastel palette
PALETTE = {
    "temperature": "#FF6B8A",   # soft rose
    "kinetic":     "#6BC5FF",   # soft sky blue
    "potential":   "#7ED68A",   # soft mint green
    "conserved":   "#B48AFF",   # soft lavender
}

PLOT_SPECS = [
    {
        "key": "temperature_K",
        "label": "Temperature",
        "ylabel": "Temperature (K)",
        "color": PALETTE["temperature"],
        "filename": "temperature_vs_time",
    },
    {
        "key": "kinetic_au",
        "label": "Kinetic Energy",
        "ylabel": "Kinetic Energy (a.u.)",
        "color": PALETTE["kinetic"],
        "filename": "kinetic_energy_vs_time",
    },
    {
        "key": "potential_au",
        "label": "Potential Energy",
        "ylabel": "Potential Energy (a.u.)",
        "color": PALETTE["potential"],
        "filename": "potential_energy_vs_time",
    },
    {
        "key": "conserved_au",
        "label": "Conserved Quantity (Total Energy)",
        "ylabel": "Conserved Quantity (a.u.)",
        "color": PALETTE["conserved"],
        "filename": "total_energy_vs_time",
    },
]

DPI = 600


def setup_style():
    """Apply a clean, modern matplotlib style."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 11,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#444444",
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "legend.fontsize": 10,
        "legend.framealpha": 0.85,
        "legend.edgecolor": "#cccccc",
        "figure.facecolor": "white",
        "axes.facecolor": "#FAFAFA",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "grid.color": "#CCCCCC",
    })


def plot_single(data, spec, outdir, target_temp=None):
    """Create a single property-vs-time plot with gradient fill."""
    x = data["time_fs"]
    y = data[spec["key"]]

    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=DPI)

    # Gradient fill beneath the curve
    gradient_fill(ax, x, y, color_top=spec["color"], alpha=0.40)

    # Main curve
    ax.plot(
        x, y,
        color=spec["color"],
        linewidth=1.2,
        label=spec["label"],
        zorder=5,
    )

    # Target temperature annotation if applicable
    if spec["key"] == "temperature_K" and target_temp is not None:
        ax.axhline(
            target_temp, 
            color="#333333", 
            linestyle="--", 
            linewidth=1.5, 
            label=f"Target temperature ({target_temp} K)",
            zorder=6,
            alpha=0.6
        )
        # Add a text box for the target temp
        ax.text(
            x.min() + (x.max() - x.min()) * 0.05, target_temp, 
            f"Target temperature: {target_temp} K", 
            color="#333333",
            va="bottom", ha="left",
            fontsize=10, fontweight="bold",
            alpha=0.8,
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=2)
        )

    ax.set_xlabel("Simulation Time (fs)")
    ax.set_ylabel(spec["ylabel"])
    ax.set_title(f"{spec['label']} vs. Simulation Time")
    ax.set_xlim(x.min(), x.max())
    ax.legend(loc="best")

    fig.tight_layout()

    # Save in both PNG and SVG
    for ext in ("png", "svg"):
        path = os.path.join(outdir, f"{spec['filename']}.{ext}")
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        print(f"  Saved: {path}")

    plt.close(fig)


def plot_combined(data, outdir, target_temp=None):
    """Create a 2x2 panel with all four properties."""
    x = data["time_fs"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), dpi=DPI)
    axes = axes.flatten()

    for ax, spec in zip(axes, PLOT_SPECS):
        y = data[spec["key"]]

        gradient_fill(ax, x, y, color_top=spec["color"], alpha=0.40)
        ax.plot(
            x, y,
            color=spec["color"],
            linewidth=1.0,
            label=spec["label"],
            zorder=5,
        )

        # Add target temperature line for Temperature plot
        if spec["key"] == "temperature_K" and target_temp is not None:
            ax.axhline(
                target_temp, 
                color="#333333", 
                linestyle="--", 
                linewidth=1.2, 
                zorder=6,
                alpha=0.5
            )
            # Add target temp label in combined plot too
            ax.text(
                x.min() + (x.max() - x.min()) * 0.05, target_temp, 
                f"{target_temp} K", 
                color="#333333",
                va="bottom", ha="left",
                fontsize=8, fontweight="bold",
                alpha=0.7
            )

        ax.set_xlabel("Simulation Time (fs)")
        ax.set_ylabel(spec["ylabel"])
        ax.set_title(spec["label"])
        ax.set_xlim(x.min(), x.max())
        ax.legend(loc="best", fontsize=9)

    fig.suptitle("AIMD Energetics Overview", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()

    for ext in ("png", "svg"):
        path = os.path.join(outdir, f"aimd_energetics_combined.{ext}")
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        print(f"  Saved: {path}")

    plt.close(fig)


def export_to_csv(data, outdir):
    """Export raw energetics data to a CSV file in outdir."""
    import pandas as pd
    
    # Create DataFrame
    df = pd.DataFrame({
        "Step": data["step"],
        "Time_fs": data["time_fs"],
        "Kinetic_au": data["kinetic_au"],
        "Temperature_K": data["temperature_K"],
        "Potential_au": data["potential_au"],
        "Conserved_au": data["conserved_au"]
    })
    
    csv_path = os.path.join(outdir, "aimd_energetics_raw_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"  CSV exported: {csv_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = args.input if os.path.isabs(args.input) else os.path.join(script_dir, args.input)
    output_dir = args.output if os.path.isabs(args.output) else os.path.join(script_dir, args.output)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Input  : {input_path}")
    print(f"Output : {output_dir}")
    print()

    # Load data
    data = load_ener(input_path)
    print(f"Loaded {len(data['step'])} frames  |  "
          f"Time range: {data['time_fs'][0]:.1f} – {data['time_fs'][-1]:.1f} fs")
    print()

    # Equilibration detection and cutoff
    import equilibration_utils
    obs_key = {
        "potential_energy": "potential_au",
        "temperature": "temperature_K",
        "kinetic_energy": "kinetic_au",
        "conserved_quantity": "conserved_au"
    }.get(getattr(args, "equil_observable", "potential_energy"), "potential_au")
    
    ts_signal = np.array(data[obs_key])
    t0_raw, g, Neff, actual_obs, _ = equilibration_utils.resolve_equilibration_start(
        args, fallback_timeseries=ts_signal, fallback_observable=getattr(args, "equil_observable", "potential_energy"),
        sample_interval=1, base_dir=__import__("pathlib").Path(script_dir)
    )
    equilibration_utils.generate_equilibration_report_and_plot(
        t0_raw, g, Neff, ts_signal, np.array(data["time_fs"]), actual_obs, output_dir
    )
    if t0_raw > 0:
        print(f"    [Equilibration] Discarding first {t0_raw} frames as equilibration phase.")
        for k in data:
            data[k] = data[k][t0_raw:]
        print(f"    [Equilibration] Production phase frames: {len(data['step'])}  |  Time range: {data['time_fs'][0]:.1f} – {data['time_fs'][-1]:.1f} fs\n")

    # Apply style
    setup_style()

    # Individual plots
    print(f"Generating individual plots (Target Temp: {args.target_temp} K) …")
    for spec in PLOT_SPECS:
        plot_single(data, spec, output_dir, target_temp=args.target_temp)

    # Combined panel
    print("\nGenerating combined panel …")
    plot_combined(data, output_dir, target_temp=args.target_temp)

    # Export CSV if requested
    if args.save_csv:
        print("\nExporting raw data to CSV …")
        export_to_csv(data, output_dir)

    print("\nAll plots generated successfully.")


if __name__ == "__main__":
    main()
