# CP2K AIMD Species Analysis Results

This directory contains the results of a reactive species analysis performed on a CP2K ab initio molecular dynamics (AIMD) trajectory. The analysis identifies and quantifies different molecular species (solvents, radicals, and intermediates) over the course of the simulation.

## 1. Analysis Methodology

### 1.1 PBC-Aware Distance Calculation

The analysis accounts for **Periodic Boundary Conditions (PBC)** using the **Minimum Image Convention**. This ensures that atoms located at opposite edges of the simulation box are correctly identified as neighbors if their periodic distance is within the specified thresholds.

### 1.2 Graph-Based Fragment Identification

The system is modeled as a mathematical graph where atoms are nodes and bonds are edges. For each frame, the script performs the following:

1.  **Bond Mapping**: Calculates all pairwise distances and applies the following distance thresholds (Å) to define graph edges:
    - **O-H**: 1.2 Å (Reactive)
    - **O-O**: 1.6 Å (Reactive)
    - **H-H**: 0.9 Å (Reactive)
    - **Substrate Bonds**: Si-O (2.0), C-H (1.2), Si-C (2.0), C-C (1.7), etc.
2.  **Connectivity Analysis**: Identifies **Connected Components** (clusters of bonded atoms) using the `scipy.sparse.csgraph` library. Each component represents a distinct molecular fragment.

### 1.3 Substrate-Aware Filtering (Substrate Exclusion)

To accurately distinguish between species in the liquid phase and those bound to the solid surface (e.g., distinguishing between a free `*OH` radical and a surface `Si-OH` group), the algorithm utilizes "Substrate Bonds" (Si-O, C-H, Si-C, etc.):

- **Exclusion Logic**: Any fragment containing **at least one** substrate atom (Si or C) is identified as part of the solid slab or surface. These fragments are **excluded** from the reactive species count.
- **Classification Logic**: Only fragments composed **purely** of Hydrogen (H) and Oxygen (O) are categorized based on their stoichiometric composition ($n_H, n_O$) as follows:

| Stoichiometry (H, O) | Species Name | Physical Description |
| :--- | :--- | :--- |
| (2, 1) | **H₂O** | Water molecule |
| (1, 0) | **H*** | Atomic hydrogen / proton |
| (1, 1) | ***OH** | Hydroxyl radical |
| (2, 0) | **H₂** | Molecular hydrogen |
| (0, 2) | **O₂** | Molecular oxygen |
| (0, 1) | **O*** | Atomic oxygen |
| (2, 2) | **H₂O₂** | Hydrogen peroxide |
| (3, 1) | **H₃O⁺** | Hydronium ion |
| (1, 2) | **HO₂*** | Hydroperoxyl radical |
| (3, 2) | **H₃O₂⁻** | Zundel-like intermediate |
| (4, 2) | **(H₂O)₂** | Water dimer |

## 2. File Descriptions

| File | Description |
| :--- | :--- |
| `species_counts.csv` | Time series data containing the count of each species for every analyzed frame. |
| `species_summary.json` | Statistical summary (mean, standard deviation, min, max) for all tracked species. |
| `species_evolution.png` | Plot showing the population of detected species over simulation time. |
| `species_distribution.png` | Pie chart illustrating the average composition of reactive species in the system. |

## 3. Executive Summary of Results

The following table summarizes the most prevalent species found in this simulation across **1002 frames**:

| Species | Mean Count | Std. Dev. | Physical Interpretation |
| :--- | :--- | :--- | :--- |
| **H₂O** | 50.00 | 0.00 | Stable water molecules |
| **H₂** | 1.00 | 0.00 | Molecular hydrogen |
| **H*** | 1.16 | 0.53 | Atomic hydrogen / Dissociated protons |

*Note: Species such as H₂O₂, *OH, and O₂ were not detected (mean count < 0.01) in this specific non-field trajectory.*

## 4. Usage for Comparative Analysis

To repeat this analysis or apply it to a new trajectory (e.g., with an external electric field), use the following script:

```bash
python cp2k_species_analysis.py --xyz trajectory.xyz --cell-file trajectory.cell --plot
```

The script configuration used for this output relied on:
- **Trajectory Stride**: 1 (Every frame analyzed)
- **Ho-only Filtering**: True (Fragments containing Si or C were identified but excluded from reactive species counts)
