"""Learning module for Topological Neural Networks and Physics Discovery."""

__all__ = []

# Optional TNN models (requires topomodelx)
try:
    from .tnn_model import HBondTNN, HBondGNN, train_tnn, prepare_tnn_data
    __all__.extend(["HBondTNN", "HBondGNN", "train_tnn", "prepare_tnn_data"])
except ImportError:
    pass

# Optional: GNN-Enhanced TNN
try:
    from .gnn_enhanced_tnn import (
        GNNEnhancedTNN,
        prepare_gnn_tnn_data,
        train_gnn_enhanced_tnn
    )
    __all__.extend(["GNNEnhancedTNN", "prepare_gnn_tnn_data", "train_gnn_enhanced_tnn"])
except ImportError:
    pass

# Optional: Discovery models (requires pysr, pysindy, etc.)
try:
    from .discovery import SymbolicRegressor, DynamicsIdentifier, HodgeLaplacianGNN
    __all__.extend(["SymbolicRegressor", "DynamicsIdentifier", "HodgeLaplacianGNN"])
except ImportError:
    pass

