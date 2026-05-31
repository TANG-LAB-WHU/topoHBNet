import numpy as np
import networkx as nx
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional

class ProtonTransferProfiler:
    """
    Computes proton transfer statistics, including projection coordinates,
    potential of mean force (PMF), and identifies low-barrier hydrogen bonds (LBHBs).
    """
    def __init__(self, temperature: float = 300.0):
        self.temperature = temperature
        self.kb = 8.617333262145e-5  # eV/K
        self.kb_kcal_mol = 0.0019872041  # kcal/(mol K)
        self.delta_values = []
        self.lbhb_count = 0
        self.total_hbonds = 0

    def add_hbond(self, d_dh: float, d_ha: float, d_oo: float):
        """
        Record a hydrogen bond.
        
        Args:
            d_dh: Distance between Donor and Hydrogen (Angstroms)
            d_ha: Distance between Hydrogen and Acceptor (Angstroms)
            d_oo: Distance between Donor and Acceptor (e.g., O-O) (Angstroms)
        """
        delta = d_dh - d_ha
        self.delta_values.append(delta)
        self.total_hbonds += 1
        
        # LBHB criterion: typically O-O distance < 2.45 A
        if d_oo < 2.45:
            self.lbhb_count += 1

    def compute_pmf(self, bins: int = 50, range_val: Tuple[float, float] = (-1.0, 1.0)) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the Potential of Mean Force (PMF) from accumulated delta values.
        
        Returns:
            centers: Bin centers for delta
            pmf: Free energy profile in kcal/mol
        """
        if not self.delta_values:
            return np.array([]), np.array([])
            
        hist, bin_edges = np.histogram(self.delta_values, bins=bins, range=range_val, density=True)
        centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        
        # Avoid log(0)
        hist = np.where(hist == 0, 1e-10, hist)
        
        # PMF = -kT ln(P)
        pmf = -self.kb_kcal_mol * self.temperature * np.log(hist)
        
        # Shift minimum to 0
        pmf -= np.min(pmf)
        return centers, pmf

    def get_lbhb_fraction(self) -> float:
        """Returns the fraction of H-bonds that are LBHBs."""
        if self.total_hbonds == 0:
            return 0.0
        return self.lbhb_count / self.total_hbonds


class ProtonWireTracker:
    """
    Tracks and analyzes "proton wires" via shortest path search on the H-bond network.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.path_lengths = []
        self.path_lifetimes = {}  # tuple of path nodes -> count

    def update_network(self, nodes: List[Any], edges: List[Tuple[Any, Any, Dict]]):
        """
        Update the current H-bond network.
        
        Args:
            nodes: List of node identifiers.
            edges: List of (u, v, attr_dict) representing directed H-bonds.
        """
        self.graph.clear()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

    def find_proton_wires(self, sources: List[Any], sinks: List[Any], weight: str = 'weight') -> List[List[Any]]:
        """
        Find shortest paths from any source to any sink.
        
        Args:
            sources: List of source node IDs (e.g. surface hydroxyls).
            sinks: List of sink node IDs (e.g. bulk water, reactive molecules).
            weight: Edge attribute to use as weight (e.g. distance or -bond_strength).
            
        Returns:
            List of node lists representing the shortest paths found.
        """
        wires = []
        for src in sources:
            if src not in self.graph:
                continue
            for sink in sinks:
                if sink not in self.graph:
                    continue
                try:
                    path = nx.shortest_path(self.graph, source=src, target=sink, weight=weight)
                    wires.append(path)
                    
                    # Track lifetime / occurrence
                    path_tuple = tuple(path)
                    self.path_lifetimes[path_tuple] = self.path_lifetimes.get(path_tuple, 0) + 1
                    self.path_lengths.append(len(path) - 1)  # number of hops
                except nx.NetworkXNoPath:
                    pass
        return wires

    def get_average_wire_length(self) -> float:
        """Calculate the average number of hops in the detected proton wires."""
        if not self.path_lengths:
            return 0.0
        return float(np.mean(self.path_lengths))


class HodgeFlowDecomposer:
    """
    Performs discrete 1-form Hodge decomposition on the H-bond network simplicial complex.
    Decomposes an edge flow into gradient (transport), curl (recirculation), and harmonic components.
    """
    def __init__(self):
        self.B1 = None  # 0-1 boundary matrix (nodes x edges)
        self.B2 = None  # 1-2 boundary matrix (edges x triangles)

    def set_boundary_matrices(self, B1: sp.csr_matrix, B2: Optional[sp.csr_matrix] = None):
        """
        Set the boundary matrices for the simplicial complex.
        
        Args:
            B1: Sparse matrix of shape (num_nodes, num_edges).
            B2: Sparse matrix of shape (num_edges, num_triangles). Optional.
        """
        self.B1 = B1
        self.B2 = B2

    def decompose(self, flow: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Decompose the given flow vector on edges.
        
        Args:
            flow: 1D numpy array of shape (num_edges,) representing the edge flow 
                  (e.g., proton hopping velocity or orientation).
                  
        Returns:
            f_grad: Gradient component (net directional transport).
            f_curl: Curl component (local recirculation).
            f_harm: Harmonic component (global circulatory flow).
        """
        if self.B1 is None:
            raise ValueError("Boundary matrix B1 must be set before decomposition.")

        # Gradient component: f_grad = B1^T * phi
        # Solve (B1 * B1^T) phi = B1 * flow
        B1_T = self.B1.T
        L0 = self.B1 @ B1_T
        rhs0 = self.B1 @ flow
        
        # Use least squares or sparse solver
        # Support SciPy >= 1.14 rtol / tol deprecation
        try:
            phi, info0 = spla.minres(L0, rhs0, rtol=1e-6)
        except TypeError:
            phi, info0 = spla.minres(L0, rhs0, tol=1e-6)
        f_grad = B1_T @ phi

        # Curl component: f_curl = B2 * psi
        if self.B2 is not None and self.B2.shape[1] > 0:
            B2_T = self.B2.T
            L2 = B2_T @ self.B2
            rhs2 = B2_T @ flow
            try:
                psi, info2 = spla.minres(L2, rhs2, rtol=1e-6)
            except TypeError:
                psi, info2 = spla.minres(L2, rhs2, tol=1e-6)
            f_curl = self.B2 @ psi
        else:
            f_curl = np.zeros_like(flow)

        # Harmonic component
        f_harm = flow - f_grad - f_curl

        return f_grad, f_curl, f_harm
