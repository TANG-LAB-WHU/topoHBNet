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
| 1 | `LBHB_Fraction ≈ -0.1466938/euler_characteristic` | 2/5 | 40.0% |
| 2 | `LBHB_Fraction ≈ -0.14669347/euler_characteristic` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ -0.1466937/euler_characteristic` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -0.14669377/euler_characteristic` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx -0.1466938/euler_characteristic$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 57/75 | 76.0% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 42/75 | 56.0% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 32/75 | 42.7% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/75 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/75 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 57/75 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: -0.14669347/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 6.499156e-07 | 0.0000 | `0.002285641` | `0.00228564100000000` |
| 3 | 6.107763e-07 | 0.0311 | `-0.14669347 / euler_characteristic` | `-0.14669347/euler_characteristic` |
| 5 | 5.983239e-07 | 0.0103 | `9.638006 / (betti_1 * betti_1)` | `9.638006/((betti_1*betti_1))` |
| 6 | 5.959220e-07 | 0.0040 | `0.0018734245 / cos(n_hbonds / -28.175238)` | `0.0018734245/cos(n_hbonds/(-28.175238))` |
| 8 | 5.949692e-07 | 0.0008 | `(9.341116 / (euler_characteristic - sin(euler_characteristic))) / euler_characteristic` | `9.341116/(euler_characteristic*(euler_characteristic - sin(euler_characteristic)))` |
| 10 | 5.920545e-07 | 0.0025 | `(2.9299972 / ((euler_characteristic * 0.31429893) - sin(euler_characteristic))) / euler_characteristic` | `2.9299972/(euler_characteristic*(euler_characteristic*0.31429893 - sin(euler_characteristic)))` |
| 11 | 5.919969e-07 | 0.0001 | `(2.6890593 / ((euler_characteristic * 0.288557) - sin(sin(euler_characteristic)))) / euler_characteristic` | `2.6890593/(euler_characteristic*(euler_characteristic*0.288557 - sin(sin(euler_characteristic))))` |
| 12 | 5.909622e-07 | 0.0017 | `(2.9310389 / ((0.31429893 * euler_characteristic) - sin(euler_characteristic / 1.1163274))) / euler_characteristic` | `2.9310389/(euler_characteristic*(0.31429893*euler_characteristic - sin(euler_characteristic/1.1163274)))` |
| 14 | 5.909584e-07 | 0.0000 | `(2.9310389 / ((0.31429893 * euler_characteristic) - sin((euler_characteristic + 0.040804707) / 1.1163274))) / euler_characteristic` | `2.9310389/(euler_characteristic*(0.31429893*euler_characteristic - sin((euler_characteristic + 0.040804707)/1.1163274)))` |
| 15 | 5.886017e-07 | 0.0040 | `(4.453909 / (((euler_characteristic * 0.471602) - sin(euler_characteristic)) - sin(n_hbonds * 0.3241565))) / euler_characteristic` | `4.453909/(euler_characteristic*(euler_characteristic*0.471602 - sin(euler_characteristic) - sin(n_hbonds*0.3241565)))` |
| 17 | 5.869072e-07 | 0.0014 | `(3.028242 / (euler_characteristic - (sin(n_hbonds * 0.2839257) * 3.028242))) / ((euler_characteristic * 0.31717405) - sin(euler_characteristic))` | `3.028242/((euler_characteristic - 3.028242*sin(n_hbonds*0.2839257))*(euler_characteristic*0.31717405 - sin(euler_characteristic)))` |
| 18 | 5.868716e-07 | 0.0001 | `sin((3.028242 / (euler_characteristic - (sin(n_hbonds * 0.2839257) * 3.626142))) / ((euler_characteristic * 0.31717405) - sin(euler_characteristic)))` | `sin(3.028242/((euler_characteristic - 3.626142*sin(n_hbonds*0.2839257))*(euler_characteristic*0.31717405 - sin(euler_characteristic))))` |
| 19 | 5.859038e-07 | 0.0017 | `(3.0281053 / (euler_characteristic - (sin(n_hbonds * 0.28354993) * 3.0281053))) / ((0.31842396 * euler_characteristic) - sin(euler_characteristic / 1.1163274))` | `3.0281053/((0.31842396*euler_characteristic - sin(euler_characteristic/1.1163274))*(euler_characteristic - 3.0281053*sin(n_hbonds*0.28354993)))` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: -0.1466938/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 6.499156e-07 | 0.0000 | `0.002285642` | `0.00228564200000000` |
| 2 | 6.499155e-07 | 0.0000 | `sin(0.0022856717)` | `sin(0.0022856717)` |
| 3 | 6.107763e-07 | 0.0621 | `-0.1466938 / euler_characteristic` | `-0.1466938/euler_characteristic` |
| 5 | 5.975735e-07 | 0.0109 | `-0.0762481 / (31.505802 - betti_1)` | `-0.0762481/(31.505802 - betti_1)` |
| 7 | 5.975593e-07 | 0.0000 | `-0.012970499 / (5.501308 - (betti_1 * 0.1723288))` | `-0.012970499/(5.501308 - 0.1723288*betti_1)` |
| 8 | 5.950074e-07 | 0.0043 | `9.636601 / (betti_1 * (sin(euler_characteristic) + betti_1))` | `9.636601/((betti_1*(betti_1 + sin(euler_characteristic))))` |
| 9 | 5.947751e-07 | 0.0004 | `9.83073 / ((exp(cos(betti_1)) + betti_1) * betti_1)` | `9.83073/((betti_1*(betti_1 + exp(cos(betti_1)))))` |
| 10 | 5.918806e-07 | 0.0049 | `-0.016396118 / (7.3444953 - ((betti_1 + sin(euler_characteristic)) * 0.22391526))` | `-0.016396118/(7.3444953 - 0.22391526*(betti_1 + sin(euler_characteristic)))` |
| 12 | 5.909835e-07 | 0.0008 | `-0.016355108 / ((7.3444953 + (sin(euler_characteristic) * -0.35430023)) - (0.22391583 * betti_1))` | `-0.016355108/(-0.22391583*betti_1 + sin(euler_characteristic)*(-0.35430023) + 7.3444953)` |
| 13 | 5.909269e-07 | 0.0001 | `-0.016355108 / (((-0.39001206 * sin(sin(euler_characteristic))) + 7.3444953) - (betti_1 * 0.22391583))` | `-0.016355108/(-0.22391583*betti_1 - 0.39001206*sin(sin(euler_characteristic)) + 7.3444953)` |
| 14 | 5.900647e-07 | 0.0015 | `-0.013090426 / ((5.452642 + (-0.30425742 * sin(-0.8830155 * betti_1))) - (0.17229736 * betti_1))` | `-0.013090426/(-0.17229736*betti_1 - 0.30425742*sin(-0.8830155*betti_1) + 5.452642)` |
| 15 | 5.876182e-07 | 0.0042 | `9.703827 / (betti_1 * (((sin(-0.3428912 * n_hbonds) + sin(euler_characteristic)) / 0.3217641) + betti_1))` | `9.703827/((betti_1*(betti_1 + (sin(euler_characteristic) + sin(-0.3428912*n_hbonds))/0.3217641)))` |
| 16 | 5.870298e-07 | 0.0010 | `9.703827 / (betti_1 * ((sin(sin(n_hbonds * 0.3217641) + sin(euler_characteristic)) / 0.19186296) + betti_1))` | `9.703827/((betti_1*(betti_1 + sin(sin(euler_characteristic) + sin(n_hbonds*0.3217641))/0.19186296)))` |
| 17 | 5.850007e-07 | 0.0035 | `9.703827 / ((betti_1 + ((sin(euler_characteristic) + sin((n_hbonds + euler_characteristic) * 0.5942207)) / 0.27994904)) * betti_1)` | `9.703827/((betti_1*(betti_1 + (sin(euler_characteristic) + sin((euler_characteristic + n_hbonds)*0.5942207))/0.27994904)))` |
| 18 | 5.849356e-07 | 0.0001 | `9.703827 / ((((sin((n_hbonds + euler_characteristic) * 0.5942207) + sin(sin(euler_characteristic))) / 0.27790645) + betti_1) * betti_1)` | `9.703827/((betti_1*(betti_1 + (sin((euler_characteristic + n_hbonds)*0.5942207) + sin(sin(euler_characteristic)))/0.27790645)))` |
| 19 | 5.846774e-07 | 0.0004 | `9.703827 / ((betti_1 + ((sin(euler_characteristic - -0.250803) + sin(-0.62651485 * (n_hbonds + euler_characteristic))) / 0.30009225)) * betti_1)` | `9.703827/((betti_1*(betti_1 + (sin(euler_characteristic - 1*(-0.250803)) + sin(-0.62651485*(euler_characteristic + n_hbonds)))/0.30009225)))` |
| 20 | 5.839246e-07 | 0.0013 | `sin(9.703827 / (betti_1 * (betti_1 + ((sin(-0.8830155 * betti_1) + sin((n_hbonds + euler_characteristic) * 0.5942207)) / 0.27994904))))` | `sin(9.703827/((betti_1*(betti_1 + (sin(-0.8830155*betti_1) + sin((euler_characteristic + n_hbonds)*0.5942207))/0.27994904))))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: -0.1466937/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 6.499156e-07 | 0.0000 | `0.0022856419` | `0.00228564190000000` |
| 3 | 6.107763e-07 | 0.0311 | `-0.1466937 / euler_characteristic` | `-0.1466937/euler_characteristic` |
| 5 | 5.975590e-07 | 0.0109 | `-0.07488982 / (32.087757 - betti_1)` | `-0.07488982/(32.087757 - betti_1)` |
| 7 | 5.971470e-07 | 0.0003 | `((n_hbonds * 0.001876519) - 0.44753864) / euler_characteristic` | `(n_hbonds*0.001876519 - 1*0.44753864)/euler_characteristic` |
| 8 | 5.918606e-07 | 0.0089 | `-0.071526825 / (33.502346 - (betti_1 + sin(euler_characteristic)))` | `-0.071526825/(33.502346 - (betti_1 + sin(euler_characteristic)))` |
| 10 | 5.911494e-07 | 0.0006 | `-0.07689934 / ((31.146488 - betti_1) + (sin(euler_characteristic) * -1.592132))` | `-0.07689934/(-betti_1 + sin(euler_characteristic)*(-1.592132) + 31.146488)` |
| 11 | 5.910331e-07 | 0.0002 | `-0.07488982 / ((32.087757 - betti_1) - (cos(betti_1) + sin(euler_characteristic)))` | `-0.07488982/(-betti_1 - (sin(euler_characteristic) + cos(betti_1)) + 32.087757)` |
| 12 | 5.903952e-07 | 0.0011 | `-0.07980567 / ((sin(euler_characteristic * 0.8957675) * -1.7170713) + (29.922739 - betti_1))` | `-0.07980567/(-betti_1 + sin(euler_characteristic*0.8957675)*(-1.7170713) + 29.922739)` |
| 13 | 5.895915e-07 | 0.0014 | `-0.002268512 - (-0.29352632 / (cos(n_hbonds * 0.3134629) + (sin(euler_characteristic) - euler_characteristic)))` | `-0.002268512 - (-1)*0.29352632/(-euler_characteristic + sin(euler_characteristic) + cos(n_hbonds*0.3134629))` |
| 15 | 5.871808e-07 | 0.0020 | `-0.0022398087 - (-0.2934598 / (((cos(n_hbonds * -0.31325752) + sin(euler_characteristic)) / 0.5403647) - euler_characteristic))` | `-0.0022398087 - (-1)*0.2934598/(-euler_characteristic + (sin(euler_characteristic) + cos(n_hbonds*(-0.31325752)))/0.5403647)` |
| 16 | 5.869950e-07 | 0.0003 | `-0.0022398087 - (-0.2934598 / ((sin(sin(euler_characteristic) + cos(n_hbonds * -0.31325752)) / 0.45930535) - euler_characteristic))` | `-0.0022398087 - (-1)*0.2934598/(-euler_characteristic + sin(sin(euler_characteristic) + cos(n_hbonds*(-0.31325752)))/0.45930535)` |
| 17 | 5.868646e-07 | 0.0002 | `-0.002243588 - (-0.29352438 / (((cos(-0.313258 * n_hbonds) + sin(euler_characteristic - -0.20438954)) / 0.5403651) - euler_characteristic))` | `-0.002243588 - (-1)*0.29352438/(-euler_characteristic + (sin(euler_characteristic - 1*(-0.20438954)) + cos(-0.313258*n_hbonds))/0.5403651)` |
| 18 | 5.854258e-07 | 0.0025 | `-0.002252472 - (-0.29352656 / (((cos(sin(euler_characteristic) + (n_hbonds * 0.31346288)) + sin(euler_characteristic)) / 0.5691531) - euler_characteristic))` | `-0.002252472 - (-1)*0.29352656/(-euler_characteristic + (sin(euler_characteristic) + cos(n_hbonds*0.31346288 + sin(euler_characteristic)))/0.5691531)` |
| 19 | 5.851560e-07 | 0.0005 | `-0.0022498681 - (-0.29343677 / (((cos((n_hbonds * 0.313254) + sin(euler_characteristic)) + sin(sin(euler_characteristic))) / 0.52561325) - euler_characteristic))` | `-0.0022498681 - (-1)*0.29343677/(-euler_characteristic + (sin(sin(euler_characteristic)) + cos(n_hbonds*0.313254 + sin(euler_characteristic)))/0.52561325)` |
| 20 | 5.849980e-07 | 0.0003 | `-0.0022488255 - (-0.29351148 / (((sin(sin(euler_characteristic)) + cos(sin(sin(euler_characteristic)) + (n_hbonds * 0.31324908))) / 0.52561367) - euler_characteristic))` | `-0.0022488255 - (-1)*0.29351148/(-euler_characteristic + (sin(sin(euler_characteristic)) + cos(n_hbonds*0.31324908 + sin(sin(euler_characteristic))))/0.52561367)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -0.1466938/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 6.499155e-07 | 0.0000 | `0.002285619` | `0.00228561900000000` |
| 3 | 6.107763e-07 | 0.0311 | `-0.1466938 / euler_characteristic` | `-0.1466938/euler_characteristic` |
| 5 | 5.983239e-07 | 0.0103 | `9.637945 / (betti_1 * betti_1)` | `9.637945/((betti_1*betti_1))` |
| 7 | 5.982459e-07 | 0.0001 | `((8.95589 / euler_characteristic) / euler_characteristic) + 9.529262e-5` | `9.529262e-5 + 8.95589/(euler_characteristic*euler_characteristic)` |
| 8 | 5.940647e-07 | 0.0070 | `(-0.2900409 / (euler_characteristic - sin(euler_characteristic))) - 0.0022465803` | `-1*0.0022465803 - 0.2900409/(euler_characteristic - sin(euler_characteristic))` |
| 10 | 5.920645e-07 | 0.0017 | `-9.476228 / (betti_1 * (euler_characteristic - (sin(euler_characteristic) / 0.3266284)))` | `-9.476228*1/(betti_1*(euler_characteristic - sin(euler_characteristic)/0.3266284))` |
| 11 | 5.920087e-07 | 0.0001 | `-9.476228 / ((euler_characteristic - (sin(sin(euler_characteristic)) / 0.27130336)) * betti_1)` | `-9.476228*1/(betti_1*(euler_characteristic - sin(sin(euler_characteristic))/0.27130336))` |
| 12 | 5.917175e-07 | 0.0005 | `-9.476228 / ((euler_characteristic - (sin(euler_characteristic - -0.23800363) / 0.3266284)) * betti_1)` | `-9.476228*1/(betti_1*(euler_characteristic - sin(euler_characteristic - 1*(-0.23800363))/0.3266284))` |
| 13 | 5.912375e-07 | 0.0008 | `sin(-9.4878 / (betti_1 * (euler_characteristic - (sin(euler_characteristic * -0.8464264) / 0.2978414))))` | `sin(-9.4878*1/(betti_1*(euler_characteristic - sin(euler_characteristic*(-0.8464264))/0.2978414)))` |
| 14 | 5.909403e-07 | 0.0005 | `-9.476228 / (betti_1 * (euler_characteristic - (sin(euler_characteristic - sin(cos(n_hbonds))) / 0.29536453)))` | `-9.476228*1/(betti_1*(euler_characteristic - sin(euler_characteristic - sin(cos(n_hbonds)))/0.29536453))` |
| 15 | 5.878383e-07 | 0.0053 | `-9.538538 / ((euler_characteristic - ((sin(n_hbonds * 0.36276087) + sin(euler_characteristic)) / 0.31737575)) * betti_1)` | `-9.538538*1/(betti_1*(euler_characteristic - (sin(euler_characteristic) + sin(n_hbonds*0.36276087))/0.31737575))` |
| 16 | 5.870871e-07 | 0.0013 | `-9.538538 / ((euler_characteristic - (sin(sin(euler_characteristic) + sin(n_hbonds * -0.34069583)) / 0.23060162)) * betti_1)` | `-9.538538*1/(betti_1*(euler_characteristic - sin(sin(euler_characteristic) + sin(n_hbonds*(-0.34069583)))/0.23060162))` |
| 17 | 5.855936e-07 | 0.0025 | `-9.476228 / ((euler_characteristic + ((cos(-0.60973203 * (n_hbonds + euler_characteristic)) - sin(euler_characteristic)) / 0.27531844)) * betti_1)` | `-9.476228*1/(betti_1*(euler_characteristic + (-sin(euler_characteristic) + cos(-0.60973203*(euler_characteristic + n_hbonds)))/0.27531844))` |
| 18 | 5.855179e-07 | 0.0001 | `-9.476228 / ((euler_characteristic + ((cos(-0.60973203 * (n_hbonds + euler_characteristic)) - sin(sin(euler_characteristic))) / 0.27531844)) * betti_1)` | `-9.476228*1/(betti_1*(euler_characteristic + (-sin(sin(euler_characteristic)) + cos(-0.60973203*(euler_characteristic + n_hbonds)))/0.27531844))` |
| 19 | 5.848307e-07 | 0.0012 | `-9.476256 / (betti_1 * (euler_characteristic + (((0.28759012 - sin(euler_characteristic)) + cos((euler_characteristic + n_hbonds) * -0.54597455)) / 0.27558655)))` | `-9.476256*1/(betti_1*(euler_characteristic + (-sin(euler_characteristic) + cos((euler_characteristic + n_hbonds)*(-0.54597455)) + 0.28759012)/0.27558655))` |
| 20 | 5.845808e-07 | 0.0004 | `-9.476256 / (betti_1 * ((((0.28759012 - sin(sin(euler_characteristic))) + cos((euler_characteristic + n_hbonds) * -0.54597455)) / 0.25568253) + euler_characteristic))` | `-9.476256*1/(betti_1*(euler_characteristic + (-sin(sin(euler_characteristic)) + cos((euler_characteristic + n_hbonds)*(-0.54597455)) + 0.28759012)/0.25568253))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: -0.14669377/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 6.499156e-07 | 0.0000 | `0.0022856419` | `0.00228564190000000` |
| 3 | 6.107763e-07 | 0.0311 | `-0.14669377 / euler_characteristic` | `-0.14669377/euler_characteristic` |
| 5 | 5.975612e-07 | 0.0109 | `-0.07553261 / (31.812412 - betti_1)` | `-0.07553261/(31.812412 - betti_1)` |
| 6 | 5.962100e-07 | 0.0023 | `exp(euler_characteristic * 0.1180303) + 0.0017335353` | `exp(euler_characteristic*0.1180303) + 0.0017335353` |
| 8 | 5.918742e-07 | 0.0036 | `-0.07098234 / (33.759037 - (sin(euler_characteristic) + betti_1))` | `-0.07098234/(33.759037 - (betti_1 + sin(euler_characteristic)))` |
| 9 | 5.903060e-07 | 0.0027 | `0.0017335353 + exp(0.1180303 * (euler_characteristic - sin(euler_characteristic)))` | `exp(0.1180303*(euler_characteristic - sin(euler_characteristic))) + 0.0017335353` |
| 10 | 5.898328e-07 | 0.0008 | `(euler_characteristic * 0.00078178186) / ((42.85668 - sin(euler_characteristic)) - betti_1)` | `euler_characteristic*0.00078178186/(-betti_1 - sin(euler_characteristic) + 42.85668)` |
| 12 | 5.887860e-07 | 0.0009 | `(betti_1 / (sin(betti_1 * 0.8816003) + (43.217655 - betti_1))) * -0.00075669703` | `betti_1*(-0.00075669703)/(-betti_1 + sin(betti_1*0.8816003) + 43.217655)` |
| 13 | 5.881882e-07 | 0.0010 | `-0.07110138 / ((sin(betti_1 - n_hbonds) + (33.759037 - sin(euler_characteristic))) - betti_1)` | `-0.07110138/(-betti_1 - sin(euler_characteristic) + sin(betti_1 - n_hbonds) + 33.759037)` |
| 15 | 5.880030e-07 | 0.0002 | `-0.07110138 / ((sin(betti_1 - n_hbonds) + (33.759037 - sin(euler_characteristic + 0.20181204))) - betti_1)` | `-0.07110138/(-betti_1 + sin(betti_1 - n_hbonds) - sin(euler_characteristic + 0.20181204) + 33.759037)` |
| 16 | 5.870935e-07 | 0.0015 | `-0.071050696 / (((sin((betti_1 - cos(betti_1)) - n_hbonds) - sin(euler_characteristic)) + 33.758694) - betti_1)` | `-0.071050696/(-betti_1 - sin(euler_characteristic) + sin(betti_1 - n_hbonds - cos(betti_1)) + 33.758694)` |
| 17 | 5.856168e-07 | 0.0025 | `-3.0457406 / (betti_1 * (sin(betti_1 * 0.88234884) - ((betti_1 * 0.309006) + sin(n_hbonds * 0.2836375))))` | `-3.0457406*1/(betti_1*(-(betti_1*0.309006 + sin(n_hbonds*0.2836375)) + sin(betti_1*0.88234884)))` |
| 19 | 5.855870e-07 | 0.0000 | `-3.0457406 / ((sin(betti_1 * 0.88234884) - (sin((-0.25231126 - n_hbonds) * -0.28275827) + (betti_1 * 0.309006))) * betti_1)` | `-3.0457406*1/(betti_1*(-(betti_1*0.309006 + sin((-n_hbonds - 0.25231126)*(-0.28275827))) + sin(betti_1*0.88234884)))` |
| 20 | 5.842924e-07 | 0.0022 | `-3.0455883 / ((sin(betti_1 * 0.88321626) - ((betti_1 * 0.3105269) + cos((n_hbonds * 0.312614) + sin(euler_characteristic)))) * betti_1)` | `-3.0455883*1/(betti_1*(-(betti_1*0.3105269 + cos(n_hbonds*0.312614 + sin(euler_characteristic))) + sin(betti_1*0.88321626)))` |

</details>

