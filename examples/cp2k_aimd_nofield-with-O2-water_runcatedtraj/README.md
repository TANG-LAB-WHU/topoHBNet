# CP2K AIMD: No Field with O2 in Water

This directory contains a complete workflow for analyzing an ab initio molecular dynamics (AIMD) trajectory of water on a substrate (e.g., Si/C surface) using the `topoHBNet` package.

> [!NOTE]
> These six analysis workflows are completely independent. They can be executed in any order (or even concurrently in parallel), as each script only processes the raw output files from the CP2K MD simulation (`trajectory.xyz`, `trajectory.cell`, and `trajectory.ener`) or correlates their outputs, and does not depend on the outputs of the other scripts (except the correlation script, which bridges the main topological ML and proton transfer outputs).

The example demonstrates six complementary analysis workflows:

1. **Hydrogen Bond Network Topology** (`topoHBNet_main_analysis.py`)
2. **Reactive Species Stoichiometry** (`trajectory_species_analysis.py`)
3. **Simulation Energetics & Stability** (`visualizing_aimd_energetics.py`)
4. **Interfacial Water & Surface Analysis** (`interfacial_water_analysis.py`)
5. **Proton Transfer & Dynamics Analysis** (`proton_transfer_analysis.py`)
6. **Bridge: Topology-Transport Correlation** (`correlate_topology_and_transport.py`)

---

## 1. Topological H-Bond Network Analysis

**Script**: `topoHBNet_main_analysis.py`

This is the central analysis script utilizing the core `topoHBNet` library. It maps the H-bond network as a topological complex and calculates invariants.

- **Key Features**:
  - H-bond counting and dynamics (lifetime, autocorrelation).
  - **Topological Invariants**: Betti numbers ($\beta_0, \beta_1, \beta_2$) and Euler characteristic.
  - **Persistent Homology (TDA)**: Barcodes and persistence diagrams to identify stable vs. transient H-bond loops.
  - **Topological Machine Learning**: TNN feature extraction, topological embeddings, and PCA visualization (enabled with `--run-ml`).
- **Primary Outputs**:
  - `topoHBNet-no_run-ml/` (contains topological analysis results without machine learning)
  - `topoHBNet-run-ml/` (contains topological analysis results with machine learning enabled)
- **Usage**:
  - **To generate topological analysis results without machine learning (`topoHBNet-no_run-ml/`):**
    ```bash
    python topoHBNet_main_analysis.py --trajectory trajectory.xyz --cell-file trajectory.cell --output-dir topoHBNet-no_run-ml
    ```
  - **To generate topological analysis results with machine learning enabled (`topoHBNet-run-ml/`):**
    ```bash
    python topoHBNet_main_analysis.py --trajectory trajectory.xyz --cell-file trajectory.cell --run-ml --output-dir topoHBNet-run-ml
    ```

## 2. Reactive Species Analysis

**Script**: `trajectory_species_analysis.py`

Focuses on detecting chemical transformations and identifying molecular fragments in the liquid phase while excluding the solid substrate.

- **Key Features**:
  - **PBC-Aware Bond Detection**: Identifies O-H, O-O, and H-H bonds across periodic boundaries (`r_oh` < 1.30 Å, `r_oo` < 1.50 Å).
  - **Graph-Based Fragmentation**: Uses connected components to isolate distinct molecules.
  - **Substrate Exclusion**: Automatically filters out surface atoms (Si, C, etc.) with physically tuned thresholds (C-O 1.85 Å, Si-O 2.15 Å).
  - **Quantum Mulliken Spin Decoupling**: Parses CP2K `.out` logs to extract atomic spin moments, decoupling `OH-` (hydroxide anion) from `*OH` (hydroxyl radical) with quantum accuracy.
  - **Equilibration Detection**: Automatically discards equilibration frames using `--equil-start-frame`.
- **Primary Output**: `trajectory_species_results/` (contains spin-decoupled `OH-` and `*OH` population counts and evolution plots).
- **Usage**:
  - **To generate species analysis results with equilibration filtering:**
    ```bash
    python trajectory_species_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --output-dir trajectory_species_results --equil-start-frame 4000
    ```

## 3. Simulation Energetics Visualization

**Script**: `visualizing_aimd_energetics.py`

