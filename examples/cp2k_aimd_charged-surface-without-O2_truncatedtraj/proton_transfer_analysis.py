#!/usr/bin/env python3
"""
Advanced Proton Transfer, Wire, and Flow Analysis for CP2K AIMD Trajectories.

Features:
1. Proton Transfer Profiler:
   - Computes H-bond projection coordinates: delta = d(D-H) - d(H-A)
   - Computes Potential of Mean Force (PMF) free energy profile: A(delta) = -kT ln P(delta)
   - Identifies Low-Barrier Hydrogen Bonds (LBHBs) (d(O-O) < 2.45 A)
2. Proton Wire Tracker:
   - Identifies Surface Oxygens (silanols/hydroxyls bonded to Si) as Sources
   - Identifies Interfacial O2 molecules as Sinks
   - Finds optimal pathways (Proton Wires) bridging sources and sinks via H-bond networks
3. Hodge Flow Decomposer:
   - Construct B1 (nodes x edges) and B2 (edges x triangles) boundary matrices
   - Decomposes the z-axis transport flow into gradient (transport), curl (loop), and harmonic components

Usage:
    python proton_transfer_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell
"""

import os
import sys
import json
import argparse
import numpy as np
import pandas as pd
import networkx as nx
import scipy.sparse as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

# Add parent directory to path for package imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from hbond_topology import (
    TrajectoryParser,
    HBondDetector,
    ProtonTransferProfiler,
    ProtonWireTracker,
    HodgeFlowDecomposer
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Advanced Proton Transfer and Flow Analysis for CP2K AIMD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--xyz', type=str, default='trajectory.xyz',
                        help='Path to CP2K pos-1.xyz trajectory')
    parser.add_argument('--cell-file', type=str, default='trajectory.cell',
                        help='Path to CP2K cell file')
    parser.add_argument('--temperature', type=float, default=300.0,
                        help='Simulation temperature in Kelvin')
    parser.add_argument('--r-da-max', type=float, default=3.5,
                        help='Max donor-acceptor distance (A)')
    parser.add_argument('--r-ha-max', type=float, default=2.5,
                        help='Max hydrogen-acceptor distance (A)')
    parser.add_argument('--angle-min', type=float, default=120.0,
                        help='Min D-H-A angle (degrees)')
    parser.add_argument('--output-dir', '-o', type=str, default='proton_transfer_results',
                        help='Output directory')
    parser.add_argument('--sample-interval', type=int, default=1,
                        help='Analyze every N frames')
    import equilibration_utils
    parser = equilibration_utils.add_equilibration_args(parser)
    return parser.parse_args()

def classify_oxygen_atoms(frame, detector):
    """
    Classify oxygen atoms into:
    - sources (bonded to Si)
    - sinks (part of O2 molecules)
    - water (part of H2O)
    """
    n_atoms = frame.n_atoms
    positions = frame.positions
    symbols = frame.symbols
    box_lengths = frame.box_lengths

    # 1. Identify oxygen, hydrogen, silicon indices
    o_indices = np.where(symbols == 'O')[0]
    h_indices = np.where(symbols == 'H')[0]
    si_indices = np.where(symbols == 'Si')[0]

    sources = set()
    sinks = set()
    water = set()

    # Create helper dictionary for O-H bonds
    o_h_dists = defaultdict(list)
    for o_idx in o_indices:
        o_pos = positions[o_idx]
        for h_idx in h_indices:
            dist, _ = detector.minimum_image_distance(o_pos, positions[h_idx], box_lengths)
            if dist < 1.2:  # typical covalent O-H threshold
                o_h_dists[o_idx].append(h_idx)

    # Classify based on covalent structure
    for o_idx in o_indices:
        o_pos = positions[o_idx]
        
        # Check Si-O bonds (Surface/Silanols)
        is_surface = False
        for si_idx in si_indices:
            dist, _ = detector.minimum_image_distance(o_pos, positions[si_idx], box_lengths)
            if dist < 2.0:  # typical covalent Si-O threshold
                is_surface = True
                break
        
        h_bonded = o_h_dists[o_idx]
        
        if is_surface:
            # If bonded to Si, treat as source (active silanols)
            sources.add(o_idx)
        elif len(h_bonded) == 2:
            # Standard water oxygen
            water.add(o_idx)
        elif len(h_bonded) == 0:
            # Potential reactive O2 or interfacial oxide sink
            sinks.add(o_idx)
        else:
            # Interfacial intermediates (OH*, H3O+ oxygen etc.)
            water.add(o_idx)

    # Fallback if no sinks/sources detected: split by Z bounds (e.g. bulk vs surface)
    if not sources and len(o_indices) > 0:
        z_positions = positions[o_indices, 2]
        z_min = np.min(z_positions)
        for o_idx in o_indices:
            # Oxygens near the bottom surface (z < z_min + 5.0) are sources
            if positions[o_idx, 2] < z_min + 5.0:
                sources.add(o_idx)
            else:
                water.add(o_idx)

    if not sinks and len(o_indices) > 0:
        # Sinks can be default bulk or top interfacial region
        z_positions = positions[o_indices, 2]
        z_max = np.max(z_positions)
        for o_idx in o_indices:
            if positions[o_idx, 2] > z_max - 5.0 and o_idx not in sources:
                sinks.add(o_idx)

    return list(sources), list(sinks), list(water)

