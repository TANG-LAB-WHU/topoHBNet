#!/usr/bin/env python3
"""
This script demonstrates comprehensive hydrogen bond network analysis from
CP2K AIMD XYZ trajectory files using the hbond_topology package.

Features:
- Basic H-bond detection and counting
- Topological invariants (Betti-0, Betti-1, Betti-2, Euler characteristic)
- H-bond lifetime and autocorrelation analysis
- Coordination, degree, and clustering distributions
- Radial distribution functions (RDF) for multiple species
- H-bond strength classification
- Persistent homology barcode and diagrams (TDA)
- Topological Machine Learning (Embedding, TNN feature extraction, PCA)

Usage:
    python topoHBNet_main_analysis.py                        # Use default parameters
    python topoHBNet_main_analysis.py --run-ml               # Run with topological ML
    python topoHBNet_main_analysis.py --sample-interval 5    # Analyze every 5 frames

Output Files:
- analysis_results.json: Per-frame analysis data
- statistics_summary.json: Overall statistics (includes TML data)
- hbond_dynamics.png, betti_dynamics.png: Time-series analysis plots
- hbond_distributions.png, coordination_degree.png: Statistical distributions
- hbond_lifetime.png, autocorrelation.png: Dynamical properties
- rdf_*.png: Radial distribution functions for species pairs
- clustering_strength.png: Clustering and H-bond strength classification
- persistence_barcode.png, persistence_diagram.png: TDA visualizations
- similarity_heatmap.png, embedding_pca.png, pca_time_series.png: TML visualizations
- frame_embeddings.npy, tnn_features.npy: Raw topological ML features
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional, Union
from collections import defaultdict

import numpy as np

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from hbond_topology import (
    HBondDetector,
    HBondComplexBuilder,
    TopologicalInvariants,
)
from hbond_topology.analysis import (
    plot_persistence_barcode,
    plot_persistence_diagram,
)
from hbond_topology.io.trajectory_parser import TrajectoryParser, Frame
from hbond_topology.embedding import HBondEmbedder
from hbond_topology.learning import HBondTNN, prepare_tnn_data

# Check for optional dependencies
HAS_GUDHI = False
try:
    import gudhi
    HAS_GUDHI = True
except ImportError:
    pass

HAS_SCIPY = False
try:
    import scipy.stats
    import scipy.signal
    HAS_SCIPY = True
except ImportError:
    pass


class _Tee:
    """Write to multiple streams (e.g. stdout and a log file)."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='CP2K AIMD H-bond Topology Analysis (Extended)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Trajectory parameters
    parser.add_argument('--trajectory', '-t', type=str, default='trajectory.xyz',
                        help='Path to trajectory file')
    parser.add_argument('--timestep', type=float, default=0.5,
                        help='MD timestep in femtoseconds')
    parser.add_argument('--sample-interval', type=int, default=1,
                        help='Analyze every N frames')
    parser.add_argument('--cell-file', type=str, default='trajectory.cell',
                        help='Path to CP2K cell file (.cell)')
    
    # H-bond detection criteria
    parser.add_argument('--r-da-max', type=float, default=3.5,
                        help='Max donor-acceptor distance (Angstrom)')
    parser.add_argument('--r-ha-max', type=float, default=2.5,
                        help='Max hydrogen-acceptor distance (Angstrom)')
    parser.add_argument('--angle-min', type=float, default=120.0,
                        help='Min D-H-A angle (degrees)')
    
    # Output settings
    parser.add_argument('--dpi', type=int, default=600,
                        help='Figure DPI')
    parser.add_argument('--output-dir', '-o', type=str, default='results',
                        help='Output directory')
    parser.add_argument('--output-dir-rawdata', type=str, default='raw_data_csv',
                        help='Output directory for raw data in CSV format')
    
    # Machine Learning parameters
    parser.add_argument('--run-ml', action='store_true',
                        help='Run topological machine learning analysis')
    parser.add_argument('--ml-dim', type=int, default=32,
                        help='Embedding/Hidden dimension for ML')
    
    # Persistence homology parameters
    parser.add_argument('--persistence-frame', type=str, default='all',
                        help='Frame for persistence diagram: "all" (default), "middle", "first", "last", or integer index')
    parser.add_argument('--persistence-barcode-legend-loc', type=str, default='upper left',
                        help='Legend position for persistence barcode: e.g. "upper right", "lower left"')
    parser.add_argument('--persistence-diagram-legend-loc', type=str, default='lower right',
                        help='Legend position for persistence diagram: e.g. "lower right", "upper left"')
    parser.add_argument('--persistence-dynamics-legend-loc', type=str, default='upper right',
                        help='Legend position for persistence_dynamics subplots: e.g. "upper right", "lower left"')
    parser.add_argument('--persistence-barcode-legend-fontsize', type=float, default=None,
                        help='Legend font size for persistence barcode (e.g. 10, 12). Default: matplotlib default')
    parser.add_argument('--persistence-diagram-legend-fontsize', type=float, default=None,
                        help='Legend font size for persistence diagram (e.g. 10, 12). Default: matplotlib default')
    parser.add_argument('--persistence-dynamics-legend-fontsize', type=float, default=None,
                        help='Legend font size for persistence_dynamics (e.g. 10, 12). Default: matplotlib default')
    
    import equilibration_utils
    parser = equilibration_utils.add_equilibration_args(parser)
    return parser.parse_args()


# =============================================================================
# Core Analysis Functions
# =============================================================================

def analyze_frame(frame: Frame, detector: HBondDetector, builder: HBondComplexBuilder, 
                  invariants: TopologicalInvariants) -> Dict:
    """Perform full analysis on a single frame."""
    hbonds = detector.detect_hbonds(frame)
    
    # Build H-bond set for tracking
    hbond_set = set()
    for hb in hbonds:
        # Use sorted tuple for undirected edge
        hbond_set.add(tuple(sorted([hb.donor_o_idx, hb.acceptor_o_idx])))
    
    result = {
        'timestep': frame.timestep,
        'n_hbonds': len(hbonds),
        'hbond_set': hbond_set,
        'hbonds': hbonds,
        'distances_da': [hb.distance_da for hb in hbonds],
        'distances_ha': [hb.distance_ha for hb in hbonds],
        'angles_dha': [hb.angle_dha for hb in hbonds],
        'betti_0': 0,
        'betti_1': 0,
        'betti_2': 0,
        'euler_char': 0,
    }
    
    if len(hbonds) > 0:
        try:
            sc = builder.build_from_frame(frame, hbonds)
            inv = invariants.compute_all_invariants(sc)
            result['betti_0'] = inv['betti_numbers'][0]
            result['betti_1'] = inv['betti_numbers'][1] if len(inv['betti_numbers']) > 1 else 0
            result['betti_2'] = inv['betti_numbers'][2] if len(inv['betti_numbers']) > 2 else 0
            result['euler_char'] = inv['euler_characteristic']
        except Exception as e:
            # Note: We don't want to crash the whole analysis if one frame fails
            # but we should at least know it happened.
            if 'sc' in locals():
                print(f"    Warning: Invariant computation failed for frame {frame.timestep}: {e}")
    
    return result


# =============================================================================
# Advanced Analysis Functions
# =============================================================================

def compute_coordination_numbers(results: List[Dict]) -> Dict:
    """
    Compute coordination number distribution.
    Coordination number = number of H-bonds per water molecule.
    """
    all_coordination = []
    raw_records = []
    
    for r in results:
        f_idx = r.get('timestep', 0)
        # Count how many H-bonds each oxygen participates in
        coord_count = defaultdict(int)
        for hb in r['hbonds']:
            coord_count[hb.donor_o_idx] += 1
            coord_count[hb.acceptor_o_idx] += 1
        
        # Collect all coordination numbers
        for atom_idx, count in coord_count.items():
            all_coordination.append(count)
            raw_records.append({
                'frame_idx': f_idx,
                'atom_idx': atom_idx,
                'coordination_number': count
            })
    
    if not all_coordination:
        return {'mean': 0, 'std': 0, 'distribution': {}, 'raw_data': [], 'raw_records': []}
    
    # Distribution
    unique, counts = np.unique(all_coordination, return_counts=True)
    distribution = {int(k): int(v) for k, v in zip(unique, counts)}
    
    return {
        'mean': float(np.mean(all_coordination)),
        'std': float(np.std(all_coordination)),
        'distribution': distribution,
        'raw_data': all_coordination,
        'raw_records': raw_records
    }


def compute_degree_distribution(results: List[Dict]) -> Dict:
    """
    Compute node degree distribution of H-bond network.
    Degree = number of connections per node (oxygen atom).
    """
    all_degrees = []
    raw_records = []
    
    for r in results:
        f_idx = r.get('timestep', 0)
        degree_count = defaultdict(int)
        for hb in r['hbonds']:
            degree_count[hb.donor_o_idx] += 1
            degree_count[hb.acceptor_o_idx] += 1
        
        for atom_idx, count in degree_count.items():
            all_degrees.append(count)
            raw_records.append({
                'frame_idx': f_idx,
                'atom_idx': atom_idx,
                'degree': count
            })
    
    if not all_degrees:
        return {'mean': 0, 'std': 0, 'distribution': {}, 'raw_data': [], 'raw_records': []}
    
    unique, counts = np.unique(all_degrees, return_counts=True)
    distribution = {int(k): int(v) for k, v in zip(unique, counts)}
    
    return {
        'mean': float(np.mean(all_degrees)),
        'std': float(np.std(all_degrees)),
        'distribution': distribution,
        'raw_data': all_degrees,
        'raw_records': raw_records
    }



def compute_hbond_lifetime(results: List[Dict], timestep_fs: float) -> Dict:
    """
    Compute H-bond lifetime distribution.
    Tracks continuous existence of each H-bond pair across frames.
    """
    if len(results) < 2:
        return {'mean': 0, 'lifetimes': []}
    
    # Track all unique H-bonds ever observed
    all_hbond_pairs = set()
    for r in results:
        all_hbond_pairs.update(r['hbond_set'])
    
    lifetimes = []
    
    for pair in all_hbond_pairs:
        # Find continuous stretches where this pair exists
        exists = [pair in r['hbond_set'] for r in results]
        
        current_lifetime = 0
        for e in exists:
            if e:
                current_lifetime += 1
            else:
                if current_lifetime > 0:
                    lifetimes.append(current_lifetime * timestep_fs)
                current_lifetime = 0
        if current_lifetime > 0:
            lifetimes.append(current_lifetime * timestep_fs)
    
    if not lifetimes:
        return {'mean': 0, 'std': 0, 'max': 0, 'lifetimes': []}
    
    return {
        'mean': float(np.mean(lifetimes)),
        'std': float(np.std(lifetimes)),
        'max': float(np.max(lifetimes)),
        'lifetimes': lifetimes
    }


