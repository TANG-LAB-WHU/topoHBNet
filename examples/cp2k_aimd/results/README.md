# CP2K AIMD Analysis Results

This directory contains the output files from the `example_analysis.py` script, which performs a comprehensive topological and dynamical analysis of the hydrogen bond network in your AIMD trajectory.

---

## 1. Summary Data Files

### `analysis_results.json`
**Content**: Detailed time-series data for every analyzed frame.
- **`frame`**: Frame index and simulation time.
- **`n_hbonds`**: Total number of hydrogen bonds detected in the frame.
- **`hbonds`**: List of individual H-bonds with atom indices (Donor, Hydrogen, Acceptor) and geometric parameters (D–A distance, D–H–A angle).
- **`graph_stats`**: Network topology statistics (clustering coefficient, average path length, etc.).
- **`betti_numbers`**: Topological invariants (β₀, β₁, β₂) representing connected components, cycles, and cavities.

### `statistics_summary.json`
**Content**: Global statistical summary averaged over the entire trajectory.
- **`basic_statistics`**: Mean and standard deviation of H-bond counts and geometry.
- **`advanced_statistics`**:
  - **Coordination**: Average number of H-bonds per water molecule.
  - **Lifetime**: Mean H-bond lifetime (in femtoseconds).
  - **Clustering**: Network clustering coefficient.
  - **H-bond Strength**: Percentage distribution of Strong, Moderate, and Weak bonds.

---

## 2. Raw ML Data (when run with `--run-ml`)

| File | Description |
|------|-------------|
| **`frame_embeddings.npy`** | Per-frame topological embeddings (e.g. Cell2Vec) of the H-bond network; shape `(n_frames, embedding_dim)`. Used for similarity and PCA plots. |
| **`tnn_features.npy`** | Topological Neural Network (TNN) features per frame, when available. |

---

## 3. Visualization Plots & Physical Meaning

### 3.1 Dynamical Properties

| Figure | File | Physical meaning |
|--------|------|-------------------|
| **H-bond count vs time** | `hbond_dynamics.png` | Time evolution of the total number of H-bonds. Reflects global network stability and fluctuations; plateaus indicate a stable liquid phase, strong oscillations may indicate phase changes or finite-size effects. |
| **H-bond lifetime** | `hbond_lifetime.png` | Decay of the continuous H-bond autocorrelation function *C*(*t*). The characteristic decay time is the average H-bond lifetime. **Physical meaning**: Shorter decay → faster breaking/reforming (higher mobility, higher *T* or lower viscosity); longer decay → more persistent H-bond network (e.g. colder or more structured liquid). |
| **Property autocorrelation** | `autocorrelation.png` | Autocorrelation of a chosen network property (e.g. H-bond count) with lag time. **Physical meaning**: Measures the “memory” of the topological state; decay time indicates how long the system retains correlation (structural relaxation timescale). |

### 3.2 Topological Invariants (Persistent Homology)

| Figure | File | Physical meaning |
|--------|------|-------------------|
| **Betti numbers vs time** | `betti_dynamics.png` | Time evolution of β₀, β₁, β₂. **β₀**: number of connected components (H-bond clusters); in bulk water typically one large component. **β₁**: number of 1D cycles (rings/loops in the network); reflects ring structure (4-, 5-, 6-member rings). **β₂**: number of 2D cavities (voids); relates to free volume and packing. |
| **Persistence barcode** | `persistence_barcode.png` | Lifespan of topological features vs. filtration parameter ε (e.g. distance threshold). **Physical meaning**: Long bars = robust, persistent structures (e.g. stable rings or cavities); short bars = noise or transient fluctuations. Horizontal axis is “scale”; only features that persist over a range of ε are structurally meaningful. |
| **Persistence diagram** | `persistence_diagram.png` | Birth vs. death of topological features (2D scatter). **Physical meaning**: Points far from the diagonal (birth ≪ death) are persistent; points near the diagonal are short-lived. Used to compare different systems or time windows (e.g. via persistence-based metrics). |

### 3.3 Structural & Geometric Distributions

| Figure | File | Physical meaning |
|--------|------|-------------------|
| **H-bond geometry** | `hbond_distributions.png` | Histograms of D–A distance *r*DA, H–A distance *r*HA, and D–H–A angle θ. **Physical meaning**: Peaks show typical H-bond geometry; narrow distributions indicate well-defined bonding; broadening at high *T* or in complex environments (e.g. ions, interfaces). |
| **Coordination & degree** | `coordination_degree.png` | **Left**: Distribution of coordination number (H-bonds per molecule). **Right**: Degree distribution *P*(*k*) of the H-bond graph. **Physical meaning**: In liquid water, coordination ~2–4 is typical; tetrahedral order gives a peak near 4; ions or defects can shift or broaden the distribution. |
| **Clustering & strength** | `clustering_strength.png` | **Clustering coefficient**: Fraction of possible triangles that exist (local “clique-ness”). **Strength pie chart**: Proportion of Strong / Moderate / Weak H-bonds by geometric criteria. **Physical meaning**: Higher clustering → more local order; strength distribution reflects how “ideal” vs. distorted the H-bonds are on average. |

