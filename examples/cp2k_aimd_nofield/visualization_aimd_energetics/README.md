# CP2K AIMD Energetics Visualization Results

This directory contains the visualization and raw data for the energy trends extracted from a CP2K ab initio molecular dynamics (AIMD) simulation. These plots and data are essential for verifying the stability and equilibration of the MD trajectory.

## 1. Overview of Energy Terms

The analysis tracks the following physical properties over time:

1.  **Potential Energy ($E_{pot}$)**: The total electronic and nuclear interaction energy of the system.
2.  **Kinetic Energy ($E_{kin}$)**: The energy associated with atomic motion, used to calculate the instantaneous temperature.
3.  **Temperature ($T$)**: Calculated from the kinetic energy using the degrees of freedom in the system.
4.  **Conserved Quantity / Total Energy ($E_{tot}$)**: In a stable AIMD simulation (NVE or NVT with a proper thermostat), this value should remain relatively constant, showing only minor fluctuations without long-term drift.

## 2. File Descriptions

### 2.1 Visualization Plots
| File | Description |
| :--- | :--- |
| `aimd_energetics_combined.png` | A single multi-panel plot showing all energy terms and temperature together for easy comparison. |
| `temperature_vs_time.png` | Individual plot showing temperature fluctuations and equilibration around the target (e.g., 298 K). |
| `potential_energy_vs_time.png` | Individual plot showing the evolution of the system's potential energy. |
| `kinetic_energy_vs_time.png` | Individual plot tracking the motion-related energy of the atoms. |
| `total_energy_vs_time.png` | Individual plot of the conserved quantity, used to assess the integration accuracy and energy conservation. |

*Note: All plots are also available in high-quality SVG format for publications.*

### 2.2 Raw Data
| File | Description |
| :--- | :--- |
| `aimd_energetics_raw_data.csv` | Comma-separated values containing the parsed numerical data for all columns: `Step`, `Time_fs`, `Kinetic_au`, `Temperature_K`, `Potential_au`, and `Conserved_au`. |

## 3. Stability Summary

Based on the analyzed trajectory (**0.0 to 500.0 fs**, 1001 total steps):

- **Temperature Stability**: The system was initialized at **298.0 K**. Fluctuations observed are typical for AIMD of this system size.
- **Energy Conservation**: The "Conserved Quantity" shows a stable trend with no significant upward or downward drift, indicating that the choice of timestep (0.5 fs) and basis set/pseudo-potentials is appropriate for this simulation.
- **Equilibration State**: The potential energy shows rapid stabilization after the initial steps, suggesting the system is well-behaved within the sampled time window.

## 4. Usage

To regenerate these plots or analyze a new CP2K log file, use the energetics visualization script:

```bash
python visualize_aimd_energetics.py --log cp2k_output.log --export-csv --output-dir results/
```

This script extracts data from the CP2K "ENERGY" and "TEMPERATURE" sections printed during the simulation run.