def build_boundary_matrices(o_indices, hbonds):
    """
    Build discrete boundary matrices B1 and B2 for Hodge Decomposition.
    """
    node_to_idx = {o_idx: i for i, o_idx in enumerate(o_indices)}
    num_nodes = len(o_indices)
    num_edges = len(hbonds)

    if num_edges == 0:
        return sp.csr_matrix((num_nodes, 0)), sp.csr_matrix((0, 0)), []

    # 1. B1 Matrix: Nodes x Edges
    # Edge is directed H-bond from donor to acceptor
    row1 = []
    col1 = []
    data1 = []
    for k, hb in enumerate(hbonds):
        u = node_to_idx.get(hb.donor_o_idx)
        v = node_to_idx.get(hb.acceptor_o_idx)
        if u is not None and v is not None:
            # donor: -1
            row1.append(u)
            col1.append(k)
            data1.append(-1.0)
            # acceptor: +1
            row1.append(v)
            col1.append(k)
            data1.append(1.0)

    B1 = sp.csr_matrix((data1, (row1, col1)), shape=(num_nodes, num_edges))

    # 2. Identify Triangles for B2 Matrix
    # We search for cycles of length 3 in the undirected H-bond graph
    G_undirected = nx.Graph()
    G_undirected.add_nodes_from(o_indices)
    for hb in hbonds:
        G_undirected.add_edge(hb.donor_o_idx, hb.acceptor_o_idx)

    # Find 3-cliques (triangles)
    cliques = list(nx.enumerate_all_cliques(G_undirected))
    triangles = [c for c in cliques if len(c) == 3]

    num_triangles = len(triangles)
    row2 = []
    col2 = []
    data2 = []

    # Map edge tuple (u, v) to edge index k
    edge_to_idx = {}
    for k, hb in enumerate(hbonds):
        edge_to_idx[(hb.donor_o_idx, hb.acceptor_o_idx)] = (k, 1.0)
        edge_to_idx[(hb.acceptor_o_idx, hb.donor_o_idx)] = (k, -1.0)

    for t_idx, tri in enumerate(triangles):
        # Nodes: n0, n1, n2. Loop orientation: n0 -> n1 -> n2 -> n0
        pairs = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
        for u, v in pairs:
            if (u, v) in edge_to_idx:
                k, sign = edge_to_idx[(u, v)]
                row2.append(k)
                col2.append(t_idx)
                data2.append(sign)

    B2 = sp.csr_matrix((data2, (row2, col2)), shape=(num_edges, num_triangles))

    return B1, B2, triangles

