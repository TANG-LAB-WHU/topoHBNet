import numpy as np
import pytest
import networkx as nx
import scipy.sparse as sp

from hbond_topology.analysis.proton_dynamics import (
    ProtonTransferProfiler,
    ProtonWireTracker,
    HodgeFlowDecomposer
)

def test_proton_transfer_profiler():
    profiler = ProtonTransferProfiler(temperature=300.0)
    
    # Add normal hbond
    profiler.add_hbond(d_dh=1.0, d_ha=1.8, d_oo=2.8)
    
    # Add LBHB
    profiler.add_hbond(d_dh=1.2, d_ha=1.2, d_oo=2.4)
    
    assert profiler.total_hbonds == 2
    assert profiler.lbhb_count == 1
    assert profiler.get_lbhb_fraction() == 0.5
    
    centers, pmf = profiler.compute_pmf(bins=10, range_val=(-2.0, 2.0))
    assert len(centers) == 10
    assert len(pmf) == 10
    assert np.min(pmf) == 0.0  # PMF minimum is shifted to 0

def test_proton_wire_tracker():
    tracker = ProtonWireTracker()
    
    nodes = [1, 2, 3, 4]
    edges = [
        (1, 2, {'weight': 1.0}),
        (2, 3, {'weight': 1.0}),
        (3, 4, {'weight': 1.0}),
        (1, 4, {'weight': 5.0})
    ]
    
    tracker.update_network(nodes, edges)
    
    # Shortest path from 1 to 4 should be 1->2->3->4 (length 3 hops, weight 3.0)
    # vs 1->4 (length 1 hop, weight 5.0)
    wires = tracker.find_proton_wires(sources=[1], sinks=[4])
    
    assert len(wires) == 1
    assert wires[0] == [1, 2, 3, 4]
    
    avg_len = tracker.get_average_wire_length()
    assert avg_len == 3.0
    
    # Check lifetimes
    assert tuple([1, 2, 3, 4]) in tracker.path_lifetimes
    assert tracker.path_lifetimes[tuple([1, 2, 3, 4])] == 1

def test_hodge_flow_decomposer():
    decomposer = HodgeFlowDecomposer()
    
    # Simple triangle complex
    # Nodes: 0, 1, 2
    # Edges: e0=(0,1), e1=(1,2), e2=(0,2)
    # Triangle: t0=(0,1,2)
    # B1 maps edges to nodes
    # e0: -1 at 0, 1 at 1
    # e1: -1 at 1, 1 at 2
    # e2: -1 at 0, 1 at 2
    
    row1 = [0, 1, 1, 2, 0, 2]
    col1 = [0, 0, 1, 1, 2, 2]
    data1 = [-1, 1, -1, 1, -1, 1]
    B1 = sp.csr_matrix((data1, (row1, col1)), shape=(3, 3))
    
    # B2 maps triangles to edges
    # e0 + e1 - e2 = 0 (boundary of t0)
    row2 = [0, 1, 2]
    col2 = [0, 0, 0]
    data2 = [1, 1, -1]
    B2 = sp.csr_matrix((data2, (row2, col2)), shape=(3, 1))
    
    decomposer.set_boundary_matrices(B1, B2)
    
    # Case 1: Pure gradient flow (e.g. from node potential phi = [0, 1, 2])
    # f = B1^T * phi
    # phi: 0=0, 1=1, 2=2
    # e0: 1-0=1
    # e1: 2-1=1
    # e2: 2-0=2
    flow_grad = np.array([1.0, 1.0, 2.0])
    
    f_g, f_c, f_h = decomposer.decompose(flow_grad)
    np.testing.assert_allclose(f_g, flow_grad, atol=1e-5)
    np.testing.assert_allclose(f_c, np.zeros(3), atol=1e-5)
    np.testing.assert_allclose(f_h, np.zeros(3), atol=1e-5)
    
    # Case 2: Pure curl flow (circulation around the triangle)
    # f = B2 * psi
    # psi = 1
    # e0: 1
    # e1: 1
    # e2: -1
    flow_curl = np.array([1.0, 1.0, -1.0])
    
    f_g, f_c, f_h = decomposer.decompose(flow_curl)
    np.testing.assert_allclose(f_g, np.zeros(3), atol=1e-5)
    np.testing.assert_allclose(f_c, flow_curl, atol=1e-5)
    np.testing.assert_allclose(f_h, np.zeros(3), atol=1e-5)