### 3.4 Radial Distribution Functions (RDFs)

RDF *g*(*r*) gives the probability of finding a pair at distance *r* relative to an ideal gas; peaks correspond to solvation shells or preferred pair distances.

| Figure | File | Physical meaning |
|--------|------|-------------------|
| **O–O** | `rdf_O_O.png` | Oxygen–oxygen pair. **Physical meaning**: First peak ~2.8 Å = first solvation shell (nearest-neighbor waters); second peak = second shell; structure reflects liquid order (e.g. tetrahedral vs. more disordered). |
| **O–H** | `rdf_O_H.png` | Oxygen–hydrogen (donor–acceptor H-bond direction). **Physical meaning**: First peak ~1.8–2.0 Å = typical H-bond length; integral relates to H-bond count and coordination. |
| **H–H** | `rdf_H_H.png` | Hydrogen–hydrogen. **Physical meaning**: Reflects H–H distances within and between water molecules (e.g. within same molecule vs. across H-bonds); sensitive to molecular geometry and packing. |
| **La–O** | `rdf_La_O.png` | Lanthanum–oxygen. **Physical meaning**: Solvation structure around La³⁺; first peak = coordination shell; number of coordinated waters and distances indicate ion–water interaction strength. |
| **K–O** | `rdf_K_O.png` | Potassium–oxygen. **Physical meaning**: Solvation of K⁺; typically weaker than La³⁺, larger first-shell distance; useful for comparing cation effects. |
| **P–O** | `rdf_P_O.png` | Phosphorus–oxygen (e.g. phosphate/phosphonate). **Physical meaning**: P–water oxygen distances; first peak = hydration shell around P; relevant for phosphates, lipids, or phosphate ions in solution. |

### 3.5 Topological Machine Learning (TML, with `--run-ml`)

| Figure | File | Physical meaning |
|--------|------|-------------------|
| **Similarity heatmap** | `similarity_heatmap.png` | Pairwise cosine similarity of per-frame topological embeddings (e.g. Cell2Vec) vs. simulation time (ps × ps). **Physical meaning**: Bright diagonal = frames similar to themselves; bands parallel to diagonal = periods of similar topology (e.g. similar H-bond network structure); blocks or stripes indicate phases or recurring structural motifs along the trajectory. |
| **Embedding PCA** | `embedding_pca.png` | PCA of frame embeddings in 2D (PC1 vs. PC2), points colored by frame index. **Physical meaning**: Proximity in this space = similar global topology; clusters = distinct “topological states”; spread along PC1/PC2 = main modes of variation in H-bond network structure. |
| **PCA time series** | `pca_time_series.png` | PC1 and PC2 vs. simulation time (ps). **Physical meaning**: Evolution of the dominant topological modes; smooth variation = gradual structural change; jumps or plateaus = transitions or metastable states; useful for identifying regimes (e.g. equilibration vs. production, or different conformations). |

---

## 4. Quick Reference: File Inventory

| Category | Files |
|----------|--------|
| **JSON** | `analysis_results.json`, `statistics_summary.json` |
| **Dynamics** | `hbond_dynamics.png`, `hbond_lifetime.png`, `autocorrelation.png` |
| **Topology** | `betti_dynamics.png`, `persistence_barcode.png`, `persistence_diagram.png` |
| **Distributions** | `hbond_distributions.png`, `coordination_degree.png`, `clustering_strength.png` |
| **RDFs** | `rdf_O_O.png`, `rdf_O_H.png`, `rdf_H_H.png`, `rdf_La_O.png`, `rdf_K_O.png`, `rdf_P_O.png` |
| **TML (optional)** | `similarity_heatmap.png`, `embedding_pca.png`, `pca_time_series.png`, `frame_embeddings.npy`, `tnn_features.npy` |

---

## 5. Interpretation Tips

- **High β₁ (many cycles)**: Liquid-like network with many closed H-bond rings; typical of bulk water.
- **High coordination (~4)**: Tetrahedral-like order (ice-like or structured liquid); lower values suggest broken network or interfaces.
- **Fast H-bond lifetime decay**: High mobility, frequent H-bond breaking/reforming (e.g. high temperature or low viscosity).
- **Persistent bars in barcode / points far from diagonal in persistence diagram**: Structurally robust features; short bars or near-diagonal points are usually noise.
- **TML**: Use similarity heatmap and PCA time series to segment the trajectory into topologically similar segments and to spot transitions or recurring states.
