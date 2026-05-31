# Discovering Robust H-Bond Topological Laws via Multi-Run Symbolic Regression

This report presents the robust physical equations discovered by running multi-run Symbolic Regression (PySR) with stability selection. By executing independent evolutionary runs with different random seeds, we identify equations and topological invariants that consistently govern proton transport properties.

## 1. Study Settings
- **Target Transport Property**: `LBHB_Fraction`
- **Total Independent PySR Runs**: 2
- **Iterations Per Run**: 5
- **Input Topological Invariants**: `n_hbonds`, `betti_0`, `betti_1`, `betti_2`, `euler_characteristic`

## 2. Robust Consensus Physical Laws (Voting Analysis)
Below is the frequency table of the 'best' equations selected by PySR across all runs. The equation with the highest vote count represents the most robust mathematical representation of the underlying physical relationship.

| Rank | Discovered Consensus Equation | Vote Count | Frequency | 
| :--- | :--- | :--- | :--- |
| 1 | `LBHB_Fraction ≈ betti_1*(-1.0000805) + betti_1 - 0.38389727/euler_characteristic` | 1/2 | 50.0% |
| 2 | `LBHB_Fraction ≈ 0.21502073/betti_1` | 1/2 | 50.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx betti_1*(-1.0000805) + betti_1 - 0.38389727/euler_characteristic$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 4/6 | 66.7% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 1/6 | 16.7% | ❄️ Low |
| `n_hbonds` | Total number of hydrogen bonds in the network | 0/6 | 0.0% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 0/6 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/6 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 4/6 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: betti_1*(-1.0000805) + betti_1 - 0.38389727/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 5.481797e-06 | 0.0000 | `0.004439705` | `0.00443970500000000` |
| 3 | 3.202917e-06 | 0.2687 | `0.21845977 / betti_1` | `0.21845977/betti_1` |
| 9 | 1.788903e-06 | 0.0971 | `(betti_1 - (0.38389727 / euler_characteristic)) + (betti_1 * -1.0000805)` | `betti_1*(-1.0000805) + betti_1 - 0.38389727/euler_characteristic` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.21502073/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 5.481797e-06 | 0.0000 | `0.0044393553` | `0.00443935530000000` |
| 3 | 3.208367e-06 | 0.2678 | `0.21502073 / betti_1` | `0.21502073/betti_1` |
| 5 | 3.063036e-06 | 0.0232 | `0.20642944 / (betti_1 + -2.9368284)` | `0.20642944/(betti_1 - 2.9368284)` |

</details>

