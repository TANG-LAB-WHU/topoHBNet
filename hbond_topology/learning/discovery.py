import numpy as np
import pandas as pd
import warnings

try:
    import pysr
    from pysr import PySRRegressor
    HAS_PYSR = True
except ImportError:
    HAS_PYSR = False
    
try:
    import pysindy as ps
    HAS_PYSINDY = True
except ImportError:
    HAS_PYSINDY = False


class SymbolicRegressor:
    """
    Automated discovery of static analytical physical laws using Symbolic Regression (PySR).
    Discovers equations of the form: target = f(features).
    """
    def __init__(self, 
                 niterations=40,
                 binary_operators=["+", "*", "-", "/"],
                 unary_operators=["exp", "sin", "cos", "log"],
                 extra_sympy_mappings=None,
                 model_selection="best",
                 random_state=42,
                 **kwargs):
        """
        Initialize the symbolic regressor.
        
        Args:
            niterations: Number of generations/iterations to run PySR.
            binary_operators: List of binary operations to allow in equations.
            unary_operators: List of unary operations to allow in equations.
            model_selection: 'best' (best loss) or 'accuracy' (simplest accurate model).
        """
        if not HAS_PYSR:
            raise ImportError("PySR is required for SymbolicRegressor. Please install it with 'pip install pysr'.")
            
        self.niterations = niterations
        self.binary_operators = binary_operators
        self.unary_operators = unary_operators
        self.extra_sympy_mappings = extra_sympy_mappings
        self.model_selection = model_selection
        self.random_state = random_state
        self.pysr_kwargs = kwargs
        
        # We initialize the actual model when fit is called, to pass variable names
        self.model = None

    def fit(self, X, y, feature_names=None):
        """
        Fit the symbolic regression model to discover equations.
        
        Args:
            X (pd.DataFrame or np.ndarray): Input topological features (N_samples, N_features).
            y (pd.Series or np.ndarray): Target physical properties (N_samples,).
            feature_names (list of str): Names of the features, if X is an array.
        """
        if isinstance(X, pd.DataFrame):
            if feature_names is None:
                feature_names = X.columns.tolist()
            X_val = X.values
        else:
            X_val = np.asarray(X)
            
        if isinstance(y, (pd.Series, pd.DataFrame)):
            y_val = y.values.ravel()
        else:
            y_val = np.asarray(y).ravel()
            
        # Ensure we don't have NaN or Inf
        mask = np.isfinite(y_val) & np.all(np.isfinite(X_val), axis=1)
        X_val = X_val[mask]
        y_val = y_val[mask]

        if len(y_val) == 0:
            raise ValueError("All input data contained NaN/Inf values.")

        # Setup default physics parameters and allow self.pysr_kwargs to override them
        pysr_params = {
            "niterations": self.niterations,
            "binary_operators": self.binary_operators,
            "unary_operators": self.unary_operators,
            "extra_sympy_mappings": self.extra_sympy_mappings,
            "model_selection": self.model_selection,
            "random_state": self.random_state,
            "elementwise_loss": "loss(prediction, target) = (prediction - target)^2",
            "parsimony": 1e-3
        }
        pysr_params.update(self.pysr_kwargs)

        if self.model is None:
            self.model = PySRRegressor(**pysr_params)
        else:
            # Filter out parameters that are not valid for set_params to support 
            # deprecated parameters (like 'multithreading') which are only absorbed via **kwargs in __init__
            valid_params = self.model.get_params(deep=True)
            filtered_params = {k: v for k, v in pysr_params.items() if k in valid_params}
            self.model.set_params(**filtered_params)
        
        print(f"Starting PySR Symbolic Regression on {X_val.shape[0]} samples with {X_val.shape[1]} features.")
        if feature_names:
            print(f"Features: {', '.join(feature_names)}")
            
        self.model.fit(X_val, y_val, variable_names=feature_names)
        
        return self

    def get_best_equation(self):
        """
        Returns the best discovered equation as a sympy string.
        """
        if self.model is None:
            raise ValueError("Model is not fitted yet.")
        return self.model.sympy()

    def get_pareto_front(self):
        """
        Returns the Pareto front of discovered equations (accuracy vs complexity).
        """
        if self.model is None:
            raise ValueError("Model is not fitted yet.")
        return self.model.equations_


class DynamicsIdentifier:
    """
    Automated discovery of dynamic differential equations using Sparse Identification of Nonlinear Dynamics (SINDy).
    Discovers equations of the form: d(X)/dt = f(X).
    """
    def __init__(self, polynomial_degree=2, include_interaction=True):
        if not HAS_PYSINDY:
            raise ImportError("PySINDy is required for DynamicsIdentifier. Please install it with 'pip install pysindy'.")
            
        self.polynomial_degree = polynomial_degree
        self.include_interaction = include_interaction
        self.model = None

    def fit(self, X_timeseries, t=None, dt=None, feature_names=None):
        """
        Fit SINDy to discover governing differential equations.
        
        Args:
            X_timeseries (np.ndarray): Time-series data of features (N_timepoints, N_features).
            t (np.ndarray): Array of time points.
            dt (float): Uniform time step if t is not provided.
        """
        if t is None and dt is None:
            raise ValueError("Either t or dt must be provided for time-series dynamics.")
            
        if isinstance(X_timeseries, pd.DataFrame):
            if feature_names is None:
                feature_names = X_timeseries.columns.tolist()
            X_val = X_timeseries.values
        else:
            X_val = np.asarray(X_timeseries)

        # Create polynomial library
        library = ps.PolynomialLibrary(degree=self.polynomial_degree, include_interaction=self.include_interaction)
        optimizer = ps.STLSQ(threshold=0.1)  # Sequentially thresholded least squares
        
        self.model = ps.SINDy(
            feature_library=library,
            optimizer=optimizer,
            feature_names=feature_names
        )
        
        self.model.fit(X_val, t=t if t is not None else dt)
        return self

    def print_equations(self):
        if self.model is None:
            raise ValueError("Model is not fitted yet.")
        self.model.print()


class HodgeLaplacianGNN:
    """
    A foundational architecture for building Graph Neural Networks that strictly operate on 
    Hodge-Laplacian matrices, guaranteeing simplicial and topological equivariance.
    Useful for directly learning and predicting gradient/curl flows in the H-bond network.
    """
    def __init__(self):
        try:
            import torch
            import torch.nn as nn
            from torch_geometric.nn import MessagePassing
        except ImportError:
            raise ImportError("PyTorch and PyTorch Geometric are required for HodgeLaplacianGNN.")
        warnings.warn("HodgeLaplacianGNN is a skeleton class meant to be subclassed or implemented dynamically based on specific network structures.")

    # Placeholder for future complex PyTorch / PyG logic 
    def forward(self, x, hodge_laplacian_sparse):
        raise NotImplementedError("Implement the forward pass using torch_sparse or standard dense matmul.")