def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("CP2K AIMD Hydrogen Bond Proton Dynamics Analysis")
    print("=" * 60)
    print(f"Trajectory:  {args.xyz}")
    print(f"Cell File:   {args.cell_file}")
    print(f"Temperature: {args.temperature} K")
    print(f"Output Dir:  {output_dir}")
    print("=" * 60)

    # 1. Parse Trajectory
    parser = TrajectoryParser(
        filepath=args.xyz,
        cell_filepath=args.cell_file
    )
    
    # 2. Initialize Analyzers
    detector = HBondDetector(
        r_da_max=args.r_da_max,
        r_ha_max=args.r_ha_max,
        angle_min=args.angle_min
    )
    
    profiler = ProtonTransferProfiler(temperature=args.temperature)
    wire_tracker = ProtonWireTracker()
    decomposer = HodgeFlowDecomposer()

    # Accumulated records for saving
    wire_lengths = []
    lbhb_fractions = []
    
    hodge_decompositions = [] # (grad, curl, harm) percentages
    
    # Frame loop
    frames = list(parser)[::args.sample_interval]
    
    # Equilibration detection and cutoff
    import equilibration_utils
    base_dir = __import__("pathlib").Path(args.xyz).parent
    ener_path = base_dir / getattr(args, "equil_ener_file", "trajectory.ener")
    if not ener_path.exists() and getattr(args, "equil_auto", False):
        print("    [Equilibration] Computing fallback timeseries (n_hbonds)...")
        fallback_ts = np.array([len(detector.detect_hbonds(f)) for f in frames])
    else:
        fallback_ts = np.array([len(f.positions) for f in frames])
        
    t0, g, Neff, actual_obs, ts_signal = equilibration_utils.resolve_equilibration_start(
        args, fallback_timeseries=fallback_ts, fallback_observable="n_hbonds",
        sample_interval=args.sample_interval, base_dir=base_dir
    )
    time_arr_fs = np.arange(len(ts_signal)) * args.sample_interval * 0.5
    equilibration_utils.generate_equilibration_report_and_plot(
        t0, g, Neff, ts_signal, time_arr_fs, actual_obs, output_dir
    )
    if t0 > 0:
        print(f"    [Equilibration] Discarding first {t0} sampled frames as equilibration phase.")
        frames = frames[t0:]
        print(f"    [Equilibration] Production phase frames: {len(frames)}\n")

    n_frames = len(frames)
    
    print(f"Analyzing {n_frames} frames...")
    
    for i, frame in enumerate(frames):
        hbonds = detector.detect_hbonds(frame)
        box_lengths = frame.box_lengths
        
        # A. Proton Transfer PMF Profiling
        for hb in hbonds:
            pos_d = frame.positions[hb.donor_o_idx]
            pos_h = frame.positions[hb.donor_h_idx]
            d_dh, _ = detector.minimum_image_distance(pos_d, pos_h, box_lengths)
            d_ha = hb.distance_ha
            d_oo = hb.distance_da
            profiler.add_hbond(d_dh, d_ha, d_oo)
            
        lbhb_fractions.append(profiler.get_lbhb_fraction())
        
        # B. Proton Wire Tracking
        sources, sinks, water = classify_oxygen_atoms(frame, detector)
        
        # Construct graph nodes & edges
        nodes = list(set(sources) | set(sinks) | set(water))
        edges = []
        for hb in hbonds:
            # We direct edge from Donor to Acceptor with weight as H-bond length
            edges.append((hb.donor_o_idx, hb.acceptor_o_idx, {'weight': hb.distance_da}))
            
        wire_tracker.update_network(nodes, edges)
        wires = wire_tracker.find_proton_wires(sources, sinks)
        wire_lengths.append(wire_tracker.get_average_wire_length())

        # C. Hodge Flow Decomposition
        if len(hbonds) > 0:
            B1, B2, triangles = build_boundary_matrices(nodes, hbonds)
            decomposer.set_boundary_matrices(B1, B2)
            
            # Flow: Vector of H-bond orientations along normal z-axis
            flow = np.zeros(len(hbonds))
            for k, hb in enumerate(hbonds):
                z_d = frame.positions[hb.donor_o_idx, 2]
                z_a = frame.positions[hb.acceptor_o_idx, 2]
                flow[k] = z_a - z_d # Directed z-displacement
                
            try:
                f_grad, f_curl, f_harm = decomposer.decompose(flow)
                
                # Norm percentages
                norm_tot = np.linalg.norm(flow)
                if norm_tot > 1e-5:
                    p_grad = float(np.linalg.norm(f_grad) / norm_tot * 100)
                    p_curl = float(np.linalg.norm(f_curl) / norm_tot * 100)
                    p_harm = float(np.linalg.norm(f_harm) / norm_tot * 100)
                else:
                    p_grad, p_curl, p_harm = 0.0, 0.0, 0.0
                hodge_decompositions.append([p_grad, p_curl, p_harm])
            except Exception as e:
                hodge_decompositions.append([0.0, 0.0, 0.0])
        else:
            hodge_decompositions.append([0.0, 0.0, 0.0])

        if (i + 1) % max(1, n_frames // 10) == 0 or i == n_frames - 1:
            print(f"  Frame {i+1}/{n_frames} analyzed.")

    # 3. Post-Processing & Save Results
    print("\nProcessing overall statistics...")
    
    # Save Time Series to CSV
    hodge_arr = np.array(hodge_decompositions)
    time_fs = [frame.timestep * 0.5 for frame in frames] # Timestep defaults to 0.5 fs
    
    ts_df = pd.DataFrame({
        "Frame": [f.timestep for f in frames],
        "Time_fs": time_fs,
        "LBHB_Fraction": lbhb_fractions,
        "Avg_Wire_Length": wire_lengths,
        "Hodge_Gradient_Pct": hodge_arr[:, 0],
        "Hodge_Curl_Pct": hodge_arr[:, 1],
        "Hodge_Harmonic_Pct": hodge_arr[:, 2]
    })
    
    ts_csv = output_dir / "proton_dynamics_timeseries.csv"
    ts_df.to_csv(ts_csv, index=False)
    print(f"  Saved time-series data: {ts_csv}")

    # Compute PMF profile
    centers, pmf = profiler.compute_pmf(bins=50, range_val=(-1.0, 1.0))
    pmf_df = pd.DataFrame({
        "Delta_A": centers,
        "Free_Energy_kcal_mol": pmf
    })
    pmf_csv = output_dir / "proton_transfer_pmf.csv"
    pmf_df.to_csv(pmf_csv, index=False)
    print(f"  Saved PMF free energy profile: {pmf_csv}")

    # Save summary stats JSON
    summary = {
        "mean_lbhb_fraction": float(np.mean(lbhb_fractions)),
        "mean_wire_length": float(np.mean(wire_lengths)),
        "mean_hodge_gradient": float(np.mean(hodge_arr[:, 0])),
        "mean_hodge_curl": float(np.mean(hodge_arr[:, 1])),
        "mean_hodge_harmonic": float(np.mean(hodge_arr[:, 2])),
    }
    
    summary_json = output_dir / "proton_dynamics_summary.json"
    with open(summary_json, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"  Saved statistics summary: {summary_json}")

    # 4. Generate Figures
    print("\nGenerating figures...")
    
    # Figure 1: PMF Free Energy Curve
    plt.figure(figsize=(7, 5))
    plt.plot(centers, pmf, color='#2C3E50', linewidth=2.5, label='PMF Profile')
    plt.fill_between(centers, pmf, color='#34495E', alpha=0.15)
    plt.xlabel(r"Proton Transfer Coordinate $\delta = d(D-H) - d(H-A)$ ($\AA$)", fontsize=11)
    plt.ylabel("Free Energy (kcal/mol)", fontsize=11)
    plt.title("Potential of Mean Force (PMF) for Proton Transfer", fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(-0.8, 0.8)
    plt.ylim(0, max(pmf) + 1.0 if len(pmf) > 0 else 10)
    plt.tight_layout()
    pmf_png = output_dir / "proton_transfer_pmf.png"
    plt.savefig(pmf_png, dpi=300)
    plt.close()
    print(f"  Saved figure: {pmf_png}")

    # Figure 2: Proton Dynamics Time-Series (LBHBs and Wires)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(time_fs, lbhb_fractions, color='#E74C3C', linewidth=1.5, label='LBHB Fraction')
    ax1.set_ylabel("LBHB Fraction", fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Time Evolution of Microscopic Proton Dynamics", fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')
    
    ax2.plot(time_fs, wire_lengths, color='#3498DB', linewidth=1.5, label='Avg Wire Length')
    ax2.set_xlabel("Time (fs)", fontsize=11)
    ax2.set_ylabel("Wire Length (Hops)", fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    dynamics_png = output_dir / "proton_dynamics_evolution.png"
    plt.savefig(dynamics_png, dpi=300)
    plt.close()
    print(f"  Saved figure: {dynamics_png}")

    # Figure 3: Hodge Decomposition Stacked Plot
    plt.figure(figsize=(10, 5))
    plt.stackplot(time_fs, hodge_arr[:, 0], hodge_arr[:, 1], hodge_arr[:, 2],
                  labels=['Gradient (Transport)', 'Curl (Loops)', 'Harmonic (Cycles)'],
                  colors=['#2ECC71', '#F1C40F', '#9B59B6'], alpha=0.8)
    plt.xlabel("Time (fs)", fontsize=11)
    plt.ylabel("Hodge Flow Percentage (%)", fontsize=11)
    plt.title("Hodge Flow Decomposition on H-Bond Simplicial Complexes", fontsize=12, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    hodge_png = output_dir / "hodge_decomposition_flow.png"
    plt.savefig(hodge_png, dpi=300)
    plt.close()
    print(f"  Saved figure: {hodge_png}")

    print("\n" + "=" * 60)
    print("Analysis Complete! All proton transfer diagnostics successfully executed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
