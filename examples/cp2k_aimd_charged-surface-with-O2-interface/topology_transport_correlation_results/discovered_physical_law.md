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
| 1 | `LBHB_Fraction ≈ exp(euler_characteristic/7.284774) + 0.0014697029` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13725807) + 0.001468715` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(euler_characteristic/7.285659) - 1*(-0.0014691307)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13727064) + 0.0014689529` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ exp(euler_characteristic/7.285246) + 0.0014694125` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(euler_characteristic/7.284774) + 0.0014697029$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 65/81 | 80.2% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 41/81 | 50.6% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 24/81 | 29.6% | ❄️ Low |
| `betti_1` | Number of independent H-bond loops/cycles | 13/81 | 16.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/81 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 65/81 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(euler_characteristic/7.284774) + 0.0014697029</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026767328` | `0.00267673280000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626758 / euler_characteristic` | `-0.14626758/euler_characteristic` |
| 4 | 7.821249e-07 | 1.0044 | `exp(n_hbonds * -0.040548157)` | `exp(n_hbonds*(-0.040548157))` |
| 5 | 5.554059e-07 | 0.3423 | `-0.058967665 / (euler_characteristic + 28.161694)` | `-0.058967665/(euler_characteristic + 28.161694)` |
| 6 | 3.622926e-07 | 0.4272 | `exp(euler_characteristic / 7.284774) + 0.0014697029` | `exp(euler_characteristic/7.284774) + 0.0014697029` |
| 7 | 3.622894e-07 | 0.0000 | `sin(0.0014697029 + exp(euler_characteristic / 7.284774))` | `sin(exp(euler_characteristic/7.284774) + 0.0014697029)` |
| 8 | 3.539107e-07 | 0.0234 | `exp(euler_characteristic / 7.4101276) - (2.5543803e-5 * euler_characteristic)` | `-2.5543803e-5*euler_characteristic + exp(euler_characteristic/7.4101276)` |
| 9 | 3.511342e-07 | 0.0079 | `exp((euler_characteristic - sin(betti_1)) / 7.235423) + 0.001501722` | `exp((euler_characteristic - sin(betti_1))/7.235423) + 0.001501722` |
| 10 | 3.496442e-07 | 0.0043 | `exp((euler_characteristic - sin(sin(betti_1))) / 7.2437177) + 0.0014962056` | `exp((euler_characteristic - sin(sin(betti_1)))/7.2437177) + 0.0014962056` |
| 11 | 3.228124e-07 | 0.0798 | `exp((sin(n_hbonds * -0.4392826) + euler_characteristic) / 7.2461686) - -0.0015082221` | `exp((euler_characteristic + sin(n_hbonds*(-0.4392826)))/7.2461686) - 1*(-0.0015082221)` |
| 13 | 3.044872e-07 | 0.0292 | `exp((sin(-0.43855247 * (n_hbonds / betti_0)) + euler_characteristic) / 7.2461686) - -0.0015082221` | `exp((euler_characteristic + sin(-0.43855247*n_hbonds/betti_0))/7.2461686) - 1*(-0.0015082221)` |
| 15 | 3.007441e-07 | 0.0062 | `exp(((sin((n_hbonds / betti_0) * -0.43857658) / 0.78089124) + euler_characteristic) / 7.246153) + 0.0015065403` | `exp((euler_characteristic + sin(n_hbonds*(-0.43857658)/betti_0)/0.78089124)/7.246153) + 0.0015065403` |
| 17 | 2.990136e-07 | 0.0029 | `exp(((betti_0 * (sin((n_hbonds / betti_0) * -0.43856132) / 0.8208883)) + euler_characteristic) / 7.24615) - -0.0015038823` | `exp((betti_0*sin(n_hbonds*(-0.43856132)/betti_0)/0.8208883 + euler_characteristic)/7.24615) - 1*(-0.0015038823)` |
| 18 | 2.973100e-07 | 0.0057 | `exp((euler_characteristic + (betti_0 * sin((n_hbonds + -8.568699) * (-0.35152268 / sin(betti_0))))) / 7.246183) - -0.0015111461` | `exp((betti_0*sin((n_hbonds - 8.568699)*(-0.35152268)/sin(betti_0)) + euler_characteristic)/7.246183) - 1*(-0.0015111461)` |
| 20 | 2.940610e-07 | 0.0055 | `exp((((0.32644704 + betti_0) * sin((n_hbonds - 8.01147) * (-0.34990504 / sin(betti_0)))) + euler_characteristic) / 7.246151) - -0.0015008952` | `exp((euler_characteristic + (betti_0 + 0.32644704)*sin((n_hbonds - 1*8.01147)*(-0.34990504)/sin(betti_0)))/7.246151) - 1*(-0.0015008952)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: exp(euler_characteristic*0.13725807) + 0.001468715</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.002676728` | `0.00267672800000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626653 / euler_characteristic` | `-0.14626653/euler_characteristic` |
| 4 | 7.821254e-07 | 1.0044 | `exp(n_hbonds / -24.661173)` | `exp(n_hbonds/(-24.661173))` |
| 5 | 7.360077e-07 | 0.0608 | `(-0.5764481 / euler_characteristic) + -0.008520047` | `-0.008520047 - 0.5764481/euler_characteristic` |
| 6 | 3.622923e-07 | 0.7088 | `exp(euler_characteristic * 0.13725807) + 0.001468715` | `exp(euler_characteristic*0.13725807) + 0.001468715` |
| 7 | 3.622890e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13725807) + 0.001468715)` | `sin(exp(euler_characteristic*0.13725807) + 0.001468715)` |
| 8 | 3.550484e-07 | 0.0202 | `(euler_characteristic * -2.6071368e-5) + exp(euler_characteristic * 0.13544248)` | `euler_characteristic*(-2.6071368e-5) + exp(euler_characteristic*0.13544248)` |
| 9 | 3.291333e-07 | 0.0758 | `((-1.9314538 / euler_characteristic) + (euler_characteristic * -0.0006166161)) + -0.06710215` | `euler_characteristic*(-0.0006166161) - 0.06710215 - 1.9314538/euler_characteristic` |
| 10 | 3.291322e-07 | 0.0000 | `sin((-1.9314538 / euler_characteristic) + ((euler_characteristic * -0.0006166161) + -0.06710215))` | `sin(euler_characteristic*(-0.0006166161) - 0.06710215 - 1.9314538/euler_characteristic)` |
| 11 | 3.221912e-07 | 0.0213 | `exp((euler_characteristic - sin(n_hbonds * 0.18345381)) * 0.13932826) + 0.0015696752` | `exp((euler_characteristic - sin(n_hbonds*0.18345381))*0.13932826) + 0.0015696752` |
| 12 | 3.221907e-07 | 0.0000 | `sin(exp((euler_characteristic - sin(0.18345381 * n_hbonds)) * 0.13932826) + 0.0015696752)` | `sin(exp((euler_characteristic - sin(0.18345381*n_hbonds))*0.13932826) + 0.0015696752)` |
| 13 | 3.063496e-07 | 0.0504 | `exp((euler_characteristic - sin((n_hbonds * 0.439244) / betti_0)) * 0.13837063) + 0.0015246338` | `exp((euler_characteristic - sin(n_hbonds*0.439244/betti_0))*0.13837063) + 0.0015246338` |
| 15 | 3.005022e-07 | 0.0096 | `exp((euler_characteristic * 0.14145713) - (sin(n_hbonds * (betti_0 * 0.18415552)) * 0.27446175)) + 0.0016579184` | `exp(euler_characteristic*0.14145713 - 0.27446175*sin(n_hbonds*betti_0*0.18415552)) + 0.0016579184` |
| 16 | 2.942307e-07 | 0.0211 | `exp((euler_characteristic * 0.14217333) - (0.29895198 * sin(n_hbonds * sin(0.18640077 * betti_0)))) + 0.00167828` | `exp(euler_characteristic*0.14217333 - 0.29895198*sin(n_hbonds*sin(0.18640077*betti_0))) + 0.00167828` |
| 17 | 2.942293e-07 | 0.0000 | `sin(exp((euler_characteristic * 0.14217333) - (sin(n_hbonds * sin(0.18640077 * betti_0)) * 0.29895198)) + 0.00167828)` | `sin(exp(euler_characteristic*0.14217333 - 0.29895198*sin(n_hbonds*sin(0.18640077*betti_0))) + 0.00167828)` |
| 18 | 2.941624e-07 | 0.0002 | `sin(sin(exp((euler_characteristic * 0.14238124) - (sin(n_hbonds * sin(betti_0 * 0.18634081)) * 0.29895145)))) + 0.0016768442` | `sin(sin(exp(euler_characteristic*0.14238124 - 0.29895145*sin(n_hbonds*sin(betti_0*0.18634081))))) + 0.0016768442` |
| 19 | 2.932929e-07 | 0.0030 | `exp((euler_characteristic - sin(sin(n_hbonds * -0.64766955) + (n_hbonds * sin(betti_0 * 0.18570949)))) * 0.13879676) + 0.0015448082` | `exp((euler_characteristic - sin(n_hbonds*sin(betti_0*0.18570949) + sin(n_hbonds*(-0.64766955))))*0.13879676) + 0.0015448082` |
| 20 | 2.927367e-07 | 0.0019 | `0.0015448082 + exp((euler_characteristic - sin(sin(sin(n_hbonds * -0.64766955)) + (n_hbonds * sin(betti_0 * 0.18570949)))) * 0.13879676)` | `exp((euler_characteristic - sin(n_hbonds*sin(betti_0*0.18570949) + sin(sin(n_hbonds*(-0.64766955)))))*0.13879676) + 0.0015448082` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(euler_characteristic/7.285659) - 1*(-0.0014691307)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.002676732` | `0.00267673200000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626792 / euler_characteristic` | `-0.14626792/euler_characteristic` |
| 4 | 7.821258e-07 | 1.0044 | `exp(n_hbonds * -0.040550325)` | `exp(n_hbonds*(-0.040550325))` |
| 5 | 7.360079e-07 | 0.0608 | `(-0.5764509 / euler_characteristic) + -0.008520031` | `-0.008520031 - 0.5764509/euler_characteristic` |
| 6 | 3.622925e-07 | 0.7088 | `exp(euler_characteristic / 7.285659) - -0.0014691307` | `exp(euler_characteristic/7.285659) - 1*(-0.0014691307)` |
| 7 | 3.622892e-07 | 0.0000 | `sin(exp(euler_characteristic / 7.285659) - -0.0014691307)` | `sin(exp(euler_characteristic/7.285659) - 1*(-0.0014691307))` |
| 8 | 3.621865e-07 | 0.0003 | `exp((euler_characteristic / 7.193836) + 0.060981024) - -0.0014898515` | `exp(euler_characteristic/7.193836 + 0.060981024) - 1*(-0.0014898515)` |
| 9 | 3.511365e-07 | 0.0310 | `exp((euler_characteristic - sin(betti_1)) / 7.2346435) - -0.0015035083` | `exp((euler_characteristic - sin(betti_1))/7.2346435) - 1*(-0.0015035083)` |
| 10 | 3.496438e-07 | 0.0043 | `exp((euler_characteristic - sin(sin(betti_1))) / 7.2442074) - -0.0014957013` | `exp((euler_characteristic - sin(sin(betti_1)))/7.2442074) - 1*(-0.0014957013)` |
| 11 | 3.228253e-07 | 0.0798 | `exp((euler_characteristic - sin(n_hbonds * 0.4389791)) / 7.244228) - -0.001510457` | `exp((euler_characteristic - sin(n_hbonds*0.4389791))/7.244228) - 1*(-0.001510457)` |
| 13 | 3.046475e-07 | 0.0290 | `exp((euler_characteristic - sin((n_hbonds / betti_0) * 0.43857265)) / 7.2442946) - -0.0015055408` | `exp((euler_characteristic - sin(n_hbonds*0.43857265/betti_0))/7.2442946) - 1*(-0.0015055408)` |
| 15 | 3.000110e-07 | 0.0077 | `exp(((cos(n_hbonds / (betti_0 - -1.3426594)) / -0.7757582) + euler_characteristic) / 7.2419176) - -0.001512269` | `exp((euler_characteristic + cos(n_hbonds/(betti_0 - 1*(-1.3426594)))/(-0.7757582))/7.2419176) - 1*(-0.001512269)` |
| 17 | 2.977232e-07 | 0.0038 | `exp(((cos(n_hbonds / (-1.3426594 - betti_0)) / (-0.7757582 / betti_0)) + euler_characteristic) / 7.2419176) - -0.001512269` | `exp((euler_characteristic + cos(n_hbonds/(-betti_0 - 1.3426594))/((-0.7757582/betti_0)))/7.2419176) - 1*(-0.001512269)` |
| 19 | 2.952965e-07 | 0.0041 | `exp((euler_characteristic + (betti_0 * (cos((n_hbonds + betti_0) / (betti_0 - -1.3630916)) / -0.7753371))) / 7.241141) - -0.0015145135` | `exp((betti_0*cos((betti_0 + n_hbonds)/(betti_0 - 1*(-1.3630916)))/(-0.7753371) + euler_characteristic)/7.241141) - 1*(-0.0015145135)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: exp(euler_characteristic*0.13727064) + 0.0014689529</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026767328` | `0.00267673280000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14627811 / euler_characteristic` | `-0.14627811/euler_characteristic` |
| 4 | 1.150810e-06 | 0.6182 | `exp(n_hbonds * -0.039249245)` | `exp(n_hbonds*(-0.039249245))` |
| 5 | 5.547168e-07 | 0.7298 | `0.05935226 / (-28.090584 - euler_characteristic)` | `0.05935226/(-euler_characteristic - 28.090584)` |
| 6 | 3.622929e-07 | 0.4260 | `exp(euler_characteristic * 0.13727064) + 0.0014689529` | `exp(euler_characteristic*0.13727064) + 0.0014689529` |
| 7 | 3.622900e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13727064)) + 0.0014689529` | `sin(exp(euler_characteristic*0.13727064)) + 0.0014689529` |
| 8 | 3.539072e-07 | 0.0234 | `exp(euler_characteristic * 0.13495818) + (euler_characteristic * -2.5587808e-5)` | `euler_characteristic*(-2.5587808e-5) + exp(euler_characteristic*0.13495818)` |
| 9 | 3.539019e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13495818) + (euler_characteristic * -2.5587808e-5))` | `sin(euler_characteristic*(-2.5587808e-5) + exp(euler_characteristic*0.13495818))` |
| 10 | 3.514104e-07 | 0.0071 | `((betti_1 * euler_characteristic) * -4.4002078e-7) + exp(euler_characteristic * 0.13350432)` | `betti_1*euler_characteristic*(-4.4002078e-7) + exp(euler_characteristic*0.13350432)` |
| 11 | 3.259797e-07 | 0.0751 | `sin(-0.1499108 / ((cos(n_hbonds * 0.10180785) * 21.218288) - betti_1))` | `sin(-0.1499108/(-betti_1 + cos(n_hbonds*0.10180785)*21.218288))` |
| 12 | 3.132181e-07 | 0.0399 | `-0.14099704 / (((-0.13322327 - cos(0.10238663 * n_hbonds)) / -0.051648002) - betti_1)` | `-0.14099704/(-betti_1 + (-cos(0.10238663*n_hbonds) - 0.13322327)/(-0.051648002))` |
| 13 | 3.131477e-07 | 0.0002 | `sin(-0.14099704 / (((-0.12965034 - cos(0.10238663 * n_hbonds)) / -0.051648002) - betti_1))` | `sin(-0.14099704/(-betti_1 + (-cos(0.10238663*n_hbonds) - 0.12965034)/(-0.051648002)))` |
| 15 | 3.065075e-07 | 0.0107 | `-0.14102508 / (((-0.106692165 - cos((n_hbonds - sin(euler_characteristic)) * 0.10221456)) / -0.05055324) - betti_1)` | `-0.14102508/(-betti_1 + (-cos((n_hbonds - sin(euler_characteristic))*0.10221456) - 0.106692165)/(-0.05055324))` |
| 16 | 3.013829e-07 | 0.0169 | `-0.14102508 / (((-0.11270958 - cos((n_hbonds + cos(exp(betti_1))) * 0.10227232)) / -0.05055324) - betti_1)` | `-0.14102508/(-betti_1 + (-cos((n_hbonds + cos(exp(betti_1)))*0.10227232) - 0.11270958)/(-0.05055324))` |
| 17 | 3.002626e-07 | 0.0037 | `-0.14123178 / (((-0.11272401 - cos((n_hbonds + sin(betti_1 / betti_0)) * 0.10227232)) / -0.050789505) - betti_1)` | `-0.14123178/(-betti_1 + (-cos((n_hbonds + sin(betti_1/betti_0))*0.10227232) - 0.11272401)/(-0.050789505))` |
| 19 | 2.979760e-07 | 0.0038 | `-0.14102508 / (((-0.11270958 - cos((n_hbonds + (cos(euler_characteristic) + cos(exp(betti_1)))) * 0.10227232)) / -0.05055324) - betti_1)` | `-0.14102508/(-betti_1 + (-cos((n_hbonds + cos(euler_characteristic) + cos(exp(betti_1)))*0.10227232) - 0.11270958)/(-0.05055324))` |
| 20 | 2.949898e-07 | 0.0101 | `-0.14123178 / (((-0.11272401 - cos((n_hbonds - cos((betti_1 / 0.01144373) + exp(betti_0))) * 0.10227232)) / -0.050789505) - betti_1)` | `-0.14123178/(-betti_1 + (-cos((n_hbonds - cos(betti_1/0.01144373 + exp(betti_0)))*0.10227232) - 0.11272401)/(-0.050789505))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: exp(euler_characteristic/7.285246) + 0.0014694125</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026766665` | `0.00267666650000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626627 / euler_characteristic` | `-0.14626627/euler_characteristic` |
| 4 | 7.821254e-07 | 1.0044 | `exp(n_hbonds / -24.661207)` | `exp(n_hbonds/(-24.661207))` |
| 5 | 5.549709e-07 | 0.3431 | `0.059963387 / (-27.975069 - euler_characteristic)` | `0.059963387/(-euler_characteristic - 27.975069)` |
| 6 | 3.622922e-07 | 0.4265 | `exp(euler_characteristic / 7.285246) + 0.0014694125` | `exp(euler_characteristic/7.285246) + 0.0014694125` |
| 7 | 3.622889e-07 | 0.0000 | `sin(exp(euler_characteristic / 7.285246) + 0.0014694125)` | `sin(exp(euler_characteristic/7.285246) + 0.0014694125)` |
| 8 | 3.546502e-07 | 0.0213 | `(euler_characteristic * -2.6148948e-5) + exp(euler_characteristic * 0.13531499)` | `euler_characteristic*(-2.6148948e-5) + exp(euler_characteristic*0.13531499)` |
| 9 | 3.350925e-07 | 0.0567 | `-0.07098723 - ((euler_characteristic / 1531.9182) + (2.0351074 / euler_characteristic))` | `-(euler_characteristic/1531.9182 + 2.0351074/euler_characteristic) - 0.07098723` |
| 10 | 3.293269e-07 | 0.0174 | `0.9312487 - exp((2.0569785 / euler_characteristic) + (euler_characteristic / 1531.9182))` | `0.9312487 - exp(euler_characteristic/1531.9182 + 2.0569785/euler_characteristic)` |
| 11 | 3.222373e-07 | 0.0218 | `exp((euler_characteristic + cos(n_hbonds * -0.19616474)) * 0.13917734) + 0.0015584554` | `exp((euler_characteristic + cos(n_hbonds*(-0.19616474)))*0.13917734) + 0.0015584554` |
| 12 | 3.222367e-07 | 0.0000 | `sin(exp((euler_characteristic + cos(n_hbonds * -0.19616474)) * 0.13917731) + 0.0015584962)` | `sin(exp((euler_characteristic + cos(n_hbonds*(-0.19616474)))*0.13917731) + 0.0015584962)` |
| 13 | 3.105542e-07 | 0.0369 | `exp((sin((n_hbonds / betti_0) * -0.4412531) + euler_characteristic) * 0.13827969) + 0.0014994537` | `exp((euler_characteristic + sin(n_hbonds*(-0.4412531)/betti_0))*0.13827969) + 0.0014994537` |
| 15 | 3.010464e-07 | 0.0155 | `exp(((sin((betti_0 * -0.18426335) * n_hbonds) / 0.49089375) + euler_characteristic) * 0.14194873) + 0.0016763067` | `exp((euler_characteristic + sin(betti_0*(-0.18426335)*n_hbonds)/0.49089375)*0.14194873) + 0.0016763067` |
| 17 | 2.997801e-07 | 0.0021 | `exp((sin(((n_hbonds * 0.18218084) * betti_0) - -0.34154862) * -0.341533) + (euler_characteristic * 0.14369443)) + 0.0017401585` | `exp(euler_characteristic*0.14369443 + sin(n_hbonds*0.18218084*betti_0 - 1*(-0.34154862))*(-0.341533)) + 0.0017401585` |
| 18 | 2.971016e-07 | 0.0090 | `exp((sin((n_hbonds * -0.18213646) * betti_0) + (euler_characteristic + sin(n_hbonds * 0.16164282))) * 0.14218423) + 0.001691733` | `exp((euler_characteristic + sin(n_hbonds*0.16164282) + sin(n_hbonds*(-0.18213646)*betti_0))*0.14218423) + 0.001691733` |
| 19 | 2.954110e-07 | 0.0057 | `exp((sin(sin(betti_0 * -0.18424818) * n_hbonds) + (sin(n_hbonds * 0.16105513) + euler_characteristic)) * 0.14232397) + 0.0016941293` | `exp((euler_characteristic + sin(n_hbonds*0.16105513) + sin(n_hbonds*sin(betti_0*(-0.18424818))))*0.14232397) + 0.0016941293` |
| 20 | 2.917095e-07 | 0.0126 | `exp(((euler_characteristic + sin((betti_0 * n_hbonds) * -0.18341416)) + sin((n_hbonds + n_hbonds) * 0.20811296)) * 0.140239) + 0.0016127337` | `exp((euler_characteristic + sin((n_hbonds + n_hbonds)*0.20811296) + sin(betti_0*n_hbonds*(-0.18341416)))*0.140239) + 0.0016127337` |

</details>

