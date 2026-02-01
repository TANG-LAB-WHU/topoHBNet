# CP2K AIMD Analysis Results

This directory contains the output files from the `example_analysis.py` script, which performs a comprehensive topological and dynamical analysis of the hydrogen bond network in your AIMD trajectory.

## 1. Summary Data Files

### `analysis_results.json`
**Content**: detailed time-series data for every analyzed frame.
- **`frame`**: Frame index and simulation time.
- **`n_hbonds`**: Total number of hydrogen bonds detected in the frame.
- **`hbonds`**: List of individual H-bonds with atom indices (Donor, Hydrogen, Acceptor) and geometric parameters (D-A distance, D-H-A angle).
- **`graph_stats`**: Network topology statistics (clustering coefficient, average path length, etc.).
- **`betti_numbers`**: Topological invariants ($\beta_0, \beta_1, \beta_2$) representing connected components, cycles, and cavities.

### `statistics_summary.json`
**Content**: Global statistical summary averaged over the entire trajectory.
- **`basic_statistics`**: Mean and standard deviation of H-bond counts and geometry.
- **`advanced_statistics`**:
    - **Coordination**: Average number of H-bonds per water molecule.
    - **Lifetime**: Mean H-bond lifetime (in femtoseconds).
    - **Clustering**: Network clustering coefficient.
    - **H-bond Strength**: Percentage distribution of Strong, Moderate, and Weak bonds.

---

## 2. Visualization & Analysis Plots

### Dynamical Properties
- **`hbond_dynamics.png`**: Time evolution of the total number of hydrogen bonds. Shows global network fluctuations and stability.
- **`hbond_lifetime.png`**: Decay of the Continuous H-bond Autocorrelation Function $C(t)$. The characteristic decay time corresponds to the average H-bond lifetime.
- **`autocorrelation.png`**: Autocorrelation of network properties, indicating the memory time of the topological state.

### Topological Invariants (Topological Data Analysis)
- **`betti_dynamics.png`**: Time evolution of Betti numbers:
    - $\beta_0$: Number of connected components (clusters of H-bonded molecules).
    - $\beta_1$: Number of 1D cycles (loops) in the network.
    - $\beta_2$: Number of 2D cavities (voids).
- **`persistence_barcode.png`**: Persistence barcode showing the lifespan of topological features (cycles, cavities) as a function of filtration parameter (e.g., bond distance). Long bars represent significant, robust features; short bars represent noise.
- **`persistence_diagram.png`**: 2D scatter plot representation of birth vs. death times of topological features. Points far from the diagonal indicate persistent structures.

### Structural Distributions
- **`hbond_distributions.png`**: Histograms of H-bond geometric parameters:
    - Donor-Acceptor Distance ($r_{DA}$)
    - Hydrogen-Acceptor Distance ($r_{HA}$)
    - Donor-Hydrogen-Acceptor Angle ($\theta_{DHA}$)
- **`coordination_degree.png`**:
    - **Coordination Number**: Distribution of the number of H-bonds per molecule (e.g., how many water molecules have 2, 3, or 4 partners).
    - **Degree Distribution**: Node degree probability $P(k)$ of the H-bond graph.
- **`clustering_strength.png`**:
    - **Clustering Coefficient**: Measure of "clique-iness" (triangles) in the graph.
    - **Strength Classification**: Pie chart of H-bond populations categorized by geometric criteria (Strong vs. Weak).

### Radial Distribution Functions (RDF)
- **`rdf_*.png`** (e.g., `rdf_O_O.png`, `rdf_O_H.png`): Radial distribution functions $g(r)$ between atomic pairs.
    - Peaks indicate preferred interaction distances (solvation shells).
    - **O-O**: Structure of the water/liquid oxygen network.
    - **O-H / H-H**: Hydrogen bonding signatures.
    - **Ion-O** (e.g., `rdf_La_O.png`): Solvation structure around ions if present.

---

## 3. Physical Interpretation Guide

- **High $\beta_1$ (Cycles)**: Indicates a "liquid-like" network with many closed loops, typical of bulk water.
- **High Coordination (~4)**: Indicates tetrahedral ordering (ice-like or structured liquid). Lower values imply broken networks or interfaces.
- **Fast Decay in Lifetime**: Indicates high molecular mobility and frequent H-bond breaking/reforming (high temperature or low viscosity).

### Topological Features (H0 & H1)
- **H0 (Connected Components)**: Represents independent clusters of molecules connected by hydrogen bonds.
    - **Physical Meaning**: Describes the connectivity of the network. Short bars in the barcode indicate transient connections, while long bars (or infinite ones) represent stable, persistent clusters. In bulk liquid water, all molecules eventually form a single giant connected component.
- **H1 (1D Loops / Cycles)**: Represents one-dimensional holes or closed loops within the network (e.g., 4-, 5-, or 6-membered rings formed by H-bonded molecules).
    - **Physical Meaning**: Characterizes the ring structure of the liquid.
        - **Birth**: Formation of a new closed loop.
        - **Death**: Filling of the loop (e.g., by cross-linking) or merging into a denser structure.
        - **Significance**: Persistent loops (long bars) suggest robust structural motifs (like stable cages or channels), whereas short-lived loops indicate the rapid flickering of the dynamic hydrogen bond network.
