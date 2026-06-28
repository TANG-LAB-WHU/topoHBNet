"""
Equilibration Detection Utilities for AIMD Trajectory Analysis.

Implements Chodera's automated equilibration detection (JCTC 2016, https://pubs.acs.org/doi/10.1021/acs.jctc.5b00784)
via pymbar.timeseries.detect_equilibration().
"""

import os
import sys
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def add_equilibration_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add standard equilibration detection arguments to an ArgumentParser."""
    group = parser.add_argument_group("Equilibration Detection Options (Chodera 2016)")
    group.add_argument(
        "--equil-auto",
        action="store_true",
        default=True,
        help="Enable automated equilibration detection using pymbar (Chodera 2016) (Enabled by default)."
    )
    group.add_argument(
        "--no-equil-auto",
        action="store_false",
        dest="equil_auto",
        help="Disable automated equilibration detection."
    )
    group.add_argument(
        "--equil-start-frame",
        type=int,
        default=None,
        help="Explicitly specify the start frame for production phase (overrides --equil-auto)."
    )
    group.add_argument(
        "--equil-observable",
        type=str,
        default="potential_energy",
        help="Observable to use for automated equilibration detection (default: potential_energy). Options include: potential_energy, temperature, kinetic_energy, conserved_quantity, n_hbonds, euler_characteristic, H2O_count, lbhb_fraction."
    )
    group.add_argument(
        "--equil-ener-file",
        type=str,
        default="trajectory.ener",
        help="Path to the CP2K .ener file used for fetching energy/thermodynamic observables (default: trajectory.ener)."
    )
    return parser


def detect_equilibration_auto(timeseries: np.ndarray):
    """
    Run pymbar.timeseries.detect_equilibration on a 1D timeseries array.
    Returns (t0, g, Neff). If pymbar is not available or fails, returns (0, 1.0, len(timeseries)).
    """
    try:
        from pymbar import timeseries as pyts
        t0, g, Neff = pyts.detect_equilibration(timeseries)
        return t0, g, Neff
    except ImportError:
        print("    [Equilibration Warning] pymbar is not installed. Automated detection disabled. Defaulting to t0 = 0.")
        return 0, 1.0, len(timeseries)
    except Exception as e:
        print(f"    [Equilibration Warning] detect_equilibration failed ({e}). Defaulting to t0 = 0.")
        return 0, 1.0, len(timeseries)


def parse_ener_file(ener_path: Path, observable_name: str):
    """
    Parse CP2K .ener file to extract the specified timeseries.
    Columns in standard CP2K .ener file (Step, Time, Kin, Temp, Pot, Cons).
    """
    if not ener_path.exists():
        return None
    try:
        # Read lines, skip header
        with open(ener_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        values = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("Step"):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            # Mapping observable to column index
            if observable_name == "potential_energy":
                val = float(parts[4])
            elif observable_name == "temperature":
                val = float(parts[3])
            elif observable_name == "kinetic_energy":
                val = float(parts[2])
            elif observable_name == "conserved_quantity":
                val = float(parts[5])
            else:
                val = float(parts[4]) # default potential
            values.append(val)
        return np.array(values)
    except Exception as e:
        print(f"    [Equilibration Warning] Failed to parse ener file {ener_path}: {e}")
        return None


def resolve_equilibration_start(args, fallback_timeseries=None, fallback_observable=None, sample_interval=1, base_dir=Path(".")):
    """
    Determine t0 cutoff frame index, g, Neff, actual_observable, and the timeseries used.
    Handles ener file loading, downsampling matching, and smart fallback.
    """
    # 1. Manual override
    if getattr(args, "equil_start_frame", None) is not None:
        t0 = args.equil_start_frame
        actual_obs = "manual_override"
        ts = fallback_timeseries if fallback_timeseries is not None else np.array([])
        return t0, 1.0, len(ts) - t0 if len(ts) > t0 else 0, actual_obs, ts

    # 2. If auto is not enabled, return 0
    if not getattr(args, "equil_auto", False):
        ts = fallback_timeseries if fallback_timeseries is not None else np.array([])
        return 0, 1.0, len(ts), "none", ts

    # 3. Auto detection enabled
    observable = getattr(args, "equil_observable", "potential_energy")
    ener_file = getattr(args, "equil_ener_file", "trajectory.ener")
    ener_path = base_dir / ener_file

    ener_observables = {"potential_energy", "temperature", "kinetic_energy", "conserved_quantity"}

    if observable in ener_observables:
        ener_ts = parse_ener_file(ener_path, observable)
        if ener_ts is not None and len(ener_ts) > 0:
            print(f"    [Equilibration] Running automated detection using {observable} from {ener_path}...")
            t0_ener, g, Neff = detect_equilibration_auto(ener_ts)
            # Adjust for sample_interval if this script uses sampled frames
            t0 = t0_ener // sample_interval
            print(f"    [Equilibration] Detected t0_ener = {t0_ener} -> script t0 = {t0} (sample_interval={sample_interval})")
            return t0, g, Neff, observable, ener_ts
        else:
            print(f"    [Equilibration Warning] {observable} requested but {ener_path} not found or invalid.")
            if fallback_timeseries is not None and fallback_observable is not None:
                print(f"    [Equilibration] Smart Fallback: using script native observable '{fallback_observable}'.")
                t0, g, Neff = detect_equilibration_auto(np.array(fallback_timeseries))
                return t0, g, Neff, fallback_observable, np.array(fallback_timeseries)
            else:
                return 0, 1.0, 0, "none", np.array([])
    else:
        # Non-energetic observable requested (e.g. n_hbonds, H2O_count)
        if fallback_timeseries is not None:
            print(f"    [Equilibration] Running automated detection using requested observable '{observable}'...")
            t0, g, Neff = detect_equilibration_auto(np.array(fallback_timeseries))
            return t0, g, Neff, observable, np.array(fallback_timeseries)
        else:
            return 0, 1.0, 0, "none", np.array([])


def generate_equilibration_report_and_plot(t0, g, Neff, timeseries, time_fs_arr, observable_name, output_dir: Path):
    """
    Generate equilibration_report.json and equilibration_cutoff_diagnostic.png.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON report
    report = {
        "t0_cutoff_index": int(t0),
        "statistical_inefficiency_g": float(g),
        "effective_independent_samples_Neff": float(Neff),
        "actual_observable": observable_name
    }
    with open(output_dir / "equilibration_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(f"    Saved: {output_dir / 'equilibration_report.json'}")

    if timeseries is None or len(timeseries) == 0:
        return

    # Generate diagnostic plot
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    
    # Ensure time_fs_arr matches timeseries length
    if time_fs_arr is None or len(time_fs_arr) != len(timeseries):
        time_fs_arr = np.arange(len(timeseries))

    ax.plot(time_fs_arr, timeseries, color="#2C3E50", label=f"{observable_name} timeseries", linewidth=1.5)
    
    if t0 > 0 and t0 < len(timeseries):
        # Cutoff line
        cutoff_time = time_fs_arr[t0]
        ax.axvline(x=cutoff_time, color="#E74C3C", linestyle="--", linewidth=2.5, label=f"Cutoff t0={t0} ({cutoff_time:.1f} fs)")
        
        # Shading equilibration phase
        ax.axvspan(time_fs_arr[0], cutoff_time, color="#E59866", alpha=0.2, label="Equilibration Phase (Discarded)")
    
    ax.set_xlabel("Time / Frame", fontsize=12, fontweight="bold")
    ax.set_ylabel(observable_name.replace("_", " ").title(), fontsize=12, fontweight="bold")
    ax.set_title("Equilibration Detection Diagnostic Plot", fontsize=14, fontweight="bold", pad=15)
    
    # Add text box with metrics
    textstr = f"[pymbar Automated Detection]\nObservable: {observable_name}\nOptimal Cutoff Frame (t0): {t0}\nStatistical Inefficiency (g): {g:.2f}\nEffective Samples (Neff): {Neff:.1f}"
    props = dict(boxstyle='round', facecolor='#F8F9F9', alpha=0.85, edgecolor='#BDC3C7')
    ax.text(0.02, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props, fontfamily='monospace')

    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#BDC3C7")
    fig.tight_layout()
    
    plot_path = output_dir / "equilibration_cutoff_diagnostic.png"
    fig.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"    Saved: {plot_path}")