A utility script to verify simulation stability by parsing the energetics output from CP2K.

- **Key Features**:
  - Tracks Temperature, Kinetic Energy, Potential Energy, and the Conserved Quantity.
  - Generates high-quality gradient-filled plots for stabilization assessment.
  - Exports raw energetics data to CSV for further statistical analysis.
- **Primary Output**: `visualization_aimd_energetics/` (contains stability plots and raw data).
- **Usage**:
  - **To generate energetics visualization results (`visualization_aimd_energetics/`):**
    ```bash
    python visualizing_aimd_energetics.py --input trajectory.ener --target-temp 298.0 --output visualization_aimd_energetics
    ```

## 4. Interfacial Water & Surface Analysis

**Script**: `interfacial_water_analysis.py`

Implements Steps 63–65 of the *Nature Protocols* paper to characterize water behavior at the interface with the substrate.

- **Key Features**:
  - **Dynamic Surface Detection**: Automatically determines the Gibbs Dividing Surface (GDS) by finding the crossover of substrate and water density profiles.
  - **Static Cutoff Mode**: Allows manual cutoff definition for rigid surfaces (like metal electrodes).
  - **Interfacial Classification (Step 63)**: Categorizes all water molecules dynamically into interfacial or bulk.
  - **Angular Probability Distributions (Step 64)**: Computes the distribution of dipole angles ($\phi$) and O-H bond angles ($\theta$) relative to the surface normal.
  - **H-Bond Networks at the Interface (Step 65)**: Computes the evolution of H-bond counts per interfacial water compared to bulk reference values.
- **Primary Output**: `interfacial_analysis_results/` (contains JSON dataset and high-quality plots of density profiles, angular distributions, and H-bond evolution).
- **Usage**:
  - **To generate interfacial water analysis results (`interfacial_analysis_results/`):**
    ```bash
    python interfacial_water_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --mode dynamic --output-dir interfacial_analysis_results
    ```

## 5. Proton Transfer & Dynamics Analysis

**Script**: `proton_transfer_analysis.py`

Analyzes proton transfer events, constructs proton wires, and performs Hodge decomposition of the hydrogen bond flow field.

- **Key Features**:
  - **Proton Transfer Profiling**: Computes the Potential of Mean Force (PMF) along the proton transfer coordinate ($\delta$).
  - **Proton Wire Tracking**: Identifies continuous hydrogen-bonded pathways (proton wires) bridging surface source oxygens (silanols) and sinks (interfacial $O_2$).
  - **Hodge Flow Decomposition**: Separates the z-directional proton transport flow into gradient (transport), curl (local loops), and harmonic (global cycles) components.
- **Primary Output**: `proton_transfer_results/` (contains PMF curve, time-series dynamics, Hodge flow decomposition plots, and raw CSV/JSON data).
- **Usage**:
  - **To generate proton transfer dynamics results (`proton_transfer_results/`):**
    ```bash
    python proton_transfer_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --output-dir proton_transfer_results
    ```

## 6. Bridge: Topology-Transport Correlation & Physical Law Discovery

**Script**: `correlate_topology_and_transport.py`

Bridges high-dimensional topological representations from machine learning with physical proton transport mechanisms. It quantifies how the geometry and topology of the hydrogen bond network govern charge carrier dynamics, and automatically discovers analytical physical laws via Symbolic Regression.

- **Key Features**:
  - **Cross-Correlation Mapping**: Computes Pearson/Spearman cross-correlation coefficients between algebraic invariants ($\beta_0, \beta_1, \beta_2$, Euler) and dynamical quantities (PMF, Wire length, Hodge flows).
  - **Topological State Clustering**: Uses K-Means on topological embedding space (TNN PC space) to isolate distinct structural states of the water network and profiles their average transport properties.
  - **Feature Importance Regression**: Trains a Random Forest to predict transport efficiency (`Hodge_Gradient_Pct` or `LBHB_Fraction`) from topological invariants and ranks which topological shapes are the strongest physical predictors.
  - **Physics-Guided Symbolic Regression (`--run-pysr`)**: Automatically runs PySR (Symbolic Regression via Genetic Programming) to discover explicit, publishable analytical physical laws. 
    > [!IMPORTANT]
    > **Physics Guidance**: In this discovery step, abstract neural network coordinates (`PC1`, `PC2`) are automatically filtered out. Restricting the feature space strictly to physically interpretable topological invariants ($\beta_1$, Euler, $n_{\text{hbonds}}$, donor/acceptor H-bond states like `state_2D0A`, `state_1D1A`) ensures that the discovered mathematical equation has well-defined physical units and clear mechanistic interpretability.
  - **Multi-Run Stability Selection**: Performs consensus voting across independent evolutionary runs (e.g. 10 runs) to identify robust physical equations and ranks invariant feature stability, Outputting a detailed report in `discovered_physical_law.md`.
