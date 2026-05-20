# CP2K AIMD: Water/Substrate Interface (No Field)

This directory contains a complete workflow for analyzing an ab initio molecular dynamics (AIMD) trajectory of water on a substrate (e.g., Si/C surface) using the `topoHBNet` package.

The example demonstrates four complementary analysis workflows:

1. **Hydrogen Bond Network Topology** (`topoHBNet_main_analysis.py`)
2. **Reactive Species Stoichiometry** (`trajectory_species_analysis.py`)
3. **Simulation Energetics & Stability** (`visualizing_aimd_energetics.py`)
4. **Interfacial Water & Surface Analysis** (`interfacial_water_analysis.py`)

---

## 1. Topological H-Bond Network Analysis

**Script**: `topoHBNet_main_analysis.py`

This is the central analysis script utilizing the core `topoHBNet` library. It maps the H-bond network as a topological complex and calculates invariants.

- **Key Features**:
  - H-bond counting and dynamics (lifetime, autocorrelation).
  - **Topological Invariants**: Betti numbers ($\beta_0, \beta_1, \beta_2$) and Euler characteristic.
  - **Persistent Homology (TDA)**: Barcodes and persistence diagrams to identify stable vs. transient H-bond loops.
  - **Topological Machine Learning**: TNN feature extraction, topological embeddings, and PCA visualization (enabled with `--run-ml`).
- **Primary Output**: `topoHBNet-no_run-ml/` (contains JSON results and visualizations).
- **Usage**:
  ```bash
  python topoHBNet_main_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --run-ml
  ```

## 2. Reactive Species Analysis

**Script**: `trajectory_species_analysis.py`

Focuses on detecting chemical transformations and identifying molecular fragments in the liquid phase while excluding the solid substrate.

- **Key Features**:
  - **PBC-Aware Bond Detection**: Identifies O-H, O-O, and H-H bonds across periodic boundaries.
  - **Graph-Based Fragmentation**: Uses connected components to isolate distinct molecules.
  - **Substrate Exclusion**: Automatically identifies and filters out surface atoms (Si, C) to focus only on reactive species.
  - **Stoichiometric Classification**: Categorizes H/O fragments into species like H₂O, H*, *OH, H₂O₂, H₃O⁺, etc.
- **Primary Output**: `trajectory_species_results/` (contains population counts and evolution plots).
- **Usage**:
  ```bash
  python trajectory_species_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --plot
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
  ```bash
  python visualizing_aimd_energetics.py --input trajectory.ener --target-temp 298.0
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
  ```bash
  python interfacial_water_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --mode dynamic
  ```

---

## Input Requirements

The scripts expect the following files (defaults are typically set for this directory):

- `trajectory.xyz`: The molecular positions for each frame.
- `trajectory.cell`: Time-dependent cell dimensions (or static dimensions).
- `trajectory.ener`: CP2K energy and temperature log.

## Directory Structure

- `trajectory_species_results/`: Detailed README and results for species quantification.
- `visualization_aimd_energetics/`: Detailed README and results for energetics.
- `interfacial_analysis_results/`: Results and visualization of the interfacial water analysis.
- `topoHBNet-run-ml/`: Main topological and machine learning output.
- `topoHBNet-no_run-ml/`: Main topological  output.
