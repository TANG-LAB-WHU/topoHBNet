"""Learning module for Topological Neural Networks and Physics Discovery."""

__all__ = [
    "HBondTNN", "HBondGNN", "train_tnn", "prepare_tnn_data", 
    "GNNEnhancedTNN", "prepare_gnn_tnn_data", "train_gnn_enhanced_tnn",
    "SymbolicRegressor", "DynamicsIdentifier", "HodgeLaplacianGNN"
]

def __getattr__(name):
    if name in ["HBondTNN", "HBondGNN", "train_tnn", "prepare_tnn_data"]:
        from .tnn_model import HBondTNN, HBondGNN, train_tnn, prepare_tnn_data
        if name == "HBondTNN": return HBondTNN
        if name == "HBondGNN": return HBondGNN
        if name == "train_tnn": return train_tnn
        if name == "prepare_tnn_data": return prepare_tnn_data
        
    elif name in ["GNNEnhancedTNN", "prepare_gnn_tnn_data", "train_gnn_enhanced_tnn"]:
        from .gnn_enhanced_tnn import GNNEnhancedTNN, prepare_gnn_tnn_data, train_gnn_enhanced_tnn
        if name == "GNNEnhancedTNN": return GNNEnhancedTNN
        if name == "prepare_gnn_tnn_data": return prepare_gnn_tnn_data
        if name == "train_gnn_enhanced_tnn": return train_gnn_enhanced_tnn
        
    elif name in ["SymbolicRegressor", "DynamicsIdentifier", "HodgeLaplacianGNN"]:
        from .discovery import SymbolicRegressor, DynamicsIdentifier, HodgeLaplacianGNN
        if name == "SymbolicRegressor": return SymbolicRegressor
        if name == "DynamicsIdentifier": return DynamicsIdentifier
        if name == "HodgeLaplacianGNN": return HodgeLaplacianGNN
        
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
