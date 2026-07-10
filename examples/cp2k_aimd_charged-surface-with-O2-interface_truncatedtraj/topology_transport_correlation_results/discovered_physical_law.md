# Discovering Robust H-Bond Topological Laws via Multi-Run Symbolic Regression

This report presents the robust physical equations discovered by running multi-run Symbolic Regression (PySR) with stability selection. By executing independent evolutionary runs with different random seeds, we identify equations and topological invariants that consistently govern proton transport properties.

## 1. Study Settings
- **Target Transport Property**: `LBHB_Fraction`
- **Total Independent PySR Runs**: 5
- **Iterations Per Run**: 500
- **Input Topological Invariants**: `n_hbonds`, `betti_0`, `betti_1`, `betti_2`, `euler_characteristic`

## 2. Robust Consensus Physical Laws (Voting Analysis)
Below is the frequency table of the 'best' equations selected by PySR across all runs. The equation with the highest vote count represents the most robust mathematical representation of the underlying physical relationship.

| Rank | Discovered Consensus Equation | Vote Count | Frequency | 
| :--- | :--- | :--- | :--- |
| 1 | `LBHB_Fraction ≈ 0.18348734/betti_1` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ 0.1834876/betti_1` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.18348595/betti_1` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ 0.18348756/betti_1` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.18348736/betti_1` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx 0.18348734/betti_1$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 51/76 | 67.1% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 45/76 | 59.2% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 34/76 | 44.7% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 28/76 | 36.8% | ⚡ Medium |
| `betti_2` | Number of topological voids/cavities | 1/76 | 1.3% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 51/76 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: 0.18348734/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535798` | `0.00285357980000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348734 / betti_1` | `0.18348734/betti_1` |
| 5 | 1.796604e-07 | 0.0027 | `(0.15820767 / betti_1) + 0.00039523386` | `0.00039523386 + 0.15820767/betti_1` |
| 6 | 1.773860e-07 | 0.0127 | `exp(betti_1 * -0.12831202) + 0.0025515645` | `exp(betti_1*(-0.12831202)) + 0.0025515645` |
| 7 | 1.768642e-07 | 0.0029 | `((n_hbonds / betti_1) * 0.0016491872) + -0.0013279406` | `-0.0013279406 + n_hbonds*0.0016491872/betti_1` |
| 8 | 1.745972e-07 | 0.0129 | `exp((euler_characteristic * 19.521065) / n_hbonds) + 0.0023155324` | `exp(euler_characteristic*19.521065/n_hbonds) + 0.0023155324` |
| 10 | 1.736007e-07 | 0.0029 | `(exp((euler_characteristic * 19.521065) / n_hbonds) / betti_0) + 0.0023173527` | `0.0023173527 + exp(euler_characteristic*19.521065/n_hbonds)/betti_0` |
| 11 | 1.736007e-07 | 0.0000 | `sin((exp((euler_characteristic * 19.521065) / n_hbonds) / betti_0) + 0.0023173527)` | `sin(0.0023173527 + exp(euler_characteristic*19.521065/n_hbonds)/betti_0)` |
| 12 | 1.735731e-07 | 0.0002 | `(exp(((0.9989268 - betti_1) * 19.521065) / n_hbonds) / betti_0) + 0.0023176298` | `0.0023176298 + exp((0.9989268 - betti_1)*19.521065/n_hbonds)/betti_0` |
| 13 | 1.735731e-07 | 0.0000 | `(exp(((cos(betti_2) - betti_1) * 19.521065) / n_hbonds) / betti_0) + 0.0023173527` | `0.0023173527 + exp((-betti_1 + cos(betti_2))*19.521065/n_hbonds)/betti_0` |
| 14 | 1.732063e-07 | 0.0021 | `(exp((cos(sin(euler_characteristic)) - betti_1) * (19.521065 / n_hbonds)) / betti_0) + 0.0023325782` | `0.0023325782 + exp((-betti_1 + cos(sin(euler_characteristic)))*19.521065/n_hbonds)/betti_0` |
| 16 | 1.731181e-07 | 0.0003 | `(exp(((cos(sin(0.80655354 - betti_1)) - betti_1) * 19.521065) / n_hbonds) / betti_0) + 0.0023325782` | `0.0023325782 + exp((-betti_1 + cos(sin(0.80655354 - betti_1)))*19.521065/n_hbonds)/betti_0` |
| 17 | 1.728728e-07 | 0.0014 | `(exp(((sin(exp(sin(0.1507947 - euler_characteristic))) - betti_1) * 19.521065) / n_hbonds) / betti_0) + 0.0023400888` | `0.0023400888 + exp((-betti_1 + sin(exp(sin(0.1507947 - euler_characteristic))))*19.521065/n_hbonds)/betti_0` |
| 19 | 1.727483e-07 | 0.0004 | `(exp(((sin(euler_characteristic / -0.0022005776) + ((euler_characteristic - 1.3937215) + euler_characteristic)) * 9.614492) / n_hbonds) / betti_0) + 0.0023014566` | `0.0023014566 + exp((euler_characteristic + euler_characteristic + sin(euler_characteristic/(-0.0022005776)) - 1*1.3937215)*9.614492/n_hbonds)/betti_0` |
| 20 | 1.727482e-07 | 0.0000 | `sin((exp(((sin(euler_characteristic / -0.0022005776) + ((euler_characteristic - 1.3937215) + euler_characteristic)) * 9.614492) / n_hbonds) / betti_0) + 0.0023014566)` | `sin(0.0023014566 + exp((euler_characteristic + euler_characteristic + sin(euler_characteristic/(-0.0022005776)) - 1*1.3937215)*9.614492/n_hbonds)/betti_0)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.1834876/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535798` | `0.00285357980000000` |
| 3 | 1.806214e-07 | 0.0919 | `0.1834876 / betti_1` | `0.1834876/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348747 / betti_1)` | `sin(0.18348747/betti_1)` |
| 5 | 1.796604e-07 | 0.0053 | `(0.15827924 / betti_1) + 0.00039419674` | `0.00039419674 + 0.15827924/betti_1` |
| 6 | 1.791664e-07 | 0.0028 | `(0.03603902 / betti_1) * log(n_hbonds)` | `0.03603902*log(n_hbonds)/betti_1` |
| 7 | 1.768643e-07 | 0.0129 | `-0.0013280711 - ((n_hbonds / betti_1) * -0.00164924)` | `-0.0013280711 - (-0.00164924)*n_hbonds/betti_1` |
| 8 | 1.741801e-07 | 0.0153 | `-0.002487981 / sin(0.47548547 - (n_hbonds / betti_1))` | `-0.002487981/sin(0.47548547 - n_hbonds/betti_1)` |
| 10 | 1.734162e-07 | 0.0022 | `(cos((n_hbonds * 1.3706551) / betti_1) * 0.0034584831) - -0.006076484` | `cos(n_hbonds*1.3706551/betti_1)*0.0034584831 - 1*(-0.006076484)` |
| 11 | 1.734162e-07 | 0.0000 | `sin((cos((n_hbonds * 1.3706551) / betti_1) * 0.003459703) - -0.0060776584)` | `sin(cos(n_hbonds*1.3706551/betti_1)*0.003459703 - 1*(-0.0060776584))` |
| 12 | 1.728745e-07 | 0.0031 | `(cos((n_hbonds / euler_characteristic) + (-0.835948 / betti_0)) * 0.0056259776) - -0.0082339365` | `cos(n_hbonds/euler_characteristic - 0.835948/betti_0)*0.0056259776 - 1*(-0.0082339365)` |
| 13 | 1.728655e-07 | 0.0001 | `(0.0059599336 * sin(sin(betti_0 * 0.85399884) + (n_hbonds / euler_characteristic))) - -0.008580461` | `0.0059599336*sin(sin(betti_0*0.85399884) + n_hbonds/euler_characteristic) - 1*(-0.008580461)` |
| 15 | 1.728534e-07 | 0.0000 | `(sin((cos(-0.85863495 / betti_0) + 0.107865795) + (n_hbonds / euler_characteristic)) * 0.006132256) - -0.008758732` | `sin(cos(-0.85863495/betti_0) + 0.107865795 + n_hbonds/euler_characteristic)*0.006132256 - 1*(-0.008758732)` |
| 17 | 1.724650e-07 | 0.0011 | `(sin((betti_0 * 0.63641006) + ((n_hbonds - sin(euler_characteristic / -0.22963372)) / euler_characteristic)) * 0.004326784) - -0.0068593933` | `sin(betti_0*0.63641006 + (n_hbonds - sin(euler_characteristic/(-0.22963372)))/euler_characteristic)*0.004326784 - 1*(-0.0068593933)` |
| 19 | 1.724650e-07 | 0.0000 | `(sin(((euler_characteristic * (betti_0 * 0.63641006)) + (n_hbonds - sin(euler_characteristic / -0.22963372))) / euler_characteristic) * 0.004326784) - -0.0068593933` | `sin((euler_characteristic*betti_0*0.63641006 + n_hbonds - sin(euler_characteristic/(-0.22963372)))/euler_characteristic)*0.004326784 - 1*(-0.0068593933)` |
| 20 | 1.721848e-07 | 0.0016 | `(sin((betti_0 * 0.63641006) + ((n_hbonds - sin(0.9175627 / sin(euler_characteristic / -0.22963372))) / euler_characteristic)) * 0.004326784) - -0.0068593933` | `sin(betti_0*0.63641006 + (n_hbonds - sin(0.9175627/sin(euler_characteristic/(-0.22963372))))/euler_characteristic)*0.004326784 - 1*(-0.0068593933)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.18348595/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.00285358` | `0.00285358000000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348595 / betti_1` | `0.18348595/betti_1` |
| 5 | 1.796631e-07 | 0.0027 | `(0.15686136 / betti_1) + 0.00041615963` | `0.00041615963 + 0.15686136/betti_1` |
| 6 | 1.773846e-07 | 0.0128 | `exp(-0.12825847 * betti_1) + 0.0025505102` | `0.0025505102 + exp(-0.12825847*betti_1)` |
| 7 | 1.768645e-07 | 0.0029 | `((n_hbonds / betti_1) * 0.0016485073) + -0.0013266853` | `-0.0013266853 + n_hbonds*0.0016485073/betti_1` |
| 8 | 1.767081e-07 | 0.0009 | `exp((betti_1 * -0.109621204) - betti_0) + 0.0025101982` | `exp(-betti_0 + betti_1*(-0.109621204)) + 0.0025101982` |
| 9 | 1.767080e-07 | 0.0000 | `sin(exp((betti_1 * -0.109621204) - betti_0) + 0.0025101982)` | `sin(exp(-betti_0 + betti_1*(-0.109621204)) + 0.0025101982)` |
| 10 | 1.766236e-07 | 0.0005 | `exp((-0.11192663 * betti_1) + (0.14121892 - betti_0)) + 0.0025022102` | `exp(-betti_0 - 0.11192663*betti_1 + 0.14121892) + 0.0025022102` |
| 11 | 1.762356e-07 | 0.0022 | `0.0025505102 + exp((sin(-2.0022027 * betti_1) + betti_1) * -0.12825847)` | `exp((betti_1 + sin(-2.0022027*betti_1))*(-0.12825847)) + 0.0025505102` |
| 12 | 1.757568e-07 | 0.0027 | `exp((sin(sin(betti_1) * -77.37281) + betti_1) * -0.12846412) + 0.0025459277` | `exp((betti_1 + sin(sin(betti_1)*(-77.37281)))*(-0.12846412)) + 0.0025459277` |
| 13 | 1.734678e-07 | 0.0131 | `exp((betti_1 * -0.11363874) - sin((n_hbonds - betti_1) * -0.11735462)) + 0.002518173` | `exp(betti_1*(-0.11363874) - sin((-betti_1 + n_hbonds)*(-0.11735462))) + 0.002518173` |
| 15 | 1.728843e-07 | 0.0017 | `0.002518173 + exp(((betti_1 * -0.11363874) - sin((n_hbonds - betti_1) * -0.11735462)) * betti_0)` | `exp(betti_0*(betti_1*(-0.11363874) - sin((-betti_1 + n_hbonds)*(-0.11735462)))) + 0.002518173` |
| 17 | 1.728595e-07 | 0.0001 | `exp((betti_1 * -0.11363874) - ((sin((n_hbonds - betti_1) * -0.11735462) * betti_0) * betti_0)) + 0.002518173` | `exp(-betti_0*betti_0*sin((-betti_1 + n_hbonds)*(-0.11735462)) + betti_1*(-0.11363874)) + 0.002518173` |
| 19 | 1.726206e-07 | 0.0007 | `exp((betti_1 * -0.11759654) - sin(sin(((n_hbonds - betti_1) + cos(betti_1 * -0.4089049)) * -0.11973321))) - -0.002524811` | `exp(betti_1*(-0.11759654) - sin(sin((-betti_1 + n_hbonds + cos(betti_1*(-0.4089049)))*(-0.11973321)))) - 1*(-0.002524811)` |
| 20 | 1.724873e-07 | 0.0008 | `exp((betti_1 * -0.11770382) - sin(sin(sin(((n_hbonds + cos(betti_1 * 0.40842736)) - betti_1) * -0.11963633)))) - -0.002516426` | `exp(betti_1*(-0.11770382) - sin(sin(sin((-betti_1 + n_hbonds + cos(betti_1*0.40842736))*(-0.11963633))))) - 1*(-0.002516426)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: 0.18348756/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535796` | `0.00285357960000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348756 / betti_1` | `0.18348756/betti_1` |
| 5 | 1.796604e-07 | 0.0027 | `(0.15819985 / betti_1) - -0.00039539585` | `-1*(-0.00039539585) + 0.15819985/betti_1` |
| 6 | 1.773857e-07 | 0.0127 | `exp(betti_1 * -0.12812462) + 0.0025466278` | `exp(betti_1*(-0.12812462)) + 0.0025466278` |
| 8 | 1.767391e-07 | 0.0018 | `exp(betti_0 * (betti_1 * -0.12812626)) + 0.0025499184` | `exp(betti_0*betti_1*(-0.12812626)) + 0.0025499184` |
| 10 | 1.766649e-07 | 0.0002 | `exp((betti_0 * (euler_characteristic + -5.895808)) * 0.11752906) - -0.0025249156` | `exp(betti_0*(euler_characteristic - 5.895808)*0.11752906) - 1*(-0.0025249156)` |
| 11 | 1.764441e-07 | 0.0013 | `exp((euler_characteristic + sin(euler_characteristic + n_hbonds)) * 0.13088253) - -0.0025658237` | `exp((euler_characteristic + sin(euler_characteristic + n_hbonds))*0.13088253) - 1*(-0.0025658237)` |
| 12 | 1.759751e-07 | 0.0027 | `exp((euler_characteristic + sin(exp(betti_1 + 0.69728225))) * 0.13088313) - -0.0025553815` | `exp((euler_characteristic + sin(exp(betti_1 + 0.69728225)))*0.13088313) - 1*(-0.0025553815)` |
| 13 | 1.755667e-07 | 0.0023 | `exp(0.13088253 * ((euler_characteristic + sin(euler_characteristic + n_hbonds)) * betti_0)) - -0.0025658237` | `exp(0.13088253*betti_0*(euler_characteristic + sin(euler_characteristic + n_hbonds))) - 1*(-0.0025658237)` |
| 14 | 1.751236e-07 | 0.0025 | `exp(betti_0 * ((euler_characteristic + sin(exp(betti_1 + 0.69728225))) * 0.13088313)) - -0.0025553815` | `exp(betti_0*(euler_characteristic + sin(exp(betti_1 + 0.69728225)))*0.13088313) - 1*(-0.0025553815)` |
| 15 | 1.750746e-07 | 0.0003 | `exp((sin((euler_characteristic + n_hbonds) / 3.2335002) + (euler_characteristic * betti_0)) * 0.12915088) - -0.002547415` | `exp((betti_0*euler_characteristic + sin((euler_characteristic + n_hbonds)/3.2335002))*0.12915088) - 1*(-0.002547415)` |
| 16 | 1.750462e-07 | 0.0002 | `exp((betti_0 * 0.13125995) * ((euler_characteristic + sin(exp(betti_1 + 0.6972822))) + 0.55553263)) - -0.002540039` | `exp(betti_0*0.13125995*(euler_characteristic + sin(exp(betti_1 + 0.6972822)) + 0.55553263)) - 1*(-0.002540039)` |
| 17 | 1.747079e-07 | 0.0019 | `exp(((sin(n_hbonds + euler_characteristic) + sin(exp(betti_1 + 0.69728225))) + euler_characteristic) * 0.13088286) - -0.0025580113` | `exp((euler_characteristic + sin(euler_characteristic + n_hbonds) + sin(exp(betti_1 + 0.69728225)))*0.13088286) - 1*(-0.0025580113)` |
| 19 | 1.738415e-07 | 0.0025 | `exp((((sin(n_hbonds + euler_characteristic) + sin(exp(betti_1 + 0.69728225))) + euler_characteristic) * 0.13088286) * betti_0) - -0.0025580113` | `exp((euler_characteristic + sin(euler_characteristic + n_hbonds) + sin(exp(betti_1 + 0.69728225)))*0.13088286*betti_0) - 1*(-0.0025580113)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.18348736/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535798` | `0.00285357980000000` |
| 3 | 1.806214e-07 | 0.0919 | `0.18348736 / betti_1` | `0.18348736/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348888 / betti_1)` | `sin(0.18348888/betti_1)` |
| 5 | 1.796604e-07 | 0.0053 | `(0.1581822 / betti_1) + 0.0003956474` | `0.0003956474 + 0.1581822/betti_1` |
| 6 | 1.780545e-07 | 0.0090 | `exp(betti_1 * -0.13075891) + 0.002593849` | `exp(betti_1*(-0.13075891)) + 0.002593849` |
| 7 | 1.768643e-07 | 0.0067 | `((n_hbonds / betti_1) * 0.0016491201) + -0.0013277679` | `-0.0013277679 + n_hbonds*0.0016491201/betti_1` |
| 8 | 1.753595e-07 | 0.0085 | `(exp(n_hbonds / betti_1) * 0.00012913313) + 0.0012113128` | `exp(n_hbonds/betti_1)*0.00012913313 + 0.0012113128` |
| 9 | 1.753595e-07 | 0.0000 | `sin(0.0012113128 + (exp(n_hbonds / betti_1) * 0.00012913313))` | `sin(exp(n_hbonds/betti_1)*0.00012913313 + 0.0012113128)` |
| 10 | 1.724521e-07 | 0.0167 | `(cos(n_hbonds / (betti_1 * 0.19043414)) * -0.0004979805) + 0.0031548862` | `0.0031548862 + cos(n_hbonds/((betti_1*0.19043414)))*(-0.0004979805)` |
| 11 | 1.724521e-07 | 0.0000 | `sin(0.0031548862 + (-0.0004979805 * cos(n_hbonds / (betti_1 * 0.19043414))))` | `sin(0.0031548862 - 0.0004979805*cos(n_hbonds/((betti_1*0.19043414))))` |
| 12 | 1.718952e-07 | 0.0032 | `(cos((n_hbonds / (betti_0 * euler_characteristic)) / -0.192009) * -0.00046697684) + 0.003106064` | `0.003106064 + cos(n_hbonds/((-0.192009)*((betti_0*euler_characteristic))))*(-0.00046697684)` |
| 14 | 1.718714e-07 | 0.0001 | `(-0.00045482963 * cos((n_hbonds / (-0.1916945 * (betti_1 + -0.93895835))) / betti_0)) + 0.0030931453` | `0.0030931453 - 0.00045482963*cos(n_hbonds/(betti_0*((-0.1916945*(betti_1 - 0.93895835)))))` |
| 16 | 1.715017e-07 | 0.0011 | `0.0030849695 + (-0.00044722928 * cos((n_hbonds / ((betti_0 * euler_characteristic) + cos(sin(euler_characteristic)))) / -0.19352506))` | `0.0030849695 - 0.00044722928*cos(n_hbonds/((-0.19352506)*(betti_0*euler_characteristic + cos(sin(euler_characteristic)))))` |
| 17 | 1.715017e-07 | 0.0000 | `sin(0.0030849695 + (-0.00044722928 * cos((n_hbonds / ((betti_0 * euler_characteristic) + cos(sin(euler_characteristic)))) / -0.19352506)))` | `sin(0.0030849695 - 0.00044722928*cos(n_hbonds/((-0.19352506)*(betti_0*euler_characteristic + cos(sin(euler_characteristic))))))` |
| 18 | 1.714025e-07 | 0.0006 | `0.0030849695 + (-0.00044722928 * cos((n_hbonds / (cos(sin(0.62277716 - betti_1)) + (euler_characteristic * betti_0))) / -0.19352506))` | `0.0030849695 - 0.00044722928*cos(n_hbonds/((-0.19352506)*(betti_0*euler_characteristic + cos(sin(0.62277716 - betti_1)))))` |
| 19 | 1.711288e-07 | 0.0016 | `(cos((n_hbonds / ((sin((euler_characteristic + euler_characteristic) + 0.99999344) + euler_characteristic) * betti_0)) / -0.19189969) * -0.00045149607) + 0.0030952215` | `0.0030952215 + cos(n_hbonds/((-0.19189969)*((betti_0*(euler_characteristic + sin(euler_characteristic + euler_characteristic + 0.99999344))))))*(-0.00045149607)` |
| 20 | 1.708983e-07 | 0.0013 | `(cos((n_hbonds / ((euler_characteristic + sin(sin((euler_characteristic + 0.9451807) + euler_characteristic))) * betti_0)) / -0.192293) * -0.00046935157) + 0.0031116665` | `0.0031116665 + cos(n_hbonds/((-0.192293)*((betti_0*(euler_characteristic + sin(sin(euler_characteristic + euler_characteristic + 0.9451807)))))))*(-0.00046935157)` |

</details>

