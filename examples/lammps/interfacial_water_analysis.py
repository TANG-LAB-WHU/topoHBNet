#!/usr/bin/env python3
"""
This script implements Steps 63-65 of the Nature Protocols paper (Li et al. 2023)
for solid-liquid interfaces. It detects the interface dynamically (via density
crossover / Gibbs dividing surface) or statically (fixed Z coordinate), separates
interfacial and bulk water, and computes orientation and H-bonding profiles.

Usage:
    python interfacial_water_analysis.py --trajectory trajectory.lammpstrj --data-file model.lmpdat --mode dynamic
    python interfacial_water_analysis.py --trajectory trajectory.lammpstrj --type-map "1:O 2:H" --mode static --static-z-surface 15.0
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for development/execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from hbond_topology.io.trajectory_parser import TrajectoryParser
from hbond_topology.analysis.interfacial import InterfacialAnalyzer, InterfacialVisualizer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interfacial Water Analysis (Protocol Steps 63-65) for LAMMPS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Trajectory options
    parser.add_argument(
        "--trajectory",
        type=str,
        default="trajectory.lammpstrj",
        help="Path to LAMMPS trajectory file.",
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default="model.lmpdat",
        help="Path to LAMMPS data file (used for mass->element mapping).",
    )
    parser.add_argument(
        "--type-map",
        type=str,
        default=None,
        help="Manual type mapping in format '1:O 2:H'. Overrides --data-file.",
    )
    parser.add_argument(
        "--timestep",
        type=float,
        default=0.5,
        help="Simulation timestep in femtoseconds.",
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

    return parser.parse_args()


def main():
    args = parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("LAMMPS AIMD Interfacial Water Analysis (Protocol Steps 63-65)")
    print("=" * 70)
    print(f"Trajectory:       {args.trajectory}")
    print(f"Data file:        {args.data_file}")
    print(f"Type map:         {args.type_map}")
    print(f"Mode:             {args.mode}")
    if args.mode == "static":
        print(f"Static Z surface: {args.static_z_surface} Å")
    print(f"Sample interval:  every {args.sample_interval} frame(s)")
    print(f"Output directory: {output_dir}")
    print("-" * 70)

    # 1. Parse trajectory
    print("\n[1/3] Parsing trajectory file...")
    traj_path = Path(args.trajectory)

    if not traj_path.exists():
        print(f"Error: Trajectory file not found: {traj_path}")
        sys.exit(1)

    specorder = None
    lammps_data = None
    
    if args.type_map:
        # Manual mapping: "1:O 2:H 3:Si 4:C"
        type_dict = {}
        for pair in args.type_map.split():
            tid_str, sym = pair.split(':')
            type_dict[int(tid_str)] = sym
        max_t = max(type_dict.keys())
        specorder = [type_dict.get(t, 'X') for t in range(1, max_t + 1)]
        print(f"    Using manual type map: {args.type_map}")
        print(f"    specorder = {specorder}")
    elif args.data_file:
        data_path = Path(args.data_file)
        if data_path.exists():
            lammps_data = data_path
            print(f"    Reading atom types from: {data_path.name}")
        else:
            print(f"    Warning: Data file not found: {data_path}")
            print(f"    ASE will assign types sequentially (may be incorrect!)")

    parser = TrajectoryParser(
        str(traj_path),
        specorder=specorder,
        lammps_data_file=lammps_data
    )
    frames = parser.parse()
    print(f"    Total frames loaded: {len(frames)}")

    # 2. Run analysis
    print("\n[2/3] Initializing InterfacialAnalyzer and running pipeline...")
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
    print("\n[3/3] Saving results and generating plots...")
    json_path = output_dir / "interfacial_analysis_results.json"
    result.to_json(json_path)
    print(f"    JSON results saved to: {json_path}")

    visualizer = InterfacialVisualizer(dpi=args.dpi)
    # The analyzer computes stride dynamics, but timestep needs to be scaled by sample_interval
    effective_timestep = args.timestep * args.sample_interval
    visualizer.plot_all(
        result,
        save_dir=output_dir,
        timestep_fs=effective_timestep,
    )

    print("\n" + "=" * 70)
    print("Interfacial water analysis completed successfully!")
    print(f"Results available in: {output_dir}/")
    print("=" * 70)


if __name__ == "__main__":
    main()
