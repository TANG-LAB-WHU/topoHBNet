"""
This package provides tools for analyzing hydrogen bond network topology
from LAMMPS molecular dynamics trajectories using TopoNetX, TopoModelX,
and TopoEmbedX libraries.
"""

__version__ = "0.3.0"
__author__ = "SIQI TANG"

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
]

# Optional: Embedding module (requires topoembedx)
try:
    from .embedding.embedder import HBondEmbedder
    __all__.append("HBondEmbedder")
except ImportError:
    pass

# Optional: Persistence module (requires gudhi)
try:
    from .topology.persistence import PersistenceAnalyzer
    __all__.append("PersistenceAnalyzer")
except ImportError:
    pass

# Optional: Physics Discovery module (requires pysr, pysindy, etc.)
# NOTE: Imported before the deep learning module to ensure juliacall is loaded before torch,
# which completely eliminates the Torch/JuliaCall dynamic library loading order segfault risk.
try:
    from .learning.discovery import SymbolicRegressor, DynamicsIdentifier, HodgeLaplacianGNN
    __all__.extend(["SymbolicRegressor", "DynamicsIdentifier", "HodgeLaplacianGNN"])
except ImportError:
    pass

# Optional: Learning module (requires topomodelx)
try:
    from .learning.tnn_model import HBondTNN
    __all__.append("HBondTNN")
except ImportError:
    pass