- **Primary Output**: `topology_transport_correlation_results/` (contains correlation heatmaps, state-profiling bar charts, topological state clustering plots, feature importance horizontal bars, aligned CSV/JSON datasets, and consensus report `discovered_physical_law.md` when `--run-pysr` is enabled).
- **Discovered Analytical Physical Law Example**:
  From multi-run stability selection on the `LBHB_Fraction` target, PySR discovers the consensus equation:

$$
LBHB\_Fraction ≈ cos(n\_hbonds\cdot (-0.06165264))\cdot (-0.001963741)
$$

- **Usage**:
  - **To generate standard correlation and Random Forest regression:**
    ```bash
    python correlate_topology_and_transport.py --topo-dir topoHBNet-run-ml --proton-dir proton_transfer_results --output-dir topology_transport_correlation_results
    ```
  - **To trigger Symbolic Regression locally and discover physical laws:**
    ```bash
    python correlate_topology_and_transport.py --topo-dir topoHBNet-run-ml --proton-dir proton_transfer_results --output-dir topology_transport_correlation_results --run-pysr
    ```
  - **HPC Cluster Execution (Required for Publication-Quality Physical Equations):**
    ```bash
    sbatch run_correlation_pysr.sh
    ```
    > [!IMPORTANT]
    > **Publication Requirement**: While local execution with `--run-pysr` is suitable for rapid testing, **equations intended for academic publication MUST be generated by submitting `run_correlation_pysr.sh` on an HPC cluster**.
    > 
    > **Why HPC Execution is Necessary**:
    > - **Massive Core Allocation**: Allocates 192 CPU cores (e.g., SLURM `9a14a` partition on Wuhan University Supercomputer Center) to perform parallel multi-run Genetic Programming across tens of thousands of candidate equations.
    > - **Thread Explosion Prevention**: Configures Julia and math environment variables (`JULIA_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`) so 192 independent PySR worker processes run without thread contention.
    > - **Multi-Run Stability Selection**: Executes 10+ independent evolutionary runs with different random seeds to perform consensus voting, guaranteeing that the final mathematical law (`discovered_physical_law.md`) is statistically stable, highly universal, and free from single-run local minima artifacts.

---

## Input Requirements

The scripts expect the following CP2K AIMD simulation files (defaults are automatically configured for this directory):

- `trajectory.xyz`: Molecular atomic coordinates for each frame (required for H-bond topology, interfacial, and species analysis).
- `trajectory.cell`: Time-dependent periodic cell dimensions or static box vectors (required for PBC distance array calculations).
- `trajectory.ener`: CP2K energy, temperature, and conserved quantity log (required for simulation energetics visualization).
- `aimd_*.out`: CP2K main calculation log files containing `Mulliken Population Analysis` tables (optional/recommended for `trajectory_species_analysis.py` to extract atomic spin moments for 100% quantum-mechanically decoupling `OH-` anions from `*OH` radicals).

## Directory Structure

- `trajectory_species_results/`: Detailed README and results for species quantification.
- `visualization_aimd_energetics/`: Detailed README and results for energetics.
- `interfacial_analysis_results/`: Results and visualization of the interfacial water analysis.
- `proton_transfer_results/`: Results and visualizations for proton transfer and Hodge flow dynamics.
- `topology_transport_correlation_results/`: Cross-correlation heatmaps, state-profiling, topological feature importance datasets, and discovered analytical physical laws (`discovered_physical_law.md`).
- `topoHBNet-run-ml/`: Main topological and machine learning output.
- `topoHBNet-no_run-ml/`: Main topological output.
