# CP2K AIMD Hydrogen Bond Topology Analysis Results

This directory contains the comprehensive analysis results from the `topoHBNet` package applied to a CP2K ab initio molecular dynamics (AIMD) trajectory. The analysis covers hydrogen bond (H-bond) detection, network topology, persistent homology, and topological machine learning.

## Table of Contents

1. [Analysis Overview](#1-analysis-overview)
2. [Data Files](#2-data-files)
3. [Raw Data CSV Files](#3-raw-data-csv-files)
4. [Visualization Outputs](#4-visualization-outputs)
   - 4.1 [H-bond Dynamics](#41-hbond_dynamicspng)
   - 4.2 [Betti Number Dynamics](#42-betti_dynamicspng)
   - 4.3 [H-bond Geometry Distributions](#43-hbond_distributionspng)
   - 4.4 [Coordination and Degree Distributions](#44-coordination_degreepng)
   - 4.5 [H-bond Lifetime Distribution](#45-hbond_lifetimepng)
   - 4.6 [Autocorrelation Function](#46-autocorrelationpng)
   - 4.7 [Radial Distribution Functions](#47-rdf_png-files)
   - 4.8 [Clustering and Strength Classification](#48-clustering_strengthpng)
   - 4.9 [Persistence Barcode](#49-persistence_barcodepng)
   - 4.10 [Persistence Diagram](#410-persistence_diagrampng)
   - 4.11 [Persistence Dynamics](#411-persistence_dynamicspng)
   - 4.12 [Topological ML Visualizations](#412-topological-machine-learning-plots)
5. [Current Analysis Results Summary](#5-current-analysis-results-summary)
6. [Physical Constants and Units](#6-physical-constants-and-units)
7. [H-bond Detection Criteria](#7-h-bond-detection-criteria)
8. [References](#8-references)
9. [Log File](#9-log-file)

---

## 1. Analysis Overview

The analysis pipeline performs the following steps:

1. **H-bond Detection**: Identifies hydrogen bonds using geometric criteria (donor-acceptor distance, hydrogen-acceptor distance, and D-H-A angle)
2. **Topological Analysis**: Constructs simplicial complexes from H-bond networks and computes Betti numbers
3. **Dynamical Analysis**: Tracks H-bond lifetime, autocorrelation, and network clustering
4. **Structural Analysis**: Computes radial distribution functions (RDF) for various atomic pairs
5. **Persistent Homology**: Applies topological data analysis (TDA) to characterize network structure
6. **Topological Machine Learning**: Generates embeddings and extracts features using Cell2Vec and TNN

---

## 2. Data Files

### 2.1 `analysis_results.json`

Per-frame analysis data containing:
- **timestep**: Frame index in the trajectory
- **n_hbonds**: Number of hydrogen bonds detected in each frame
- **betti_0, betti_1, betti_2**: Betti numbers (topological invariants)
- **euler_char**: Euler characteristic of the H-bond network
- **mean_distance_da**: Average donor-acceptor distance (Å)
- **mean_angle_dha**: Average D-H-A angle (degrees)

### 2.2 `statistics_summary.json`

Comprehensive statistical summary including:
- Basic statistics (H-bond count, Betti numbers, geometry)
- Advanced statistics (coordination, degree, lifetime, clustering, H-bond strength)
- Persistent homology summary
- Topological ML results (PCA explained variance)

### 2.3 `frame_embeddings.npy`

NumPy array containing topological embeddings for each frame, generated using the Cell2Vec algorithm. Shape: `(n_frames, embedding_dim)`.

### 2.4 `tnn_features.npy`

NumPy array containing Topological Neural Network (TNN) features extracted using the Simplicial Attention Network (SAN). These features capture higher-order structural information from the H-bond network.

---

## 3. Raw Data CSV Files

The `raw_data_csv/` directory contains detailed numerical data in CSV format for further analysis or custom plotting.

### 3.1 Time Series Data

| File | Description | Columns |
|------|-------------|---------|
| `dynamics_topology.csv` | H-bond count and Betti numbers over time | `time_fs`, `time_ps`, `n_hbonds`, `betti_0`, `betti_1`, `betti_2`, `euler_characteristic` |
| `clustering_coefficient.csv` | Network clustering coefficient time series | `time_fs`, `time_ps`, `clustering_coefficient` |
| `persistence_dynamics.csv` | Persistent homology statistics over time | `frame_idx`, `time_fs`, `time_ps`, `total_persistence_H0`, `total_persistence_H1`, `n_features_H0`, `n_features_H1`, `mean_lifetime_H0`, `mean_lifetime_H1` |
| `property_autocorrelation.csv` | H-bond existence autocorrelation | `lag_time_fs`, `property_acf` |

### 3.2 Distribution Data

| File | Description | Columns |
|------|-------------|---------|
| `coordination_raw_obs.csv` | Raw coordination number observations | `coordination_number` |
| `degree_raw_obs.csv` | Raw node degree observations | `degree` |

### 3.3 Radial Distribution Functions

| File | Description | Columns |
|------|-------------|---------|
| `rdf_O_O.csv` | Oxygen-Oxygen RDF | `r_angstrom`, `g_r` |
| `rdf_O_H.csv` | Oxygen-Hydrogen RDF | `r_angstrom`, `g_r` |
| `rdf_H_H.csv` | Hydrogen-Hydrogen RDF | `r_angstrom`, `g_r` |
| `rdf_La_O.csv` | Lanthanum-Oxygen RDF | `r_angstrom`, `g_r` |
| `rdf_K_O.csv` | Potassium-Oxygen RDF | `r_angstrom`, `g_r` |
| `rdf_P_O.csv` | Phosphorus-Oxygen RDF | `r_angstrom`, `g_r` |

### 3.4 Machine Learning Data

| File | Description | Columns |
|------|-------------|---------|
| `ml_frame_embeddings.csv` | Cell2Vec embeddings per frame | `frame_idx`, `dim_0`, `dim_1`, ..., `dim_N` |
| `ml_pca_components.csv` | PCA projections | `time_fs`, `time_ps`, `PC1`, `PC2` |
| `ml_pca_variance.csv` | PCA explained variance | `component`, `explained_variance_ratio` |
| `ml_similarity_matrix.csv` | Cosine similarity matrix | N×N matrix (no header) |

---

## 4. Visualization Outputs

All figures are provided in both PNG (600 DPI) and SVG (vector) formats.

---

### 4.1 `hbond_dynamics.png`

**Title**: Hydrogen Bond Network Dynamics

**Description**: Time evolution of the total number of hydrogen bonds in the system.

**Variables**:
- **X-axis (Simulation time, fs)**: Time in femtoseconds (1 fs = 10⁻¹⁵ s)
- **Y-axis (Number of H-bonds)**: Total count of hydrogen bonds detected at each frame

**Physical Meaning**:
- Fluctuations reflect the dynamic nature of the H-bond network due to thermal motion
- Steady-state values indicate equilibration of the system
- Large fluctuations may indicate phase transitions or significant structural rearrangements

---

### 4.2 `betti_dynamics.png`

**Title**: Topological Invariants Dynamics

**Description**: Time evolution of Betti numbers, which are fundamental topological invariants describing the "shape" of the H-bond network.

**Variables**:
- **β₀ (Betti-0)**: Number of connected components in the H-bond network
  - *Physical meaning*: Represents the number of isolated H-bond clusters or water clusters that are not connected to each other through H-bonds
  - *Higher values*: More fragmented network with many isolated clusters
  - *Lower values*: More connected, cohesive network

- **β₁ (Betti-1)**: Number of independent loops (1-dimensional holes) in the network
  - *Physical meaning*: Represents cyclic H-bond arrangements (e.g., H-bond rings, pentagonal/hexagonal water rings)
  - *Higher values*: More ring-like structures in the H-bond network
  - *Common in bulk water*: Water often forms pentagonal and hexagonal rings

- **β₂ (Betti-2)**: Number of voids (2-dimensional holes, enclosed cavities)
  - *Physical meaning*: Represents enclosed 3D cavities within the H-bond network
  - *Typically near zero*: Indicates absence of large enclosed voids, consistent with dense liquid structure

---

### 4.3 `hbond_distributions.png`

**Title**: Hydrogen Bond Geometry Distributions

**Description**: Statistical distributions of the three geometric parameters defining H-bonds.

**Variables**:

- **D-A Distance (Donor-Acceptor Distance, Å)**:
  - Distance between the oxygen atom donating the H-bond and the oxygen atom accepting it
  - *Typical range*: 2.5–3.5 Å
  - *Peak position*: Indicates the most probable H-bond length
  - *Distribution width*: Reflects thermal fluctuations and H-bond strength variability

- **H-A Distance (Hydrogen-Acceptor Distance, Å)**:
  - Distance between the hydrogen atom and the acceptor oxygen
  - *Typical range*: 1.5–2.5 Å
  - *Shorter distances*: Stronger H-bonds

- **D-H-A Angle (degrees)**:
  - Angle formed by donor oxygen, hydrogen, and acceptor oxygen
  - *Ideal value*: 180° (linear H-bond)
  - *Typical range*: 120°–180°
  - *Higher angles*: More linear and generally stronger H-bonds

---

### 4.4 `coordination_degree.png`

**Title**: Coordination Number and Degree Distribution

**Description**: Network-based distributions characterizing how water molecules participate in H-bonding.

**Variables**:

- **Coordination Number**:
  - Number of H-bonds each water molecule participates in (as donor or acceptor)
  - *Physical meaning*: Describes the local H-bond environment of each water molecule
  - *In bulk water*: Typically 3–4 (tetrahedral coordination)
  - *Distribution shape*: Indicates heterogeneity in local environments

- **Node Degree**:
  - Same as coordination number in this context (number of H-bond connections per oxygen atom)
  - *Mean value*: Average connectivity in the H-bond network
  - *High connectivity*: More robust, interconnected network

---

### 4.5 `hbond_lifetime.png`

**Title**: Hydrogen Bond Lifetime Distribution

**Description**: Distribution of H-bond lifetimes, measuring how long individual H-bonds persist before breaking.

**Variables**:
- **X-axis (H-bond Lifetime, fs)**: Duration that a specific donor-acceptor pair maintains an H-bond
- **Y-axis (Count)**: Frequency of H-bonds with given lifetime

**Physical Meaning**:
- **Short lifetimes (< 50 fs)**: Transient, weak H-bonds
- **Mean lifetime**: Characteristic timescale for H-bond dynamics
- **Long tail**: Presence of particularly stable H-bonds
- *Typical bulk water lifetime*: ~1-2 ps (1000-2000 fs)

---

### 4.6 `autocorrelation.png`

**Title**: H-bond Autocorrelation Function

**Description**: Time correlation function C(t) measuring how H-bond patterns persist over time.

**Variables**:
- **X-axis (Time lag, fs)**: Time difference between observations
- **Y-axis (C(t))**: Autocorrelation value, ranging from 1 (perfectly correlated) to 0 (uncorrelated)

**Physical Meaning**:
- **C(t) = ⟨h(0)h(t)⟩ / ⟨h(0)²⟩** where h(t) = 1 if H-bond exists at time t
- **Decay rate**: Indicates how quickly H-bond memory is lost
- **1/e crossing**: Characteristic correlation time (τ)
- **Exponential decay**: Single-mode relaxation
- **Non-exponential decay**: Multiple relaxation processes

---

### 4.7 `rdf_*.png` Files

**Title**: Radial Distribution Functions

**Description**: Probability of finding atom pairs at distance r, normalized to bulk density.

**Files**:
- `rdf_O_O.png`: Oxygen-Oxygen RDF
- `rdf_O_H.png`: Oxygen-Hydrogen RDF
- `rdf_H_H.png`: Hydrogen-Hydrogen RDF
- `rdf_La_O.png`: Lanthanum-Oxygen RDF (if La present)
- `rdf_K_O.png`: Potassium-Oxygen RDF (if K present)
- `rdf_P_O.png`: Phosphorus-Oxygen RDF (if P present)

**Variables**:
- **X-axis (r, Å)**: Distance between atomic pairs
- **Y-axis (g(r))**: Radial distribution function value

**Physical Meaning**:
- **g(r) = 1**: Random (ideal gas) distribution
- **g(r) > 1**: Enhanced probability (preferred distances)
- **g(r) < 1**: Depleted probability (exclusion zones)
- **First peak position**: Characteristic bond or contact distance
- **Peak height**: Structural ordering strength

**Typical Features for Water**:
- **O-O first peak (~2.8 Å)**: H-bonded O-O distance
- **O-O second peak (~4.5 Å)**: Second coordination shell
- **O-H first peak (~1.0 Å)**: Covalent O-H bond
- **O-H second peak (~1.8 Å)**: H-bonded H...O distance

---

### 4.8 `clustering_strength.png`

**Title**: Network Clustering Coefficient and H-bond Strength Classification

**Description**: Two-panel figure showing network topology and H-bond strength distribution.

**Left Panel - Clustering Coefficient**:
- **Definition**: C = (3 × triangles) / (connected triples)
- **Physical meaning**: Measures tendency of H-bonds to form triangular motifs (loops of 3 connected waters)
- **Range**: 0 (no clustering) to 1 (maximum clustering)
- **Time evolution**: Shows structural fluctuations

**Right Panel - H-bond Strength Pie Chart**:
- **Strong H-bonds (D-A < 2.8 Å)**: Short, strong interactions; typically ~40%
- **Moderate H-bonds (2.8 ≤ D-A < 3.2 Å)**: Intermediate strength; typically ~45-50%
- **Weak H-bonds (D-A ≥ 3.2 Å)**: Long, weak interactions; typically ~10-15%

---

### 4.9 `persistence_barcode.png`

**Title**: Persistence Barcode

**Description**: Topological Data Analysis (TDA) visualization showing the "birth" and "death" of topological features as the distance threshold (ε) increases.

**Variables**:
- **X-axis (ε, Å)**: Distance threshold (filtration parameter)
- **Horizontal bars**: Each bar represents one topological feature
- **Bar start (Birth)**: Distance at which the feature first appears
- **Bar end (Death)**: Distance at which the feature disappears (merges or fills in)
- **Bar length (Persistence)**: Death - Birth; measures feature significance

**Color Coding**:
- **Blue (H0)**: Connected components
- **Red (H1)**: Loops/rings

**Physical Meaning**:
- **Long H0 bars**: Persistent, well-separated clusters
- **Short H0 bars**: Quickly merging components
- **H1 bars**: Ring structures at specific distance scales
- **Persistence**: Features with longer bars are more "real" (not noise)

---

### 4.10 `persistence_diagram.png`

**Title**: Persistence Diagram

**Description**: Alternative TDA visualization plotting birth vs. death times for each topological feature.

**Variables**:
- **X-axis (Birth, ε)**: Distance at which feature appears
- **Y-axis (Death, ε)**: Distance at which feature disappears
- **Diagonal line**: Birth = Death (features on this line have zero persistence)
- **Distance from diagonal**: Persistence (significance) of the feature

**Color Coding**:
- **Blue points (H0)**: Connected components
- **Red points (H1)**: Loops/rings

**Physical Meaning**:
- **Points far from diagonal**: Significant, persistent topological features
- **Points near diagonal**: Noise or transient features
- **Cluster of H0 points**: Characteristic inter-cluster distances
- **H1 points**: Ring formation scales

---

### 4.11 `persistence_dynamics.png`

**Title**: Persistence Dynamics (All Frames)

**Description**: Time evolution of persistent homology statistics computed for every frame.

**Four Panels**:

1. **Total Persistence Over Time**:
   - Sum of all bar lengths (persistence values) for H0 and H1
   - *Physical meaning*: Overall topological complexity of the network

2. **Topological Feature Count**:
   - Number of H0 components and H1 loops detected
   - *Physical meaning*: Structural richness at each time point

3. **Mean Feature Lifetime**:
   - Average persistence (death - birth) for features
   - *Physical meaning*: Typical "robustness" of topological features

4. **H1/H0 Persistence Ratio**:
   - Ratio of loop persistence to component persistence
   - *Physical meaning*: Balance between ring formation and clustering
   - *Higher values*: More ring-dominated topology
   - *Lower values*: More fragmented, cluster-dominated topology

---

### 4.12 Topological Machine Learning Plots

#### `similarity_heatmap.png`

**Title**: Inter-Frame Topological Similarity

**Description**: Heatmap showing cosine similarity between frame embeddings.

**Variables**:
- **X and Y axes (Simulation time, ps)**: Time coordinates
- **Color intensity**: Cosine similarity (0 to 1)
- **Diagonal**: Always 1 (self-similarity)

**Physical Meaning**:
- **High similarity (bright)**: Similar H-bond network topology
- **Low similarity (dark)**: Different network structures
- **Block patterns**: Temporal regimes with consistent topology
- **Gradual transitions**: Continuous structural evolution

---

#### `embedding_pca.png`

**Title**: PCA of Topological Embeddings

**Description**: Principal Component Analysis projection of frame embeddings into 2D space.

**Variables**:
- **PC1, PC2**: First two principal components
- **Explained variance (%)**: Fraction of total variance captured
- **Color (Frame Index)**: Time progression through trajectory

**Physical Meaning**:
- **Clustering**: Frames with similar topology group together
- **Trajectory in PC space**: Shows structural evolution
- **PC1/PC2**: Dominant modes of topological variation
- **Spread**: Diversity of H-bond network structures sampled

---

#### `pca_time_series.png`

**Title**: PCA Components Evolution

**Description**: Time series of the first two principal components.

**Variables**:
- **X-axis (Simulation time, ps)**: Time in picoseconds
- **Y-axis (PC value)**: Principal component projection value

**Physical Meaning**:
- **PC1 evolution**: Dominant structural changes over time
- **PC2 evolution**: Secondary structural variations
- **Oscillations**: Reversible structural fluctuations
- **Trends**: Systematic structural drift (equilibration or transitions)
- **Correlation between PCs**: Coupled vs. independent structural modes

---

## 5. Current Analysis Results Summary

This section provides key findings from the present CP2K AIMD trajectory analysis:

### 5.1 System Information
- **Frames analyzed**: 501
- **Sampling**: Every frame from trajectory
- **Timestep**: 0.5 fs

### 5.2 H-bond Network Statistics

| Property | Mean | Std | Min | Max |
|----------|------|-----|-----|-----|
| H-bonds per frame | 30.0 | 3.1 | 19 | 37 |
| Coordination number | 1.68 | 0.75 | - | - |
| H-bond lifetime | 121.0 fs | 95.3 fs | - | 250.5 fs |
| Clustering coefficient | 0.018 | 0.036 | - | - |

### 5.3 Betti Numbers (Topological Invariants)

| Invariant | Mean | Std | Physical Interpretation |
|-----------|------|-----|------------------------|
| β₀ | 6.6 | 0.9 | ~6-7 disconnected H-bond clusters |
| β₁ | 0.7 | 0.4 | <1 loop on average (sparse ring structure) |
| β₂ | 0.0 | 0.0 | No enclosed cavities (dense liquid) |

### 5.4 H-bond Geometry

| Parameter | Mean | Std | Range |
|-----------|------|-----|-------|
| D-A distance | 2.90 Å | 0.23 Å | - |
| D-H-A angle | 158.0° | 13.6° | - |

### 5.5 H-bond Strength Classification

| Category | Criterion | Percentage |
|----------|-----------|------------|
| Strong | D-A < 2.8 Å | 40.1% |
| Moderate | 2.8 ≤ D-A < 3.2 Å | 46.5% |
| Weak | D-A ≥ 3.2 Å | 13.4% |

### 5.6 Persistent Homology Summary

| Metric | H0 (Components) | H1 (Loops) |
|--------|-----------------|------------|
| Total persistence (mean) | 445.6 Å | 44.5 Å |
| Number of features (mean) | 162 | 78.9 |

### 5.7 Topological Machine Learning

| PCA Component | Explained Variance |
|---------------|-------------------|
| PC1 | 17.0% |
| PC2 | 14.0% |
| **Total (PC1+PC2)** | **31.0%** |

---

## 6. Physical Constants and Units

| Quantity | Unit | Conversion |
|----------|------|------------|
| Distance | Å (Angstrom) | 1 Å = 10⁻¹⁰ m |
| Time | fs (femtosecond) | 1 fs = 10⁻¹⁵ s |
| Time | ps (picosecond) | 1 ps = 1000 fs |
| Angle | degrees | 180° = π radians |

---

## 7. H-bond Detection Criteria

The default geometric criteria for H-bond detection:
- **Donor-Acceptor distance**: ≤ 3.5 Å
- **Hydrogen-Acceptor distance**: ≤ 2.5 Å
- **D-H-A angle**: ≥ 120°

---

## 8. References

1. **Betti Numbers**: Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*.
2. **Persistent Homology**: Carlsson, G. (2009). *Topology and Data*. Bulletin of the AMS.
3. **Water H-bond Networks**: Luzar, A., & Chandler, D. (1996). *Nature*, 379, 55-57.
4. **RDF Interpretation**: Allen, M. P., & Tildesley, D. J. (2017). *Computer Simulation of Liquids*.

---

## 9. Log File

`topoHBNet_analysis_*.log` contains the complete analysis log with timing information, intermediate results, and any warnings encountered during the analysis.