def compute_autocorrelation(results: List[Dict], max_lag: int = None) -> Dict:
    """
    Compute H-bond existence autocorrelation function C(t).
    C(t) = <h(0)h(t)> / <h(0)^2>
    where h(t) = 1 if H-bond exists at time t, 0 otherwise.
    """
    if len(results) < 2:
        return {'lags': [], 'acf': []}
    
    if max_lag is None:
        max_lag = min(len(results) // 2, 100)
    
    # Get all unique H-bond pairs
    all_pairs = set()
    for r in results:
        all_pairs.update(r['hbond_set'])
    
    if not all_pairs:
        return {'lags': [], 'acf': []}
    
    # Build existence matrix: (n_pairs, n_frames)
    pair_list = list(all_pairs)
    n_pairs = len(pair_list)
    n_frames = len(results)
    
    existence = np.zeros((n_pairs, n_frames), dtype=float)
    for t, r in enumerate(results):
        for i, pair in enumerate(pair_list):
            if pair in r['hbond_set']:
                existence[i, t] = 1.0
    
    # Compute autocorrelation
    acf = []
    lags = list(range(max_lag))
    
    for lag in lags:
        if lag >= n_frames:
            break
        # C(lag) = mean over all pairs and times of h(t)*h(t+lag)
        numerator = 0
        denominator = 0
        for i in range(n_pairs):
            for t in range(n_frames - lag):
                numerator += existence[i, t] * existence[i, t + lag]
                denominator += existence[i, t] * existence[i, t]
        
        if denominator > 0:
            acf.append(numerator / denominator)
        else:
            acf.append(0)
    
    return {
        'lags': lags[:len(acf)],
        'acf': acf
    }


def compute_clustering_coefficient(results: List[Dict]) -> Dict:
    """
    Compute network clustering coefficient for each frame.
    C = (3 * number of triangles) / (number of connected triples)
    """
    clustering_coeffs = []
    
    for r in results:
        if len(r['hbonds']) < 3:
            clustering_coeffs.append(0.0)
            continue
        
        # Build adjacency from H-bonds
        neighbors = defaultdict(set)
        for hb in r['hbonds']:
            neighbors[hb.donor_o_idx].add(hb.acceptor_o_idx)
            neighbors[hb.acceptor_o_idx].add(hb.donor_o_idx)
        
        # Count triangles and connected triples
        triangles = 0
        triples = 0
        
        for node in neighbors:
            node_neighbors = list(neighbors[node])
            k = len(node_neighbors)
            if k < 2:
                continue
            
            # Count pairs of neighbors that are connected (triangles)
            for i in range(k):
                for j in range(i + 1, k):
                    triples += 1
                    if node_neighbors[j] in neighbors[node_neighbors[i]]:
                        triangles += 1
        
        if triples > 0:
            clustering_coeffs.append(triangles / triples)
        else:
            clustering_coeffs.append(0.0)
    
    return {
        'mean': float(np.mean(clustering_coeffs)),
        'std': float(np.std(clustering_coeffs)),
        'per_frame': clustering_coeffs
    }


def compute_rdf(frames: List[Frame], symbol1: str, symbol2: str, r_max: float = 8.0, dr: float = 0.1) -> Dict:
    """
    General Radial Distribution Function g(r) computation for two elements.
    """
    bins = np.arange(0, r_max + dr, dr)
    hist = np.zeros(len(bins) - 1)
    n_frames = len(frames)
    total_n1 = 0
    total_n2 = 0
    
    for frame in frames:
        idx1 = np.where(frame.symbols == symbol1)[0]
        idx2 = np.where(frame.symbols == symbol2)[0]
        
        n1 = len(idx1)
        n2 = len(idx2)
        total_n1 += n1
        total_n2 += n2
        
        if n1 == 0 or n2 == 0:
            continue
            
        pos1 = frame.positions[idx1]
        pos2 = frame.positions[idx2]
        box_lengths = frame.box_lengths
        
        # Calculate all-pairs distances using broadcasting/vectorization if possible
        # For simplicity and to handle PBC, we use a loop but optimized
        for i in range(n1):
            diff = pos2 - pos1[i]
            # Minimum image convention
            diff = diff - box_lengths * np.round(diff / box_lengths)
            dist = np.linalg.norm(diff, axis=1)
            
            # If same species, avoid self-counting
            if symbol1 == symbol2:
                dist = dist[dist > 0.001]
                
            in_range = dist[dist < r_max]
            for d in in_range:
                idx = int(d / dr)
                if idx < len(hist):
                    hist[idx] += 1

    r_centers = (bins[:-1] + bins[1:]) / 2
    if n_frames > 0 and total_n1 > 0 and total_n2 > 0:
        avg_n1 = total_n1 / n_frames
        avg_n2 = total_n2 / n_frames
        avg_vol = np.mean([np.prod(f.box_lengths) for f in frames])
        rho2 = avg_n2 / avg_vol
        
        shell_volumes = 4 * np.pi * r_centers**2 * dr
        # Normalization factor: hist / (n_frames * n1 * rho2 * shell_vol)
        ideal_count = n_frames * avg_n1 * rho2 * shell_volumes
        
        with np.errstate(divide='ignore', invalid='ignore'):
            g_r = hist / ideal_count
            g_r = np.nan_to_num(g_r, nan=0.0, posinf=0.0)
    else:
        g_r = np.zeros_like(r_centers)
        
    return {'r': r_centers.tolist(), 'g_r': g_r.tolist()}


def classify_hbond_strength(results: List[Dict]) -> Dict:
    """
    Classify H-bonds by strength based on D-A distance.
    Strong: D-A < 2.8 Å
    Moderate: 2.8 Å <= D-A < 3.2 Å
    Weak: D-A >= 3.2 Å
    """
    strong = 0
    moderate = 0
    weak = 0
    
    for r in results:
        for d in r['distances_da']:
            if d < 2.8:
                strong += 1
            elif d < 3.2:
                moderate += 1
            else:
                weak += 1
    
    total = strong + moderate + weak
    if total == 0:
        return {
            'strong': 0, 'moderate': 0, 'weak': 0, 'total': 0,
            'strong_pct': 0.0, 'moderate_pct': 0.0, 'weak_pct': 0.0
        }
    
    return {
        'strong': strong,
        'moderate': moderate,
        'weak': weak,
        'total': total,
        'strong_pct': 100 * strong / total,
        'moderate_pct': 100 * moderate / total,
        'weak_pct': 100 * weak / total
    }


def compute_water_hbond_states(results: List[Dict], frames: List[Frame], detector: HBondDetector) -> Dict:
    """
    Compute detailed hydrogen-bonding states (nDmA, free H2O, etc.) for water molecules.
    """
    all_states = []
    state_counts = defaultdict(int)
    raw_records = []
    
    for r, frame in zip(results, frames):
        f_idx = r.get('timestep', 0)
        # Identify water molecules in this frame
        water_mols = detector.identify_water_molecules(frame)
        water_o_indices = {wm.o_idx for wm in water_mols}
        
        # Initialize counts for each water oxygen
        donor_count = {o_idx: 0 for o_idx in water_o_indices}
        acceptor_count = {o_idx: 0 for o_idx in water_o_indices}
        
        # Count donor and acceptor roles for each H-bond in this frame
        for hb in r['hbonds']:
            # Only count H-bonds where the atoms belong to identified water molecules
            if hb.donor_o_idx in water_o_indices:
                donor_count[hb.donor_o_idx] += 1
            if hb.acceptor_o_idx in water_o_indices:
                acceptor_count[hb.acceptor_o_idx] += 1
                
        # Classify the state of each water molecule
        for o_idx in water_o_indices:
            d = donor_count[o_idx]
            a = acceptor_count[o_idx]
            
            if d == 0 and a == 0:
                state = 'free H2O'
            else:
                state = f'{d}D{a}A'
                
            all_states.append(state)
            state_counts[state] += 1
            raw_records.append({
                'frame_idx': int(f_idx),
                'atom_idx': int(o_idx),
                'donor_count': int(d),
                'acceptor_count': int(a),
                'state': state
            })
            
    if not all_states:
        return {'distribution': {}, 'raw_data': [], 'raw_records': []}
        
    # Calculate percentage distribution
    total_water_observations = len(all_states)
    distribution = {}
    for state, count in state_counts.items():
        distribution[state] = {
            'count': int(count),
            'percentage': float(100 * count / total_water_observations)
        }
        
    # Sort distribution by state name (e.g. 1D1A, 1D2A, 2D2A, free H2O)
    sorted_distribution = dict(sorted(distribution.items(), key=lambda x: x[0]))
    
    return {
        'distribution': sorted_distribution,
        'raw_data': all_states,
        'raw_records': raw_records
    }


def _compute_single_frame_persistence(frame: Frame, max_edge_length: float = 5.0) -> Dict:
    """
    Compute persistence for a single frame.
    
    Returns dict with 'H0', 'H1' barcode lists and statistics.
    """
    o_indices = np.where(frame.symbols == 'O')[0]
    if len(o_indices) < 3:
        return {'H0': [], 'H1': [], 'total_persistence_H0': 0, 'total_persistence_H1': 0,
                'n_features_H0': 0, 'n_features_H1': 0}
    
    o_positions = frame.positions[o_indices]
    
    # Build Rips complex on oxygen positions
    rips = gudhi.RipsComplex(points=o_positions, max_edge_length=max_edge_length)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    
    barcodes = {'H0': [], 'H1': []}
    
    for dim, (birth, death) in st.persistence():
        death_val = death if death < float('inf') else max_edge_length
        if dim == 0:
            barcodes['H0'].append([birth, death_val])
        elif dim == 1:
            barcodes['H1'].append([birth, death_val])
    
    # Compute statistics
    h0_lifetimes = [d - b for b, d in barcodes['H0']]
    h1_lifetimes = [d - b for b, d in barcodes['H1']]
    
    return {
        'H0': barcodes['H0'],
        'H1': barcodes['H1'],
        'total_persistence_H0': sum(h0_lifetimes) if h0_lifetimes else 0,
        'total_persistence_H1': sum(h1_lifetimes) if h1_lifetimes else 0,
        'n_features_H0': len(barcodes['H0']),
        'n_features_H1': len(barcodes['H1']),
        'mean_lifetime_H0': np.mean(h0_lifetimes) if h0_lifetimes else 0,
        'mean_lifetime_H1': np.mean(h1_lifetimes) if h1_lifetimes else 0,
    }


def compute_persistent_homology(results: List[Dict], frames: List[Frame], 
                                 frame_selection: str = 'middle') -> Dict:
    """
    Compute persistent homology using GUDHI (if available).
    
    Persistence diagrams/barcodes are computed for point clouds (oxygen positions).
    
    Parameters
    ----------
    results : List[Dict]
        Analysis results for each frame.
    frames : List[Frame]
        List of trajectory frames (sampled).
    frame_selection : str
        Which frame(s) to use for persistence:
        - 'all': ALL frames (default; computes persistence for each frame, returns time series)
        - 'middle': middle frame
        - 'first': first frame
        - 'last': last frame
        - integer string (e.g., '100'): specific frame index
    
    Returns
    -------
    Dict with keys:
        - 'available': bool
        - 'frame_index': int (0-based index of representative frame for barcode plot)
        - 'total_frames': int (total number of frames)
        - 'barcodes': dict with 'H0' and 'H1' lists (for representative frame)
        - 'all_frames': bool (True if all frames were analyzed)
        - 'dynamics': dict (only if all_frames=True) with time series of persistence stats
    """
    if not HAS_GUDHI:
        return {'available': False, 'message': 'GUDHI not installed'}
    
    total_frames = len(frames)
    
    # Handle 'all' frames mode
    if frame_selection == 'all':
        print(f"        Computing persistence for all {total_frames} frames...")
        
        # Initialize time series arrays
        dynamics = {
            'total_persistence_H0': [],
            'total_persistence_H1': [],
            'n_features_H0': [],
            'n_features_H1': [],
            'mean_lifetime_H0': [],
            'mean_lifetime_H1': [],
        }
        
        all_barcodes = []
        
        for i, frame in enumerate(frames):
            result = _compute_single_frame_persistence(frame)
            all_barcodes.append({'H0': result['H0'], 'H1': result['H1']})
            
            dynamics['total_persistence_H0'].append(result['total_persistence_H0'])
            dynamics['total_persistence_H1'].append(result['total_persistence_H1'])
            dynamics['n_features_H0'].append(result['n_features_H0'])
            dynamics['n_features_H1'].append(result['n_features_H1'])
            dynamics['mean_lifetime_H0'].append(result['mean_lifetime_H0'])
            dynamics['mean_lifetime_H1'].append(result['mean_lifetime_H1'])
            
            if (i + 1) % 100 == 0:
                print(f"            Processed {i + 1}/{total_frames} frames...")
        
        # Convert to numpy arrays
        for key in dynamics:
            dynamics[key] = np.array(dynamics[key])
        
        # Use middle frame for representative barcode plot
        mid_idx = total_frames // 2
        
        return {
            'available': True,
            'all_frames': True,
            'frame_index': mid_idx,
            'total_frames': total_frames,
            'barcodes': all_barcodes[mid_idx],
            'dynamics': dynamics,
            'all_barcodes': all_barcodes,  # Keep all for potential further analysis
        }
    
    # Single frame mode
    if frame_selection == 'middle':
        frame_idx = total_frames // 2
    elif frame_selection == 'first':
        frame_idx = 0
    elif frame_selection == 'last':
        frame_idx = total_frames - 1
    else:
        # Try to parse as integer
        try:
            frame_idx = int(frame_selection)
            if frame_idx < 0 or frame_idx >= total_frames:
                print(f"    Warning: frame index {frame_idx} out of range [0, {total_frames-1}], using middle frame")
                frame_idx = total_frames // 2
        except ValueError:
            print(f"    Warning: invalid frame_selection '{frame_selection}', using middle frame")
            frame_idx = total_frames // 2
    
    result = _compute_single_frame_persistence(frames[frame_idx])
    
    return {
        'available': True,
        'all_frames': False,
        'frame_index': frame_idx,
        'total_frames': total_frames,
        'barcodes': {'H0': result['H0'], 'H1': result['H1']}
    }


# =============================================================================
# Visualization Functions
# =============================================================================

# Light Premium Color Palette
COLORS = {
    'blue_soft': '#5DADE2',    # Time series main
    'blue_fill': '#5DADE2',    # Fill with alpha
    'red_soft': '#F5B7B1',     # Means / fits
    'red_fill': '#F5B7B1',
    'green_soft': '#82E0AA',   # Betti 0 / dist
    'purple_soft': '#AF7AC5',  # Betti 2 / degree
    'teal_soft': '#76D7C4',    # Coordination
    'orange_soft': '#F5CBA7',  # Lifetime
    'gray_grid': '#EBEDEF',
    'pie': ['#82E0AA', '#F5CBA7', '#F1948A'] # Green, Orange, Red soft
}


def plot_persistence_dynamics(dynamics: Dict, timestep_fs: float, sample_interval: int,
                               save_path: Path, dpi: int = 600,
                               legend_loc: str = 'upper right',
                               legend_fontsize: Optional[float] = None):
    """
    Plot persistence dynamics over time (all frames analysis).
    
    Creates a 2x2 subplot showing:
    - Total persistence (H0 and H1) over time
    - Number of features (H0 and H1) over time
    - Mean lifetime (H0 and H1) over time
    - Persistence ratio H1/H0 over time
    
    Parameters
    ----------
    dynamics : Dict
        Dictionary with time series arrays for persistence statistics.
    timestep_fs : float
        MD timestep in femtoseconds.
    sample_interval : int
        Sample interval (frames between samples).
    save_path : Path
        Path to save the figure.
    dpi : int
        Figure resolution.
    legend_loc : str
        Legend position for all subplots (e.g. 'upper right', 'lower left').
    legend_fontsize : float, optional
        Legend font size. If None, use matplotlib default.
    """
    import matplotlib.pyplot as plt
    
    n_frames = len(dynamics['total_persistence_H0'])
    times = np.arange(n_frames) * sample_interval * timestep_fs  # Time in fs
    
    legend_kw = {'frameon': False, 'loc': legend_loc}
    if legend_fontsize is not None:
        legend_kw['fontsize'] = legend_fontsize
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Persistence Dynamics (All Frames)', fontsize=14, fontweight='bold', color='#2C3E50')
    
    # 1. Total persistence over time
    ax = axes[0, 0]
    ax.plot(times, dynamics['total_persistence_H0'], color=COLORS['green_soft'], 
            linewidth=1.5, label='H0 (components)', alpha=0.8)
    ax.plot(times, dynamics['total_persistence_H1'], color=COLORS['orange_soft'], 
            linewidth=1.5, label='H1 (loops)', alpha=0.8)
    ax.set_xlabel('Time (fs)', fontsize=11)
    ax.set_ylabel('Total Persistence (Å)', fontsize=11)
    ax.set_title('Total Persistence Over Time', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.legend(**legend_kw)
    ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # 2. Number of features over time
    ax = axes[0, 1]
    ax.plot(times, dynamics['n_features_H0'], color=COLORS['green_soft'], 
            linewidth=1.5, label='H0 (components)', alpha=0.8)
    ax.plot(times, dynamics['n_features_H1'], color=COLORS['orange_soft'], 
            linewidth=1.5, label='H1 (loops)', alpha=0.8)
    ax.set_xlabel('Time (fs)', fontsize=11)
    ax.set_ylabel('Number of Features', fontsize=11)
    ax.set_title('Topological Feature Count Over Time', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.legend(**legend_kw)
    ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # 3. Mean lifetime over time
    ax = axes[1, 0]
    ax.plot(times, dynamics['mean_lifetime_H0'], color=COLORS['green_soft'], 
            linewidth=1.5, label='H0 (components)', alpha=0.8)
    ax.plot(times, dynamics['mean_lifetime_H1'], color=COLORS['orange_soft'], 
            linewidth=1.5, label='H1 (loops)', alpha=0.8)
    ax.set_xlabel('Time (fs)', fontsize=11)
    ax.set_ylabel('Mean Lifetime (Å)', fontsize=11)
    ax.set_title('Mean Feature Lifetime Over Time', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.legend(**legend_kw)
    ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # 4. H1/H0 ratio (loop complexity relative to connectivity)
    ax = axes[1, 1]
    # Avoid division by zero
    h0_total = dynamics['total_persistence_H0']
    h1_total = dynamics['total_persistence_H1']
    ratio = np.divide(h1_total, h0_total, out=np.zeros_like(h1_total), where=h0_total > 0)
    ax.plot(times, ratio, color=COLORS['purple_soft'], linewidth=1.5, alpha=0.8)
    ax.axhline(y=np.mean(ratio), color=COLORS['red_soft'], linestyle='--', 
               linewidth=1.5, label=f'Mean: {np.mean(ratio):.3f}')
    ax.set_xlabel('Time (fs)', fontsize=11)
    ax.set_ylabel('H1/H0 Persistence Ratio', fontsize=11)
    ax.set_title('Loop-to-Component Persistence Ratio', fontsize=12, fontweight='bold', color='#2C3E50')
    ax.legend(**legend_kw)
    ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
    fig.savefig(Path(save_path).with_suffix('.svg'), format='svg', bbox_inches='tight')
    plt.close(fig)


def generate_basic_plots(results: List[Dict], output_dir: Path, timestep_fs: float, dpi: int):
    """Generate basic visualization plots."""
    import matplotlib.pyplot as plt
    sns = None
    try:
        import seaborn as sns
    except ImportError:
        pass
    
    # Correct time calculation: r['timestep'] is the absolute frame index
    times = [r['timestep'] * timestep_fs for r in results]
    n_hbonds = [r['n_hbonds'] for r in results]
    betti_0 = [r['betti_0'] for r in results]
    betti_1 = [r['betti_1'] for r in results]
    betti_2 = [r['betti_2'] for r in results]
    
    all_distances_da = []
    all_distances_ha = []
    all_angles = []
    for r in results:
        all_distances_da.extend(r['distances_da'])
        all_distances_ha.extend(r['distances_ha'])
        all_angles.extend(r['angles_dha'])
    
    # Modern clean style
    plt.style.use('seaborn-v0_8-ticks')
    try:
        sns.set_context("notebook", font_scale=1.1)
    except:
        pass
    
    # 1. H-bond Dynamics with Gradient Fill
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, n_hbonds, color=COLORS['blue_soft'], linewidth=2, alpha=0.9)
    ax.fill_between(times, n_hbonds, color=COLORS['blue_fill'], alpha=0.2)
    ax.set_xlabel('Simulation time (fs)', fontsize=12)
    ax.set_ylabel('Number of H-bonds', fontsize=12)
    ax.set_title('Hydrogen Bond Network Dynamics', fontsize=14, fontweight='bold', color='#2C3E50')
    ax.grid(True, color=COLORS['gray_grid'], alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_dir / "hbond_dynamics.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "hbond_dynamics.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: hbond_dynamics.png, hbond_dynamics.svg")
    
    # 2. Betti Number Dynamics
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    # Beta 0 (Components) - Green
    axes[0].plot(times, betti_0, color=COLORS['green_soft'], linewidth=2, label=r'$\beta_0$ (components)')
    axes[0].fill_between(times, betti_0, color=COLORS['green_soft'], alpha=0.2)
    axes[0].set_ylabel(r'$\beta_0$', fontsize=12)
    axes[0].legend(loc='upper right', frameon=False)
    axes[0].set_title('Topological Invariants Dynamics', fontsize=14, fontweight='bold', color='#2C3E50')
    axes[0].grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # Beta 1 (Loops) - Red/Orange (using soft red here for distinction)
    axes[1].plot(times, betti_1, color='#F1948A', linewidth=2, label=r'$\beta_1$ (loops)')
    axes[1].fill_between(times, betti_1, color='#F1948A', alpha=0.2)
    axes[1].set_ylabel(r'$\beta_1$', fontsize=12)
    axes[1].legend(loc='upper right', frameon=False)
    axes[1].grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # Beta 2 (Voids) - Purple
    axes[2].plot(times, betti_2, color=COLORS['purple_soft'], linewidth=2, label=r'$\beta_2$ (voids)')
    axes[2].fill_between(times, betti_2, color=COLORS['purple_soft'], alpha=0.2)
    axes[2].set_xlabel('Simulation time (fs)', fontsize=12)
    axes[2].set_ylabel(r'$\beta_2$', fontsize=12)
    axes[2].legend(loc='upper right', frameon=False)
    axes[2].grid(True, color=COLORS['gray_grid'], alpha=0.5)

    fig.tight_layout()
    fig.savefig(output_dir / "betti_dynamics.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "betti_dynamics.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: betti_dynamics.png, betti_dynamics.svg")
    
    # 3. H-bond Distributions
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    if all_distances_da:
        axes[0].hist(all_distances_da, bins=50, color='#85C1E9', edgecolor='white', alpha=0.8, density=True)
        if sns is not None:
            try:
                sns.kdeplot(all_distances_da, ax=axes[0], color='#2874A6', linewidth=2)
            except Exception as e:
                print(f"    Warning: KDE plot failed for D-A distance: {e}")
        axes[0].axvline(np.mean(all_distances_da), color='#E74C3C', linestyle=':', label=f'Mean: {np.mean(all_distances_da):.2f} A')
        axes[0].set_xlabel('D-A Distance (angstrom)', fontsize=12)
        axes[0].set_ylabel('Density', fontsize=12)
        axes[0].set_title('Donor-Acceptor Distance', fontsize=12, fontweight='bold', color='#2C3E50')
        axes[0].legend(frameon=False)
        axes[0].grid(False)
    
    if all_distances_ha:
        axes[1].hist(all_distances_ha, bins=50, color='#F8C471', edgecolor='white', alpha=0.8, density=True)
        if sns is not None:
            try:
                sns.kdeplot(all_distances_ha, ax=axes[1], color='#D35400', linewidth=2)
            except Exception as e:
                print(f"    Warning: KDE plot failed for H-A distance: {e}")
        axes[1].axvline(np.mean(all_distances_ha), color='#E74C3C', linestyle=':', label=f'Mean: {np.mean(all_distances_ha):.2f} A')
        axes[1].set_xlabel('H-A Distance (angstrom)', fontsize=12)
        axes[1].set_ylabel('Density', fontsize=12)
        axes[1].set_title('Hydrogen-Acceptor Distance', fontsize=12, fontweight='bold', color='#2C3E50')
        axes[1].legend(frameon=False)
        axes[1].grid(False)
    
    if all_angles:
        axes[2].hist(all_angles, bins=50, color='#82E0AA', edgecolor='white', alpha=0.8, density=True)
        if sns is not None:
            try:
                sns.kdeplot(all_angles, ax=axes[2], color='#229954', linewidth=2)
            except Exception as e:
                print(f"    Warning: KDE plot failed for H-bond angle: {e}")
        axes[2].axvline(np.mean(all_angles), color='#E74C3C', linestyle=':', label=f'Mean: {np.mean(all_angles):.1f} deg')
        axes[2].set_xlabel('D-H-A Angle (deg)', fontsize=12)
        axes[2].set_ylabel('Density', fontsize=12)
        axes[2].set_title('H-bond Angle', fontsize=12, fontweight='bold', color='#2C3E50')
        axes[2].legend(frameon=False)
        axes[2].grid(False)
    
    fig.suptitle('Hydrogen Bond Geometry Distributions', fontsize=14, fontweight='bold', color='#2C3E50', y=1.05)
    fig.tight_layout()
    fig.savefig(output_dir / "hbond_distributions.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "hbond_distributions.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: hbond_distributions.png, hbond_distributions.svg")
    
    # =========================================================================
    # Log distribution shape summary (mean, std, median, IQR, skewness, peaks)
    # =========================================================================
    print("\n    === H-bond Geometry Distribution Summary ===")
    
    # D-A Distance
    if all_distances_da and len(all_distances_da) >= 10:
        n_da = len(all_distances_da)
        mean_da = np.mean(all_distances_da)
        std_da = np.std(all_distances_da)
        med_da = np.percentile(all_distances_da, 50)
        p25_da, p75_da = np.percentile(all_distances_da, [25, 75])
        
        # Skewness and peak detection (if scipy available)
        skew_da = scipy.stats.skew(all_distances_da) if HAS_SCIPY else None
        n_peak_da, peak_pos_da, main_peak_da = 0, [], None
        if HAS_SCIPY:
            try:
                kde_da = scipy.stats.gaussian_kde(all_distances_da)
                x_grid = np.linspace(min(all_distances_da), max(all_distances_da), 300)
                pdf_da = kde_da(x_grid)
                peaks_idx, _ = scipy.signal.find_peaks(pdf_da, prominence=0.01 * np.max(pdf_da))
                n_peak_da = len(peaks_idx)
                if n_peak_da:
                    peak_pos_da = x_grid[peaks_idx]
                    main_peak_da = peak_pos_da[np.argmax(pdf_da[peaks_idx])]
            except Exception:
                pass
        
        print(f"    [D-A Distance]")
        print(f"      Samples: {n_da:,}")
        print(f"      Mean / Median / Std: {mean_da:.3f} / {med_da:.3f} / {std_da:.3f} Å")
        print(f"      25% / 75% (IQR): {p25_da:.3f} / {p75_da:.3f} Å")
        if skew_da is not None:
            print(f"      Skewness: {skew_da:.3f}")
        if n_peak_da:
            peaks_str = ", ".join(f"{p:.3f}" for p in sorted(peak_pos_da))
            print(f"      KDE Peaks: {n_peak_da} (main={main_peak_da:.3f} Å; all=[{peaks_str}] Å)")
    
    # H-A Distance
    if all_distances_ha and len(all_distances_ha) >= 10:
        n_ha = len(all_distances_ha)
        mean_ha = np.mean(all_distances_ha)
        std_ha = np.std(all_distances_ha)
        med_ha = np.percentile(all_distances_ha, 50)
        p25_ha, p75_ha = np.percentile(all_distances_ha, [25, 75])
        
        skew_ha = scipy.stats.skew(all_distances_ha) if HAS_SCIPY else None
        n_peak_ha, peak_pos_ha, main_peak_ha = 0, [], None
        if HAS_SCIPY:
            try:
                kde_ha = scipy.stats.gaussian_kde(all_distances_ha)
                x_grid = np.linspace(min(all_distances_ha), max(all_distances_ha), 300)
                pdf_ha = kde_ha(x_grid)
                peaks_idx, _ = scipy.signal.find_peaks(pdf_ha, prominence=0.01 * np.max(pdf_ha))
                n_peak_ha = len(peaks_idx)
                if n_peak_ha:
                    peak_pos_ha = x_grid[peaks_idx]
                    main_peak_ha = peak_pos_ha[np.argmax(pdf_ha[peaks_idx])]
            except Exception:
                pass
        
        print(f"    [H-A Distance]")
        print(f"      Samples: {n_ha:,}")
        print(f"      Mean / Median / Std: {mean_ha:.3f} / {med_ha:.3f} / {std_ha:.3f} Å")
        print(f"      25% / 75% (IQR): {p25_ha:.3f} / {p75_ha:.3f} Å")
        if skew_ha is not None:
            print(f"      Skewness: {skew_ha:.3f}")
        if n_peak_ha:
            peaks_str = ", ".join(f"{p:.3f}" for p in sorted(peak_pos_ha))
            print(f"      KDE Peaks: {n_peak_ha} (main={main_peak_ha:.3f} Å; all=[{peaks_str}] Å)")
    
    # D-H-A Angle
    if all_angles and len(all_angles) >= 10:
        n_ang = len(all_angles)
        mean_ang = np.mean(all_angles)
        std_ang = np.std(all_angles)
        med_ang = np.percentile(all_angles, 50)
        p25_ang, p75_ang = np.percentile(all_angles, [25, 75])
        
        skew_ang = scipy.stats.skew(all_angles) if HAS_SCIPY else None
        n_peak_ang, peak_pos_ang, main_peak_ang = 0, [], None
        if HAS_SCIPY:
            try:
                kde_ang = scipy.stats.gaussian_kde(all_angles)
                x_grid = np.linspace(min(all_angles), max(all_angles), 300)
                pdf_ang = kde_ang(x_grid)
                peaks_idx, _ = scipy.signal.find_peaks(pdf_ang, prominence=0.01 * np.max(pdf_ang))
                n_peak_ang = len(peaks_idx)
                if n_peak_ang:
                    peak_pos_ang = x_grid[peaks_idx]
                    main_peak_ang = peak_pos_ang[np.argmax(pdf_ang[peaks_idx])]
            except Exception:
                pass
        
        print(f"    [D-H-A Angle]")
        print(f"      Samples: {n_ang:,}")
        print(f"      Mean / Median / Std: {mean_ang:.1f} / {med_ang:.1f} / {std_ang:.1f}°")
        print(f"      25% / 75% (IQR): {p25_ang:.1f} / {p75_ang:.1f}°")
        if skew_ang is not None:
            print(f"      Skewness: {skew_ang:.3f}")
        if n_peak_ang:
            peaks_str = ", ".join(f"{p:.1f}" for p in sorted(peak_pos_ang))
            print(f"      KDE Peaks: {n_peak_ang} (main={main_peak_ang:.1f}°; all=[{peaks_str}]°)")


def plot_water_states_distribution(water_states_data: Dict, output_dir: Path, dpi: int):
    """
    Plot the distribution of water hydrogen bond coordination states (nDmA).
    """
    import matplotlib.pyplot as plt
    
    dist = water_states_data['distribution']
    if not dist:
        return
        
    states = list(dist.keys())
    percentages = [info['percentage'] for info in dist.values()]
    counts = [info['count'] for info in dist.values()]
    
    # Premium color palette for states
    # Covers all physically relevant nDmA states in interface water systems
    state_colors = []
    color_map = {
        'free H2O': '#AEB6BF', # gray — isolated water
        # Symmetric states (D > 0 and A > 0)
        '1D1A': '#FAD7A0',    # soft orange-yellow
        '1D2A': '#F5B7B1',    # soft pink-red
        '2D1A': '#AED6F1',    # soft light blue
        '2D2A': '#A9DFBF',    # soft green (tetrahedral, bulk-like)
        '3D1A': '#D2B4DE',    # soft purple (bifurcated donor)
        '1D3A': '#A3E4D7',    # soft teal (overcoordinated acceptor)
        '2D3A': '#7FB3D8',    # steel blue
        '3D2A': '#C39BD3',    # medium purple
        # Donor-only states (A = 0): common at hydrophobic / O2 interface
        '1D0A': '#F9E79F',    # soft yellow
        '2D0A': '#F4D03F',    # golden yellow
        '3D0A': '#D4AC0D',    # dark gold (bifurcated, very rare)
        # Acceptor-only states (D = 0): common at charged surfaces
        '0D1A': '#D5F5E3',    # pale green
        '0D2A': '#82E0AA',    # medium green
        '0D3A': '#27AE60',    # deep green (overcoordinated, rare)
        # Extreme edge cases
        '0D4A': '#1E8449',    # forest green (very rare)
        '4D0A': '#B7950B',    # olive gold (artifact)
    }
    
    for s in states:
        state_colors.append(color_map.get(s, '#D5D8DC'))
        
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Water Hydrogen Bond Coordination States ($nDmA$)', fontsize=15, fontweight='bold', color='#2C3E50', y=0.98)
    
    # Left: Bar chart of all states
    ax_bar = axes[0]
    bars = ax_bar.bar(states, percentages, color=state_colors, edgecolor='#E5E7E9', linewidth=1.2, alpha=0.85)
    ax_bar.set_ylabel('Percentage (%)', fontsize=12)
    ax_bar.set_xlabel('Coordination State', fontsize=12)
    ax_bar.set_title('Detailed State Distribution', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    ax_bar.grid(axis='y', color=COLORS['gray_grid'], alpha=0.5)
    ax_bar.tick_params(axis='x', rotation=90)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax_bar.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#34495E')
                    
    # Right: Pie chart of major states (donut chart)
    ax_pie = axes[1]
    
    pie_labels = []
    pie_sizes = []
    pie_colors = []
    others_pct = 0.0
    
    # Sort states by percentage descending
    sorted_states = sorted(dist.items(), key=lambda x: x[1]['percentage'], reverse=True)
    
    for state, info in sorted_states:
        pct = info['percentage']
        if pct >= 2.0:
            pie_labels.append(state)
            pie_sizes.append(pct)
            pie_colors.append(color_map.get(state, '#D5D8DC'))
        else:
            others_pct += pct
            
    if others_pct > 0:
        pie_labels.append('Others')
        pie_sizes.append(others_pct)
        pie_colors.append('#E5E7E9')
        
    explode = [0.03 if s == '2D2A' or s == 'free H2O' else 0 for s in pie_labels]
    
    wedges, texts, autotexts = ax_pie.pie(
        pie_sizes, explode=explode, labels=pie_labels, colors=pie_colors,
        autopct='%1.1f%%', startangle=140, pctdistance=0.75,
        textprops=dict(color="#2C3E50", fontsize=11),
        wedgeprops=dict(edgecolor='#E5E7E9', linewidth=1.2)
    )
    
    for autotext in autotexts:
        autotext.set_weight('bold')
        
    centre_circle = plt.Circle((0,0), 0.50, fc='white', edgecolor='#E5E7E9')
    ax_pie.add_artist(centre_circle)
    
    ax_pie.set_title('Major Coordination States Summary', fontsize=12, fontweight='bold', color='#2C3E50', pad=10)
    
    fig.tight_layout()
    fig.savefig(output_dir / "water_states_distribution.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "water_states_distribution.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: water_states_distribution.png, water_states_distribution.svg")


def generate_advanced_plots(results: List[Dict], frames: List[Frame], 
                           advanced_stats: Dict, output_dir: Path, 
                           timestep_fs: float, sample_interval: int, dpi: int,
                           barcode_legend_loc: str = 'upper right',
                           diagram_legend_loc: str = 'lower right',
                           barcode_legend_fontsize: Optional[float] = None,
                           diagram_legend_fontsize: Optional[float] = None,
                           dynamics_legend_loc: str = 'upper right',
                           dynamics_legend_fontsize: Optional[float] = None):
    """Generate advanced analysis plots."""
    import matplotlib.pyplot as plt
    sns = None
    try:
        import seaborn as sns
    except ImportError:
        pass
    
    plt.style.use('seaborn-v0_8-ticks')
    try:
        sns.set_context("notebook", font_scale=1.1)
    except:
        pass
    
    # 4. Coordination and Degree Distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    coord_data = advanced_stats['coordination']
    if coord_data['raw_data']:
        axes[0].hist(coord_data['raw_data'], bins=range(0, max(coord_data['raw_data'])+2), 
                    color=COLORS['teal_soft'], edgecolor='white', alpha=0.85, align='left')
        axes[0].axvline(coord_data['mean'], color=COLORS['red_soft'], linestyle='--', linewidth=2,
                       label=f'Mean: {coord_data["mean"]:.2f}')
        axes[0].set_xlabel('Coordination Number', fontsize=12)
        axes[0].set_ylabel('Count', fontsize=12)
        axes[0].set_title('Coordination Number Distribution', fontsize=12, fontweight='bold', color='#2C3E50')
        axes[0].legend(frameon=False)
        axes[0].grid(axis='y', color=COLORS['gray_grid'], alpha=0.5)
    
    degree_data = advanced_stats['degree']
    if degree_data['raw_data']:
        axes[1].hist(degree_data['raw_data'], bins=range(0, max(degree_data['raw_data'])+2),
                    color=COLORS['purple_soft'], edgecolor='white', alpha=0.85, align='left')
        axes[1].axvline(degree_data['mean'], color=COLORS['red_soft'], linestyle='--', linewidth=2,
                       label=f'Mean: {degree_data["mean"]:.2f}')
        axes[1].set_xlabel('Node Degree', fontsize=12)
        axes[1].set_ylabel('Count', fontsize=12)
        axes[1].set_title('Degree Distribution', fontsize=12, fontweight='bold', color='#2C3E50')
        axes[1].legend(frameon=False)
        axes[1].grid(axis='y', color=COLORS['gray_grid'], alpha=0.5)

    fig.tight_layout()
    fig.savefig(output_dir / "coordination_degree.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "coordination_degree.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: coordination_degree.png, coordination_degree.svg")
    
    # 5. H-bond Lifetime Distribution
    lifetime_data = advanced_stats['lifetime']
    if lifetime_data['lifetimes']:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(lifetime_data['lifetimes'], bins=50, color=COLORS['orange_soft'], 
               edgecolor='white', alpha=0.85)
        ax.axvline(lifetime_data['mean'], color=COLORS['red_soft'], linestyle='--', linewidth=2,
                  label=f'Mean: {lifetime_data["mean"]:.2f} fs')
        ax.set_xlabel('H-bond Lifetime (fs)', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Hydrogen Bond Lifetime Distribution', fontsize=14, fontweight='bold', color='#2C3E50')
        ax.legend(frameon=False)
        ax.grid(axis='y', color=COLORS['gray_grid'], alpha=0.5)
        fig.tight_layout()
        fig.savefig(output_dir / "hbond_lifetime.png", dpi=dpi, bbox_inches='tight')
        fig.savefig(output_dir / "hbond_lifetime.svg", format='svg', bbox_inches='tight')
        plt.close(fig)
        print(f"    Saved: hbond_lifetime.png, hbond_lifetime.svg")
    
    # 6. Autocorrelation Function
    acf_data = advanced_stats['autocorrelation']
    if acf_data['acf']:
        fig, ax = plt.subplots(figsize=(8, 4))
        # ACF lags are in sampled frames, so multiply by (timestep * sample_interval)
        lags_time = [l * timestep_fs * sample_interval for l in acf_data['lags']]
        ax.plot(lags_time, acf_data['acf'], color=COLORS['blue_soft'], linewidth=2.5)
        ax.fill_between(lags_time, acf_data['acf'], color=COLORS['blue_fill'], alpha=0.15)
        ax.axhline(1/np.e, color=COLORS['red_soft'], linestyle='--', alpha=0.8, label='1/e')
        ax.set_xlabel('Time lag (fs)', fontsize=12)
        ax.set_ylabel('C(t)', fontsize=12)
        ax.set_title('H-bond Autocorrelation Function', fontsize=14, fontweight='bold', color='#2C3E50')
        ax.legend(frameon=False)
        ax.set_ylim(0, 1.1)
        ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
        fig.tight_layout()
        fig.savefig(output_dir / "autocorrelation.png", dpi=dpi, bbox_inches='tight')
        fig.savefig(output_dir / "autocorrelation.svg", format='svg', bbox_inches='tight')
        plt.close(fig)
        print(f"    Saved: autocorrelation.png, autocorrelation.svg")
    
    # 7. RDF Individual Pairs
    rdf_all = advanced_stats['rdf']
    if rdf_all:
        for pair_name, data in rdf_all.items():
            if data['r'] and data['g_r']:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(data['r'], data['g_r'], color='#5D6D7E', linewidth=2)
                ax.fill_between(data['r'], data['g_r'], color='#D6DBDF', alpha=0.3)
                ax.axhline(1.0, color='gray', linestyle=':', alpha=0.5)
                ax.set_xlabel('r (angstrom)', fontsize=12)
                ax.set_ylabel('g(r)', fontsize=12)
                ax.set_title(f'Radial Distribution Function: {pair_name}', fontsize=14, fontweight='bold', color='#2C3E50')
                ax.set_xlim(0, 8)
                ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)
                fig.tight_layout()
                
                # Save as rdf_PairName.png, replacing '-' with '_' for filename consistency if desired
                filename = f"rdf_{pair_name.replace('-', '_')}.png"
                fig.savefig(output_dir / filename, dpi=dpi, bbox_inches='tight')
                svg_filename = Path(filename).with_suffix('.svg')
                fig.savefig(output_dir / svg_filename, format='svg', bbox_inches='tight')
                plt.close(fig)
                print(f"    Saved: {filename}, {svg_filename}")
    
    # 8. Clustering Coefficient and H-bond Strength
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Clustering coefficient over time
    clustering_data = advanced_stats['clustering']
    # r['timestep'] is the absolute frame index
    times = [r['timestep'] * timestep_fs for r in results]
    axes[0].plot(times, clustering_data['per_frame'], color='#27AE60', linewidth=1.5)
    axes[0].fill_between(times, clustering_data['per_frame'], color='#ABEBC6', alpha=0.2)
    axes[0].axhline(clustering_data['mean'], color='red', linestyle='--', linewidth=1,
                   label=f'Mean: {clustering_data["mean"]:.3f}')
    axes[0].set_xlabel('Simulation time (fs)', fontsize=12)
    axes[0].set_ylabel('Clustering Coefficient', fontsize=12)
    axes[0].set_title('Network Clustering Coefficient', fontsize=12, fontweight='bold', color='#2C3E50')
    axes[0].legend(frameon=False)
    axes[0].grid(True, color=COLORS['gray_grid'], alpha=0.5)
    
    # H-bond strength pie chart
    strength_data = advanced_stats['strength']
    if strength_data['total'] > 0:
        labels = ['Strong\n(<2.8 A)', 'Moderate\n(2.8-3.2 A)', 'Weak\n(>3.2 A)']
        sizes = [strength_data['strong'], strength_data['moderate'], strength_data['weak']]
        explode = (0.05, 0, 0)
        
        # Use custom pie colors
        wedges, texts, autotexts = axes[1].pie(sizes, explode=explode, labels=labels, colors=COLORS['pie'],
                                              autopct='%1.1f%%', startangle=90, textprops=dict(color="#2C3E50"))
        
        # Make percentages bold
        for autotext in autotexts:
            autotext.set_weight('bold')
            
        axes[1].set_title('H-bond Strength Classification', fontsize=12, fontweight='bold', color='#2C3E50')

    fig.tight_layout()
    fig.savefig(output_dir / "clustering_strength.png", dpi=dpi, bbox_inches='tight')
    fig.savefig(output_dir / "clustering_strength.svg", format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: clustering_strength.png, clustering_strength.svg")
    
    # 9. Persistent Homology (Barcode, Diagram, and Dynamics)
    persistence_data = advanced_stats.get('persistence', {})
    if persistence_data.get('available') and persistence_data.get('barcodes'):
        barcodes = persistence_data['barcodes']
        frame_idx = persistence_data['frame_index']
        total_frames = persistence_data.get('total_frames', '?')
        all_frames_mode = persistence_data.get('all_frames', False)
        
        # Plot Barcode (representative frame)
        title_suffix = " [representative]" if all_frames_mode else ""
        plot_persistence_barcode(
            barcodes, 
            title=f"Persistence Barcode (Frame {frame_idx} / {total_frames}){title_suffix}",
            save_path=output_dir / "persistence_barcode.png",
            dpi=dpi,
            legend_loc=barcode_legend_loc,
            legend_fontsize=barcode_legend_fontsize
        )
        print(f"    Saved: persistence_barcode.png, persistence_barcode.svg")
        
        # Plot Diagram (representative frame)
        plot_persistence_diagram(
            barcodes,
            title=f"Persistence Diagram (Frame {frame_idx} / {total_frames}){title_suffix}",
            save_path=output_dir / "persistence_diagram.png",
            dpi=dpi,
            legend_loc=diagram_legend_loc,
            legend_fontsize=diagram_legend_fontsize
        )
        print(f"    Saved: persistence_diagram.png, persistence_diagram.svg")
        
        # If all frames were analyzed, plot persistence dynamics
        if all_frames_mode and 'dynamics' in persistence_data:
            plot_persistence_dynamics(
                persistence_data['dynamics'],
                timestep_fs=timestep_fs,
                sample_interval=sample_interval,
                save_path=output_dir / "persistence_dynamics.png",
                dpi=dpi,
                legend_loc=dynamics_legend_loc,
                legend_fontsize=dynamics_legend_fontsize
            )
            print(f"    Saved: persistence_dynamics.png, persistence_dynamics.svg")

    # 10. Water Coordination States Distribution
    if 'water_states' in advanced_stats:
        plot_water_states_distribution(advanced_stats['water_states'], output_dir, dpi)


# =============================================================================
# Topological Machine Learning Analysis
# =============================================================================

def perform_topological_ml_analysis(sc_list: List, ml_dim: int) -> Dict:
    """
    Perform topological machine learning analysis on a list of simplicial complexes.
    
    Includes:
    - Topological embeddings (Cell2Vec)
    - TNN feature extraction (SAN)
    - Dimensionality reduction (PCA)
    """
    if not sc_list:
        return {}
    
    print(f"    Running TML on {len(sc_list)} frames...")
    
    # 1. Topological Embeddings
    print("        Generating Cell2Vec embeddings...")
    embedder = HBondEmbedder(method='cell2vec', dimensions=ml_dim)
    frame_embeddings = []
    
    for i, sc in enumerate(sc_list):
        try:
            # Try specified method first, fallback to HOPE if it fails or returns zeros
            try:
                emb = embedder.fit_transform(sc)
            except Exception as e:
                if i < 3: print(f"        [Frame {i}] Cell2Vec failed: {e}", flush=True)
                emb = None
            
            # If zeros or None, try HOPE (deterministic)
            if emb is None or len(emb) == 0 or (isinstance(emb, np.ndarray) and np.ptp(emb) == 0):
                if i < 3: print(f"        [Frame {i}] Falling back to HOPE...", flush=True)
                try:
                    fallback_embedder = HBondEmbedder(method='hope', dimensions=ml_dim)
                    emb = fallback_embedder.fit_transform(sc)
                except Exception as e:
                    if i < 3: print(f"        [Frame {i}] HOPE failed: {e}", flush=True)
                    emb = None
                
            if emb is not None and len(emb) > 0:
                frame_embeddings.append(np.mean(emb, axis=0))
            else:
                frame_embeddings.append(np.zeros(ml_dim))
        except Exception as e:
            if i < 3: print(f"        [Frame {i}] Processing failed: {e}", flush=True)
            frame_embeddings.append(np.zeros(ml_dim))
    
    frame_embeddings = np.array(frame_embeddings)
    
    # Debug: Check variance
    ptp = np.ptp(frame_embeddings)
    if ptp == 0:
        print("        Warning: Frame embeddings have zero variance. Try a different rank or check data.")
    
    # 2. TNN Feature Extraction (Demonstration)
    print("        Extracting TNN features (SAN forward pass)...")
    tnn_features = None
    try:
        import torch
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"        Using device: {device}")
        
        model = HBondTNN(in_channels=1, hidden_channels=ml_dim, out_channels=ml_dim)
        model = model.to(device)
        model.eval()
        
        tnn_feats_list = []
        for sc in sc_list:
            if sc.dim >= 1:
                data = prepare_tnn_data(sc)
                # Move data to device
                edge_features = data['edge_features'].to(device)
                laplacian_up = data['laplacian_up'].to(device)
                laplacian_down = data['laplacian_down'].to(device)
                
                with torch.no_grad():
                    edge_feats, _ = model(edge_features, laplacian_up, laplacian_down)
                    # Move result back to CPU for numpy conversion
                    tnn_feats_list.append(edge_feats.mean(dim=0).cpu().numpy())
            else:
                tnn_feats_list.append(np.zeros(ml_dim))
        tnn_features = np.array(tnn_feats_list)
    except Exception as e:
        print(f"        Warning: TNN feature extraction failed: {e}")
    
    # 3. PCA on embeddings
    pca_results = None
    explained_variance = []
    try:
        from sklearn.decomposition import PCA
        # Check if we have enough variance to run PCA
        if len(frame_embeddings) > 1 and ptp > 0:
            pca = PCA(n_components=min(2, len(frame_embeddings)))
            pca_results = pca.fit_transform(frame_embeddings)
            explained_variance = pca.explained_variance_ratio_.tolist()
        else:
            # If zero variance, we can still "mock" PCA data for visualization if we want
            # but better to just report it.
            print("        Skipping PCA: zero variance in embeddings.")
    except Exception as e:
         print(f"        Warning: PCA analysis failed: {e}")
        
    return {
        'frame_embeddings': frame_embeddings,
        'tnn_features': tnn_features,
        'pca_results': pca_results,
        'explained_variance': explained_variance
    }


def generate_ml_plots(ml_results: Dict, output_dir: Path, dpi: int, timestep_fs: float = 0.5, sample_interval: int = 1):
    """Generate plots for TML analysis."""
    import matplotlib.pyplot as plt
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Similarity Heatmap (Doesn't depend on PCA)
    embeddings = ml_results.get('frame_embeddings')
    if embeddings is not None and len(embeddings) > 1:
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            similarity_matrix = cosine_similarity(embeddings)
            
            fig, ax = plt.subplots(figsize=(8, 7))
            
            # Calculate total time in ps
            total_time_ps = len(embeddings) * sample_interval * timestep_fs / 1000.0
            
            im = ax.imshow(similarity_matrix, cmap='magma', origin='lower',
                           extent=[0, total_time_ps, 0, total_time_ps])
            
            cbar = plt.colorbar(im)
            cbar.set_label('Cosine Similarity', fontsize=12)
            ax.set_xlabel('Simulation time (ps)', fontsize=12)
            ax.set_ylabel('Simulation time (ps)', fontsize=12)
            ax.set_title('Inter-Frame Topological Similarity', fontsize=14, fontweight='bold')
            
            fig.tight_layout()
            fig.savefig(output_dir / "similarity_heatmap.png", dpi=dpi, bbox_inches='tight')
            fig.savefig(output_dir / "similarity_heatmap.svg", format='svg', bbox_inches='tight')
            plt.close(fig)
            print(f"    Saved: similarity_heatmap.png, similarity_heatmap.svg")
        except Exception as e:
            print(f"    Warning: Similarity heatmap failed: {e}")

    # 2. PCA Results (Scatter and Time-Series)
    pca_data = ml_results.get('pca_results')
    if pca_data is not None and len(pca_data) >= 1:
        try:
            # PCA Scatter Plot
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(pca_data[:, 0], pca_data[:, 1], c=range(len(pca_data)), 
                                 cmap='viridis', alpha=0.7, s=50)
            cbar = plt.colorbar(scatter)
            cbar.set_label('Frame Index', fontsize=12)
            
            if len(ml_results.get('explained_variance', [])) >= 2:
                ax.set_xlabel(f'PC1 ({ml_results["explained_variance"][0]*100:.1f}%)', fontsize=12)
                ax.set_ylabel(f'PC2 ({ml_results["explained_variance"][1]*100:.1f}%)', fontsize=12)
            else:
                ax.set_xlabel('PC1', fontsize=12)
                ax.set_ylabel('PC2', fontsize=12)
                
            ax.set_title('PCA of Topological Embeddings', fontsize=14, fontweight='bold')
            
            fig.tight_layout()
            fig.savefig(output_dir / "embedding_pca.png", dpi=dpi, bbox_inches='tight')
            fig.savefig(output_dir / "embedding_pca.svg", format='svg', bbox_inches='tight')
            plt.close(fig)
            print(f"    Saved: embedding_pca.png, embedding_pca.svg")
        except Exception as e:
            print(f"    Warning: PCA scatter plot failed: {e}")
        
        try:
            # PCA vs Time
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Calculate time in ps: frame_idx * sample_interval * timestep_fs / 1000
            time_ps = np.arange(len(pca_data)) * sample_interval * timestep_fs / 1000.0
            
            # PC1
            ax.plot(time_ps, pca_data[:, 0], label='PC1', color=COLORS['blue_soft'], linewidth=2, alpha=0.9)
            ax.fill_between(time_ps, pca_data[:, 0], color=COLORS['blue_fill'], alpha=0.15)
            
            # PC2
            if pca_data.shape[1] > 1:
                ax.plot(time_ps, pca_data[:, 1], label='PC2', color=COLORS['red_soft'], linewidth=2, alpha=0.9)
                ax.fill_between(time_ps, pca_data[:, 1], color=COLORS['red_fill'], alpha=0.15)
                
            ax.set_xlabel('Simulation time (ps)', fontsize=12)
            ax.set_ylabel('Principal Component Value', fontsize=12)
            ax.set_title('PCA Components Evolution', fontsize=14, fontweight='bold', color='#2C3E50')
            ax.legend(frameon=False)
            ax.grid(True, color=COLORS['gray_grid'], alpha=0.5)

            fig.tight_layout()
            fig.savefig(output_dir / "pca_time_series.png", dpi=dpi, bbox_inches='tight')
            fig.savefig(output_dir / "pca_time_series.svg", format='svg', bbox_inches='tight')
            plt.close(fig)
            print(f"    Saved: pca_time_series.png, pca_time_series.svg")
        except Exception as e:
            print(f"    Warning: PCA time-series plot failed: {e}")


# =============================================================================
# Results Saving
# =============================================================================

def save_results(results: List[Dict], advanced_stats: Dict, output_dir: Path, ml_results: Optional[Dict] = None):
    """Save analysis results to JSON files."""
    def convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, set):
            return list(obj)
        return obj
    
    # Per-frame results (simplified)
    simplified_results = []
    for r in results:
        simplified_results.append({
            'timestep': convert(r['timestep']),
            'n_hbonds': convert(r['n_hbonds']),
            'betti_0': convert(r['betti_0']),
            'betti_1': convert(r['betti_1']),
            'betti_2': convert(r['betti_2']),
            'euler_char': convert(r['euler_char']),
            'mean_distance_da': float(np.mean(r['distances_da'])) if r['distances_da'] else 0,
            'mean_angle_dha': float(np.mean(r['angles_dha'])) if r['angles_dha'] else 0,
        })
    
    with open(output_dir / "analysis_results.json", 'w') as f:
        json.dump(simplified_results, f, indent=2)
    print(f"    Saved: analysis_results.json")
    
    # Comprehensive statistics
    n_hbonds = [r['n_hbonds'] for r in results]
    betti_0 = [r['betti_0'] for r in results]
    betti_1 = [r['betti_1'] for r in results]
    betti_2 = [r['betti_2'] for r in results]
    
    all_distances_da = []
    all_angles = []
    for r in results:
        all_distances_da.extend(r['distances_da'])
        all_angles.extend(r['angles_dha'])
    
    stats = {
        'n_frames_analyzed': len(results),
        'basic_statistics': {
            'hbond_count': {
                'mean': float(np.mean(n_hbonds)),
                'std': float(np.std(n_hbonds)),
                'min': int(np.min(n_hbonds)),
                'max': int(np.max(n_hbonds)),
            },
            'betti_0': {
                'mean': float(np.mean(betti_0)),
                'std': float(np.std(betti_0)),
            },
            'betti_1': {
                'mean': float(np.mean(betti_1)),
                'std': float(np.std(betti_1)),
            },
            'betti_2': {
                'mean': float(np.mean(betti_2)),
                'std': float(np.std(betti_2)),
            },
            'geometry': {
                'mean_distance_da': float(np.mean(all_distances_da)) if all_distances_da else 0,
                'std_distance_da': float(np.std(all_distances_da)) if all_distances_da else 0,
                'mean_angle_dha': float(np.mean(all_angles)) if all_angles else 0,
                'std_angle_dha': float(np.std(all_angles)) if all_angles else 0,
            }
        },
        'advanced_statistics': {
            'coordination': {
                'mean': advanced_stats['coordination']['mean'],
                'std': advanced_stats['coordination']['std'],
                'distribution': advanced_stats['coordination']['distribution'],
            },
            'water_states': advanced_stats['water_states']['distribution'],
            'degree': {
                'mean': advanced_stats['degree']['mean'],
                'std': advanced_stats['degree']['std'],
                'distribution': advanced_stats['degree']['distribution'],
            },
            'lifetime': {
                'mean_fs': advanced_stats['lifetime']['mean'],
                'std_fs': advanced_stats['lifetime']['std'],
                'max_fs': advanced_stats['lifetime']['max'],
            },
            'clustering': {
                'mean': advanced_stats['clustering']['mean'],
                'std': advanced_stats['clustering']['std'],
            },
            'hbond_strength': advanced_stats['strength'],
            'persistent_homology': {
                'available': advanced_stats['persistence']['available'],
                'frame_index': advanced_stats['persistence'].get('frame_index'),
                'total_frames': advanced_stats['persistence'].get('total_frames'),
                'all_frames_analyzed': advanced_stats['persistence'].get('all_frames', False),
            }
        }
    }
    
    # Add persistence dynamics statistics if all frames were analyzed
    persistence_data = advanced_stats.get('persistence', {})
    if persistence_data.get('all_frames') and 'dynamics' in persistence_data:
        dynamics = persistence_data['dynamics']
        stats['advanced_statistics']['persistent_homology']['dynamics_summary'] = {
            'total_persistence_H0': {
                'mean': float(np.mean(dynamics['total_persistence_H0'])),
                'std': float(np.std(dynamics['total_persistence_H0'])),
            },
            'total_persistence_H1': {
                'mean': float(np.mean(dynamics['total_persistence_H1'])),
                'std': float(np.std(dynamics['total_persistence_H1'])),
            },
            'n_features_H0': {
                'mean': float(np.mean(dynamics['n_features_H0'])),
                'std': float(np.std(dynamics['n_features_H0'])),
            },
            'n_features_H1': {
                'mean': float(np.mean(dynamics['n_features_H1'])),
                'std': float(np.std(dynamics['n_features_H1'])),
            },
        }
    
    if ml_results:
        stats['topological_machine_learning'] = {
            'pca_explained_variance': convert(ml_results.get('explained_variance')),
            'feature_extraction': 'Cell2Vec (Embedding) + SAN (TNN)'
        }
        
        # Save embeddings separately
        if ml_results.get('frame_embeddings') is not None:
            np.save(output_dir / "frame_embeddings.npy", ml_results['frame_embeddings'])
            print(f"    Saved: frame_embeddings.npy")
        if ml_results.get('tnn_features') is not None:
            np.save(output_dir / "tnn_features.npy", ml_results['tnn_features'])
            print(f"    Saved: tnn_features.npy")
    
    with open(output_dir / "statistics_summary.json", 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"    Saved: statistics_summary.json")


def save_raw_data(results: List[Dict], advanced_stats: Dict, ml_results: Optional[Dict], 
                 output_dir_raw: Union[str, Path], timestep_fs: float, sample_interval: int):
    """Save raw data of analysis to CSV files."""
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas is required for reducing raw data to CSV. Please install pandas.")
        return

    out_path = Path(output_dir_raw)
    out_path.mkdir(parents=True, exist_ok=True)
    print(f"\n[7.5] Saving raw data to CSV in {out_path.resolve()}...")

    # 1. H-bond Dynamics & Topology (Time Series)
    # Extract time series data
    data_dynamics = []
    for r in results:
        t_fs = r['timestep'] * timestep_fs
        metric = {
            'time_fs': t_fs,
            'time_ps': t_fs / 1000.0,
            'n_hbonds': r['n_hbonds'],
            'betti_0': r['betti_0'],
            'betti_1': r['betti_1'],
            'betti_2': r['betti_2'],
            'euler_characteristic': r['euler_char']
        }
        data_dynamics.append(metric)
    
    df_dynamics = pd.DataFrame(data_dynamics)
    df_dynamics.to_csv(out_path / "dynamics_topology.csv", index=False)
    print(f"    Saved: dynamics_topology.csv")

    # 2. Lifetime & Autocorrelation
    # Lifetime ACF
    if 'lifetime' in advanced_stats and 'acf' in advanced_stats['lifetime']:
        acf = advanced_stats['lifetime']['acf']
        lags = np.arange(len(acf))
        times_fs = lags * sample_interval * timestep_fs
        df_life = pd.DataFrame({'lag_time_fs': times_fs, 'acf': acf})
        df_life.to_csv(out_path / "hbond_lifetime_acf.csv", index=False)
        print(f"    Saved: hbond_lifetime_acf.csv")
        
    # Property Autocorrelation
    if 'autocorrelation' in advanced_stats and advanced_stats['autocorrelation']['acf'] is not None:
        acf_prop = advanced_stats['autocorrelation']['acf']
        lags_prop = advanced_stats['autocorrelation']['lags']
        times_prop_fs = np.array(lags_prop) * sample_interval * timestep_fs
        df_acf = pd.DataFrame({'lag_time_fs': times_prop_fs, 'property_acf': acf_prop})
        df_acf.to_csv(out_path / "property_autocorrelation.csv", index=False)
        print(f"    Saved: property_autocorrelation.csv")

    # 3. Clustering
    if 'clustering' in advanced_stats and 'per_frame' in advanced_stats['clustering']:
        clustering_vals = advanced_stats['clustering']['per_frame']
        # Assuming clustering aligns with results
        times_cluster = [r['timestep'] * timestep_fs for r in results]
        df_cluster = pd.DataFrame({
            'time_fs': times_cluster,
            'time_ps': np.array(times_cluster) / 1000.0,
            'clustering_coefficient': clustering_vals
        })
        df_cluster.to_csv(out_path / "clustering_coefficient.csv", index=False)
        print(f"    Saved: clustering_coefficient.csv")

    # 4. RDFs
    if 'rdf' in advanced_stats:
        for pair_name, rdf_data in advanced_stats['rdf'].items():
            if rdf_data.get('r') is not None and rdf_data.get('g_r') is not None:
                df_rdf = pd.DataFrame({
                    'r_angstrom': rdf_data['r'],
                    'g_r': rdf_data['g_r']
                })
                # filename safe
                safe_name = pair_name.replace('-', '_')
                df_rdf.to_csv(out_path / f"rdf_{safe_name}.csv", index=False)
                print(f"    Saved: rdf_{safe_name}.csv")

    # 5. Distributions (Coordination, Degree)
    # These are usually histograms in 'distribution' key as (bin_edges, counts) or similar
    # Check structure from code viewing earlier: 'distribution' seemed to be stored.
    # Actually, let's re-compute or extract if available. 
    # The 'compute_coordination_numbers' returns dict with 'distribution': tuple(bins, counts)? 
    # Wait, need to check structure. 
    # Based on plot code: coord_data['raw_data'] is used for histogram. 
    # advanced_stats['coordination'] has 'raw_data'? Yes.
    
    if 'coordination' in advanced_stats and 'raw_records' in advanced_stats['coordination']:
        # Save raw observations with labels
        df_coord_raw = pd.DataFrame(advanced_stats['coordination']['raw_records'])
        df_coord_raw.to_csv(out_path / "coordination_raw_obs.csv", index=False)
        print(f"    Saved: coordination_raw_obs.csv")
    
    if 'degree' in advanced_stats and 'raw_records' in advanced_stats['degree']:
        # Save raw observations with labels
        df_degree_raw = pd.DataFrame(advanced_stats['degree']['raw_records'])
        df_degree_raw.to_csv(out_path / "degree_raw_obs.csv", index=False)
        print(f"    Saved: degree_raw_obs.csv")


    # 6. ML Results
    if ml_results:
        # PCA
        if 'pca_results' in ml_results and ml_results['pca_results'] is not None:
            pca_data = ml_results['pca_results']
            df_pca = pd.DataFrame(pca_data, columns=[f'PC{i+1}' for i in range(pca_data.shape[1])])
            
            # Add time info
            total_frames = len(pca_data)
            time_arr = np.arange(total_frames) * sample_interval * timestep_fs
            df_pca.insert(0, 'time_fs', time_arr)
            df_pca.insert(1, 'time_ps', time_arr / 1000.0)
            
            df_pca.to_csv(out_path / "ml_pca_components.csv", index=False)
            print(f"    Saved: ml_pca_components.csv")
            
        # Explained Variance
        if 'explained_variance' in ml_results:
            df_var = pd.DataFrame({
                'component': [f'PC{i+1}' for i in range(len(ml_results['explained_variance']))],
                'explained_variance_ratio': ml_results['explained_variance']
            })
            df_var.to_csv(out_path / "ml_pca_variance.csv", index=False)
            print(f"    Saved: ml_pca_variance.csv")

        # Similarity Matrix
        if 'frame_embeddings' in ml_results:
            # We can compute it again or if we had it. 
            # We generate it on the fly in plotting usually.
            # Let's save the frame embeddings themselves, user can compute similarity.
            # Saved as .npy in main, but let's save as CSV if dimensionality is not too high?
            # 32 dims * 500 frames is small.
            embeddings = ml_results['frame_embeddings']
            if embeddings is not None:
                df_emb = pd.DataFrame(embeddings, columns=[f'dim_{i}' for i in range(embeddings.shape[1])])
                df_emb.insert(0, 'frame_idx', range(len(embeddings)))
                df_emb.to_csv(out_path / "ml_frame_embeddings.csv", index=False)
                print(f"    Saved: ml_frame_embeddings.csv")
                
                # Also save Similarity Matrix since user asked for heatmap data
                try:
                    from sklearn.metrics.pairwise import cosine_similarity
                    sim_mat = cosine_similarity(embeddings)
                    df_sim = pd.DataFrame(sim_mat)
                    df_sim.to_csv(out_path / "ml_similarity_matrix.csv", index=False, header=False)
                    print(f"    Saved: ml_similarity_matrix.csv")
                except ImportError:
                    pass

    # 7. Persistence Dynamics (if all frames were analyzed)
    persistence_data = advanced_stats.get('persistence', {})
    if persistence_data.get('all_frames') and 'dynamics' in persistence_data:
        dynamics = persistence_data['dynamics']
        n_frames = len(dynamics['total_persistence_H0'])
        time_arr = np.arange(n_frames) * sample_interval * timestep_fs
        
        df_persist = pd.DataFrame({
            'frame_idx': range(n_frames),
            'time_fs': time_arr,
            'time_ps': time_arr / 1000.0,
            'total_persistence_H0': dynamics['total_persistence_H0'],
            'total_persistence_H1': dynamics['total_persistence_H1'],
            'n_features_H0': dynamics['n_features_H0'],
            'n_features_H1': dynamics['n_features_H1'],
            'mean_lifetime_H0': dynamics['mean_lifetime_H0'],
            'mean_lifetime_H1': dynamics['mean_lifetime_H1'],
        })
        df_persist.to_csv(out_path / "persistence_dynamics.csv", index=False)
        print(f"    Saved: persistence_dynamics.csv")

    # 8. Water Coordination States
    if 'water_states' in advanced_stats:
        if 'raw_records' in advanced_stats['water_states']:
            df_states_raw = pd.DataFrame(advanced_stats['water_states']['raw_records'])
            df_states_raw.to_csv(out_path / "water_states_raw.csv", index=False)
            print(f"    Saved: water_states_raw.csv")
        
        if 'distribution' in advanced_stats['water_states']:
            dist_list = []
            for s_name, s_info in advanced_stats['water_states']['distribution'].items():
                dist_list.append({
                    'coordination_state': s_name,
                    'count': s_info['count'],
                    'percentage': s_info['percentage']
                })
            df_dist = pd.DataFrame(dist_list)
            df_dist.to_csv(out_path / "water_states_distribution.csv", index=False)
            print(f"    Saved: water_states_distribution.csv")

    print("    Done saving raw data.\n")


# =============================================================================
# Main Analysis Script
# =============================================================================

def main():
    """Run comprehensive H-bond topology analysis on CP2K AIMD trajectory."""
    
    args = parse_args()
    traj_file = Path(__file__).parent / args.trajectory
    
    if not traj_file.exists():
        print(f"Error: Trajectory file not found: {traj_file}")
        return

    # Redirect stdout/stderr to both terminal and log file in default results dir
    output_dir = Path(__file__).parent / args.output_dir
    output_dir.mkdir(exist_ok=True)
    log_name = f"topoHBNet_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = output_dir / log_name
    log_file = open(log_path, "w", encoding="utf-8")
    _orig_stdout, _orig_stderr = sys.stdout, sys.stderr
    sys.stdout = _Tee(_orig_stdout, log_file)
    sys.stderr = _Tee(_orig_stderr, log_file)
    try:
        _main_body(args, traj_file, output_dir, log_path)
    finally:
        sys.stdout = _orig_stdout
        sys.stderr = _orig_stderr
        log_file.close()


def _main_body(args, traj_file: Path, output_dir: Path, log_path: Path):
    """Main analysis logic (stdout/stderr are already teed to log)."""
    print("=" * 70)
    print("CP2K AIMD Hydrogen Bond Topology Analysis")
    print("=" * 70)
    print(f"    Log file: {log_path}")
    print(f"\nConfiguration:")
    print(f"    Timestep: {args.timestep} fs")
    print(f"    Sample interval: every {args.sample_interval} frames")
    print(f"    H-bond criteria: D-A < {args.r_da_max} A, H-A < {args.r_ha_max} A, angle > {args.angle_min} deg")
    print(f"    Persistence frame: {args.persistence_frame}")
    print(f"    Output DPI: {args.dpi}")
    print(f"    GUDHI available: {HAS_GUDHI}")
    
    # Parse trajectory
    print("\n[1] Parsing trajectory with ASE backend...")
    cell_path = Path(__file__).parent / args.cell_file if args.cell_file else None
    parser = TrajectoryParser(traj_file, format='xyz', cell_filepath=cell_path)
    frames = parser.parse()
    print(f"    Loaded {len(frames)} frames")
    print(f"    Atoms per frame: {frames[0].n_atoms}")
    print(f"    Simulation time: {len(frames) * args.timestep:.1f} fs")
    
    n_oxygen = np.sum(frames[0].symbols == 'O')
    n_hydrogen = np.sum(frames[0].symbols == 'H')
    print(f"    Oxygen atoms: {n_oxygen}, Hydrogen atoms: {n_hydrogen}")
    
    unique_elements = np.unique(frames[0].symbols)
    print(f"    Elements: {', '.join(unique_elements)}")
    
    # Equilibration detection — cut BEFORE analysis
    import equilibration_utils
    sample_interval = args.sample_interval
    base_dir = Path(__file__).parent

    print("\n[2] Equilibration detection (cut before analysis)...")
    t0_raw, g, Neff, actual_obs, ts_signal = equilibration_utils.resolve_equilibration_start(
        args, fallback_timeseries=None, fallback_observable="n_hbonds",
        sample_interval=sample_interval, base_dir=base_dir
    )

    # Generate equilibration diagnostic report and plot
    if ts_signal is not None and len(ts_signal) > 0:
        # For .ener-based detection, time_arr is per raw frame
        if actual_obs in {"potential_energy", "temperature", "kinetic_energy", "conserved_quantity"}:
            time_arr_fs = np.arange(len(ts_signal)) * args.timestep
        else:
            time_arr_fs = np.arange(len(ts_signal)) * sample_interval * args.timestep
    else:
        time_arr_fs = np.array([])
    equilibration_utils.generate_equilibration_report_and_plot(
        t0_raw, g, Neff, ts_signal, time_arr_fs,
        actual_obs if actual_obs != "potential_energy" else "potential_energy", output_dir
    )

    # Trim equilibration frames from raw trajectory
    if t0_raw > 0:
        print(f"    [Equilibration] Discarding first {t0_raw} raw frames as equilibration phase.")
        frames = frames[t0_raw:]
        print(f"    [Equilibration] Production phase raw frames: {len(frames)}")
    else:
        print(f"    [Equilibration] No equilibration trimming needed (t0_raw=0).")
    
    # Initialize analyzers
    print("\n[3] Initializing analyzers...")
    detector = HBondDetector(
        r_da_max=args.r_da_max,
        r_ha_max=args.r_ha_max,
        angle_min=args.angle_min,
        o_symbol='O',
        h_symbol='H'
    )
    builder = HBondComplexBuilder()
    invariants = TopologicalInvariants()
    
    # Analyze production trajectory only
    print(f"\n[4] Analyzing production trajectory (every {sample_interval} frames)...")
    sampled_frames = frames[::sample_interval]
    results = []
    sc_list = [] if args.run_ml else None
    
    for i, frame in enumerate(sampled_frames):
        result = analyze_frame(frame, detector, builder, invariants)
        # timestep reflects global frame index (including equilibration offset)
        result['timestep'] = t0_raw + i * sample_interval
        results.append(result)
        
        if args.run_ml:
            hbonds = detector.detect_hbonds(frame)
            if hbonds:
                sc_list.append(builder.build_from_frame(frame, hbonds))
            else:
                import toponetx as tnx
                sc_list.append(tnx.SimplicialComplex())
                
        if (i + 1) % 50 == 0:
            print(f"    Processed {i + 1}/{len(sampled_frames)} frames...")
    
    print(f"    Completed analysis of {len(results)} production frames")

    # Advanced analysis
    print("\n[5] Running advanced analysis...")
    advanced_stats = {}
    
    print("    Computing coordination numbers...")
    advanced_stats['coordination'] = compute_coordination_numbers(results)
    
    print("    Computing detailed water coordination states (nDmA)...")
    advanced_stats['water_states'] = compute_water_hbond_states(results, sampled_frames, detector)
    
    print("    Computing degree distribution...")
    advanced_stats['degree'] = compute_degree_distribution(results)
    
    print("    Computing H-bond lifetimes...")
    advanced_stats['lifetime'] = compute_hbond_lifetime(results, args.timestep * sample_interval)
    
    print("    Computing autocorrelation function...")
    advanced_stats['autocorrelation'] = compute_autocorrelation(results)
    
    print("    Computing clustering coefficients...")
    advanced_stats['clustering'] = compute_clustering_coefficient(results)
    
    print("    Computing RDFs for multiple pairs...")
    rdfs = {}
    rdf_pairs = [('O', 'O'), ('O', 'H'), ('H', 'H'), ('La', 'O'), ('K', 'O'), ('P', 'O')]
    for s1, s2 in rdf_pairs:
        # Check if both elements exist in first frame
        if s1 in unique_elements and s2 in unique_elements:
            print(f"        RDF: {s1}-{s2}")
            rdfs[f"{s1}-{s2}"] = compute_rdf(sampled_frames, s1, s2)
    advanced_stats['rdf'] = rdfs
    
    print("    Classifying H-bond strength...")
    advanced_stats['strength'] = classify_hbond_strength(results)
    
    print("    Computing persistent homology...")
    advanced_stats['persistence'] = compute_persistent_homology(
        results, sampled_frames, frame_selection=args.persistence_frame
    )
    
    # Print summary statistics
    print("\n[6] Summary Statistics:")
    n_hbonds = [r['n_hbonds'] for r in results]
    print(f"    H-bonds: {np.mean(n_hbonds):.1f} +/- {np.std(n_hbonds):.1f}")
    print(f"    Coordination: {advanced_stats['coordination']['mean']:.2f} +/- {advanced_stats['coordination']['std']:.2f}")
    if 'water_states' in advanced_stats and advanced_stats['water_states']['distribution']:
        water_states_dist = advanced_stats['water_states']['distribution']
        top_states = sorted(water_states_dist.items(), key=lambda x: x[1]['percentage'], reverse=True)[:3]
        top_states_str = ", ".join(f"{state}: {info['percentage']:.1f}%" for state, info in top_states)
        print(f"    Water States (top 3): {top_states_str}")
    print(f"    H-bond lifetime: {advanced_stats['lifetime']['mean']:.2f} fs")
    print(f"    Clustering coeff: {advanced_stats['clustering']['mean']:.3f}")
    print(f"    H-bond strength: Strong {advanced_stats['strength']['strong_pct']:.1f}%, "
          f"Moderate {advanced_stats['strength']['moderate_pct']:.1f}%, "
          f"Weak {advanced_stats['strength']['weak_pct']:.1f}%")
    
    # ML Analysis
    ml_results = {}
    if args.run_ml:
        print("\n[6.5] Running Topological Machine Learning analysis...")
        ml_results = perform_topological_ml_analysis(sc_list, args.ml_dim)
        generate_ml_plots(ml_results, output_dir, args.dpi, args.timestep, args.sample_interval)
    
    # Save results
    print("\n[7] Saving results...")
    save_results(results, advanced_stats, output_dir, ml_results if args.run_ml else None)
    
    if args.output_dir_rawdata:
        raw_dir = Path(args.output_dir_rawdata)
        if not raw_dir.is_absolute():
            raw_dir = output_dir / raw_dir
        save_raw_data(results, advanced_stats, ml_results if args.run_ml else None, 
                     raw_dir, args.timestep, args.sample_interval)
    
    # Generate plots
    print("\n[8] Generating plots...")
    try:
        generate_basic_plots(results, output_dir, args.timestep, args.dpi)
        generate_advanced_plots(results, sampled_frames, advanced_stats, output_dir, 
                               args.timestep, args.sample_interval, args.dpi,
                               barcode_legend_loc=args.persistence_barcode_legend_loc,
                               diagram_legend_loc=args.persistence_diagram_legend_loc,
                               barcode_legend_fontsize=args.persistence_barcode_legend_fontsize,
                               diagram_legend_fontsize=args.persistence_diagram_legend_fontsize,
                               dynamics_legend_loc=args.persistence_dynamics_legend_loc,
                               dynamics_legend_fontsize=args.persistence_dynamics_legend_fontsize)
    except ImportError as e:
        print(f"    Warning: matplotlib not available: {e}")
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
