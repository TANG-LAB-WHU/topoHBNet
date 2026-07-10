"""
This package provides tools for analyzing hydrogen bond network topology
from LAMMPS molecular dynamics trajectories using TopoNetX, TopoModelX,
and TopoEmbedX libraries.
"""

__version__ = "0.4.0"
__author__ = "SIQI TANG"

# To avoid a known segmentation fault caused by loading PyTorch before JuliaCall,
# we attempt to import PySR/juliacall first if they exist in the environment.
# See: https://github.com/pytorch/pytorch/issues/78829
try:
    import pysr
except ImportError:
    try:
        import juliacall
    except ImportError:
        pass


# Core modules (always available)
from .io.trajectory_parser import TrajectoryParser
from .detection.hbond_detector import HBondDetector
from .topology.complex_builder import HBondComplexBuilder
from .topology.invariants import TopologicalInvariants
from .analysis.dynamics import DynamicsAnalyzer
from .analysis.visualization import TopologyVisualizer
from .analysis.interfacial import InterfacialAnalyzer, InterfacialVisualizer, InterfacialAnalysisResult
from .analysis.proton_dynamics import ProtonTransferProfiler, ProtonWireTracker, HodgeFlowDecomposer

__all__ = [
    "TrajectoryParser",
    "HBondDetector", 
    "HBondComplexBuilder",
    "TopologicalInvariants",
    "DynamicsAnalyzer",
    "TopologyVisualizer",
    "InterfacialAnalyzer",
    "InterfacialVisualizer",
    "InterfacialAnalysisResult",
    "ProtonTransferProfiler",
    "ProtonWireTracker",
    "HodgeFlowDecomposer",
    "HBondEmbedder",
    "PersistenceAnalyzer",
    "SymbolicRegressor",
    "DynamicsIdentifier",
    "HodgeLaplacianGNN",
    "HBondTNN",
]

# Lazy loading for heavy optional modules (PEP 562)
# This prevents Torch/JuliaCall segfaults and massive thread contention slowdowns
# by ensuring they are only loaded when explicitly requested, not on every import.
def __getattr__(name):
    if name == "HBondEmbedder":
        from .embedding.embedder import HBondEmbedder
        return HBondEmbedder
    elif name == "PersistenceAnalyzer":
        from .topology.persistence import PersistenceAnalyzer
        return PersistenceAnalyzer
    elif name in ["SymbolicRegressor", "DynamicsIdentifier", "HodgeLaplacianGNN"]:
        # NOTE: To avoid a known segmentation fault caused by loading PyTorch before JuliaCall,
        # we ensure pysr/juliacall is loaded before torch if both are used.
        try:
            import pysr
        except ImportError:
            try:
                import juliacall
            except ImportError:
                pass
        from .learning.discovery import SymbolicRegressor, DynamicsIdentifier, HodgeLaplacianGNN
        return locals()[name]
    elif name == "HBondTNN":
        from .learning.tnn_model import HBondTNN
        return HBondTNN
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
