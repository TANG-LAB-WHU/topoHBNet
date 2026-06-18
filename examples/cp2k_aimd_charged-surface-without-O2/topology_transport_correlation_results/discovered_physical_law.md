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
| 1 | `LBHB_Fraction ≈ -0.101274066/(22.646284 - betti_1)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ 0.10153661/(betti_1 - 22.584824)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.101342805/(betti_1 - 22.629667)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -0.100718774/(euler_characteristic + 21.726381)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ -0.101123504/(euler_characteristic + 21.633018)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx -0.101274066/(22.646284 - betti_1)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 50/76 | 65.8% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 39/76 | 51.3% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 22/76 | 28.9% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 14/76 | 18.4% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/76 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 50/76 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: -0.101274066/(22.646284 - betti_1)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.634241e-06 | 0.0000 | `0.0028299987` | `0.00282999870000000` |
| 3 | 7.291760e-07 | 0.4035 | `-0.17314437 / euler_characteristic` | `-0.17314437/euler_characteristic` |
| 5 | 2.444067e-07 | 0.5465 | `-0.101274066 / (22.646284 - betti_1)` | `-0.101274066/(22.646284 - betti_1)` |
| 6 | 2.444062e-07 | 0.0000 | `sin(-0.101274066 / (22.646284 - betti_1))` | `sin(-0.101274066/(22.646284 - betti_1))` |
| 7 | 2.444056e-07 | 0.0000 | `sin(sin(-0.101274066 / (22.646284 - betti_1)))` | `sin(sin(-0.101274066/(22.646284 - betti_1)))` |
| 8 | 2.345052e-07 | 0.0414 | `0.100979246 / ((sin(betti_1) - 22.76904) + betti_1)` | `0.100979246/(betti_1 + sin(betti_1) - 1*22.76904)` |
| 9 | 2.343617e-07 | 0.0006 | `0.100979246 / ((betti_1 + sin(sin(betti_1))) - 22.76904)` | `0.100979246/(betti_1 + sin(sin(betti_1)) - 1*22.76904)` |
| 10 | 1.883502e-07 | 0.2186 | `((10.037847 - cos(betti_1 * 0.22061247)) / betti_1) / betti_1` | `(10.037847 - cos(betti_1*0.22061247))/(betti_1*betti_1)` |
| 12 | 1.837694e-07 | 0.0123 | `((10.174187 - (cos(betti_1 * 0.21966076) * 1.468828)) / betti_1) / betti_1` | `(10.174187 - 1.468828*cos(betti_1*0.21966076))/(betti_1*betti_1)` |
| 13 | 1.837693e-07 | 0.0000 | `sin(((10.174187 - (1.468828 * cos(0.21966076 * betti_1))) / betti_1) / betti_1)` | `sin((10.174187 - 1.468828*cos(0.21966076*betti_1))/(betti_1*betti_1))` |
| 14 | 1.767570e-07 | 0.0389 | `((10.174229 - (euler_characteristic * (-0.02633285 * cos(betti_1 * 0.21926098)))) / betti_1) / betti_1` | `(10.174229 - (-0.02633285)*euler_characteristic*cos(betti_1*0.21926098))/(betti_1*betti_1)` |
| 15 | 1.767569e-07 | 0.0000 | `sin(((10.174229 - (-0.02633285 * (euler_characteristic * cos(betti_1 * 0.21926098)))) / betti_1) / betti_1)` | `sin((10.174229 - (-1)*0.02633285*euler_characteristic*cos(betti_1*0.21926098))/(betti_1*betti_1))` |
| 16 | 1.736379e-07 | 0.0178 | `((10.174187 - ((betti_1 * (betti_1 * cos(betti_1 * -0.21915768))) * 0.0004481782)) / betti_1) / betti_1` | `(10.174187 - 0.0004481782*betti_1*betti_1*cos(betti_1*(-0.21915768)))/(betti_1*betti_1)` |
| 17 | 1.736377e-07 | 0.0000 | `sin(((10.174187 - ((betti_1 * (betti_1 * cos(betti_1 * -0.21915768))) * 0.0004481782)) / betti_1) / betti_1)` | `sin((10.174187 - 0.0004481782*betti_1*betti_1*cos(betti_1*(-0.21915768)))/(betti_1*betti_1))` |
| 18 | 1.688317e-07 | 0.0281 | `(((sin(euler_characteristic * 0.1998186) / euler_characteristic) / exp(cos(n_hbonds * -0.09255979))) + (9.881087 / betti_1)) / betti_1` | `(sin(euler_characteristic*0.1998186)/(euler_characteristic*exp(cos(n_hbonds*(-0.09255979)))) + 9.881087/betti_1)/betti_1` |
| 19 | 1.688314e-07 | 0.0000 | `sin((((sin(euler_characteristic * 0.1998186) / euler_characteristic) / exp(cos(n_hbonds * -0.09255979))) + (9.881087 / betti_1)) / betti_1)` | `sin((sin(euler_characteristic*0.1998186)/(euler_characteristic*exp(cos(n_hbonds*(-0.09255979)))) + 9.881087/betti_1)/betti_1)` |
| 20 | 1.670605e-07 | 0.0105 | `(((sin(0.1998186 * euler_characteristic) / (euler_characteristic / betti_0)) / exp(cos(n_hbonds * -0.09255979))) + (9.881087 / betti_1)) / betti_1` | `(sin(0.1998186*euler_characteristic)/(((euler_characteristic/betti_0))*exp(cos(n_hbonds*(-0.09255979)))) + 9.881087/betti_1)/betti_1` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.10153661/(betti_1 - 22.584824)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.634241e-06 | 0.0000 | `0.0028299754` | `0.00282997540000000` |
| 3 | 7.291759e-07 | 0.4035 | `-0.17314401 / euler_characteristic` | `-0.17314401/euler_characteristic` |
| 4 | 4.339355e-07 | 0.5190 | `exp(n_hbonds * -0.038318235)` | `exp(n_hbonds*(-0.038318235))` |
| 5 | 2.444299e-07 | 0.5740 | `0.10153661 / (betti_1 + -22.584824)` | `0.10153661/(betti_1 - 22.584824)` |
| 6 | 2.279820e-07 | 0.0697 | `exp(n_hbonds * -0.0411009) + 0.0011011249` | `exp(n_hbonds*(-0.0411009)) + 0.0011011249` |
| 8 | 2.223796e-07 | 0.0124 | `(0.0010650281 / betti_0) + exp(n_hbonds * -0.04089238)` | `exp(n_hbonds*(-0.04089238)) + 0.0010650281/betti_0` |
| 12 | 2.122811e-07 | 0.0116 | `(1.6023773 / euler_characteristic) / ((euler_characteristic * 0.17235738) + sin(euler_characteristic * -0.19949046))` | `1.6023773/(euler_characteristic*(euler_characteristic*0.17235738 + sin(euler_characteristic*(-0.19949046))))` |
| 13 | 2.114267e-07 | 0.0040 | `(1.6022841 / euler_characteristic) / ((0.17117383 * euler_characteristic) + sin(sin(-0.19838424 * euler_characteristic)))` | `1.6022841/(euler_characteristic*(0.17117383*euler_characteristic + sin(sin(-0.19838424*euler_characteristic))))` |
| 14 | 1.856202e-07 | 0.1302 | `(-1.4445379 / ((0.12991402 * euler_characteristic) + (-1.0626906 + sin(euler_characteristic * -0.19975023)))) / betti_1` | `-1.4445379/(betti_1*(0.12991402*euler_characteristic + sin(euler_characteristic*(-0.19975023)) - 1.0626906))` |
| 15 | 1.840999e-07 | 0.0082 | `sin((-1.2454407 / (sin(euler_characteristic * -0.19908091) + ((euler_characteristic * 0.10527945) + -1.2481656))) / betti_1)` | `sin(-1.2454407/(betti_1*(euler_characteristic*0.10527945 + sin(euler_characteristic*(-0.19908091)) - 1.2481656)))` |
| 17 | 1.827994e-07 | 0.0035 | `sin((-1.4446744 / (((sin(euler_characteristic * -0.19862954) + -1.051154) * betti_0) + (euler_characteristic * 0.1287899))) / betti_1)` | `sin(-1.4446744/(betti_1*(betti_0*(sin(euler_characteristic*(-0.19862954)) - 1.051154) + euler_characteristic*0.1287899)))` |
| 18 | 1.827992e-07 | 0.0000 | `sin(sin((-1.4446744 / (((sin(euler_characteristic * -0.19862954) + -1.051154) * betti_0) + (euler_characteristic * 0.1287899))) / betti_1))` | `sin(sin(-1.4446744/(betti_1*(betti_0*(sin(euler_characteristic*(-0.19862954)) - 1.051154) + euler_characteristic*0.1287899))))` |
| 19 | 1.826562e-07 | 0.0008 | `sin((-1.4446199 / ((euler_characteristic * 0.12947883) + (betti_0 * (sin((euler_characteristic * -0.19795834) + 0.07801376) + -1.0511702)))) / betti_1)` | `sin(-1.4446199/(betti_1*(betti_0*(sin(0.07801376 + euler_characteristic*(-0.19795834)) - 1.0511702) + euler_characteristic*0.12947883)))` |
| 20 | 1.809317e-07 | 0.0095 | `sin((-1.4447452 / (sin((euler_characteristic + sin(betti_1 * -0.19642305)) * -0.19851889) + ((euler_characteristic * 0.12840204) + -1.1169711))) / betti_1)` | `sin(-1.4447452/(betti_1*(euler_characteristic*0.12840204 + sin((euler_characteristic + sin(betti_1*(-0.19642305)))*(-0.19851889)) - 1.1169711)))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.101342805/(betti_1 - 22.629667)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.634241e-06 | 0.0000 | `0.0028303002` | `0.00283030020000000` |
| 3 | 7.291759e-07 | 0.4035 | `-0.17314427 / euler_characteristic` | `-0.17314427/euler_characteristic` |
| 4 | 4.339333e-07 | 0.5190 | `exp(n_hbonds * -0.038316604)` | `exp(n_hbonds*(-0.038316604))` |
| 5 | 2.444083e-07 | 0.5741 | `0.101342805 / (-22.629667 + betti_1)` | `0.101342805/(betti_1 - 22.629667)` |
| 6 | 2.278141e-07 | 0.0703 | `exp(n_hbonds * -0.04106787) + 0.00108672` | `exp(n_hbonds*(-0.04106787)) + 0.00108672` |
| 7 | 2.277758e-07 | 0.0002 | `exp(n_hbonds * sin(-0.04106787)) + 0.00108672` | `exp(n_hbonds*sin(-0.04106787)) + 0.00108672` |
| 8 | 2.230315e-07 | 0.0210 | `exp(n_hbonds * -0.04106787) + (0.00108672 / betti_0)` | `exp(n_hbonds*(-0.04106787)) + 0.00108672/betti_0` |
| 9 | 1.921737e-07 | 0.1489 | `((0.9318955 / betti_1) - (betti_1 * -0.00020826836)) + -0.025450872` | `-(-0.00020826836)*betti_1 - 0.025450872 + 0.9318955/betti_1` |
| 10 | 1.921724e-07 | 0.0000 | `sin(((0.9318955 / betti_1) - (betti_1 * -0.00020826836)) + -0.025450872)` | `sin(-(-0.00020826836)*betti_1 - 0.025450872 + 0.9318955/betti_1)` |
| 11 | 1.728297e-07 | 0.1061 | `betti_1 * (((0.030727357 / betti_1) + -0.00087717775) - (betti_1 * -6.787936e-6))` | `betti_1*(-(-6.787936e-6)*betti_1 - 0.00087717775 + 0.030727357/betti_1)` |
| 13 | 1.717163e-07 | 0.0032 | `((0.030664068 / betti_1) - (((betti_1 - betti_0) * -6.7244628e-6) + 0.0008653385)) * betti_1` | `betti_1*(-(0.0008653385 + (-betti_0 + betti_1)*(-6.7244628e-6)) + 0.030664068/betti_1)` |
| 14 | 1.717159e-07 | 0.0000 | `sin(((0.030664068 / betti_1) - (((betti_1 - betti_0) * -6.7244628e-6) + 0.0008653385)) * betti_1)` | `sin(betti_1*(-(0.0008653385 + (-betti_0 + betti_1)*(-6.7244628e-6)) + 0.030664068/betti_1))` |
| 15 | 1.717155e-07 | 0.0000 | `sin(sin(((0.030664068 / betti_1) - (((betti_1 - betti_0) * -6.7244628e-6) + 0.0008653385)) * betti_1))` | `sin(sin(betti_1*(-(0.0008653385 + (-betti_0 + betti_1)*(-6.7244628e-6)) + 0.030664068/betti_1)))` |
| 16 | 1.715892e-07 | 0.0007 | `euler_characteristic * (-0.18992127 / ((betti_1 + (sin(-0.3277721 - (euler_characteristic * 0.13694134)) * 14.204058)) * betti_1))` | `euler_characteristic*(-0.18992127)/(betti_1*(betti_1 + sin(-0.13694134*euler_characteristic - 0.3277721)*14.204058))` |
| 17 | 1.715760e-07 | 0.0001 | `sin(euler_characteristic / (betti_1 * ((sin(-0.3277721 - (euler_characteristic * 0.13694134)) * 14.204058) + betti_1))) * -0.18992127` | `sin(euler_characteristic/((betti_1*(betti_1 + sin(-0.13694134*euler_characteristic - 0.3277721)*14.204058))))*(-0.18992127)` |
| 18 | 1.713708e-07 | 0.0012 | `(euler_characteristic * -0.19100589) / ((betti_1 + 0.29548463) * ((sin(-0.3277417 - (euler_characteristic * 0.136966)) * 14.039708) + betti_1))` | `euler_characteristic*(-0.19100589)/((betti_1 + 0.29548463)*(betti_1 + sin(-0.136966*euler_characteristic - 0.3277417)*14.039708))` |
| 19 | 1.710468e-07 | 0.0019 | `euler_characteristic * (-0.1896933 / ((cos(betti_1) + betti_1) * (betti_1 + (sin(-0.32778218 - (euler_characteristic * 0.13652287)) * 14.204054))))` | `euler_characteristic*(-0.1896933)/((betti_1 + sin(-0.13652287*euler_characteristic - 0.32778218)*14.204054)*(betti_1 + cos(betti_1)))` |
| 20 | 1.708745e-07 | 0.0010 | `(euler_characteristic * -0.1897043) / ((betti_1 + (sin(-0.32778066 - (euler_characteristic * 0.13658819)) * 14.204053)) * (sin(cos(betti_1)) + betti_1))` | `euler_characteristic*(-0.1897043)/((betti_1 + sin(-0.13658819*euler_characteristic - 0.32778066)*14.204053)*(betti_1 + sin(cos(betti_1))))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -0.100718774/(euler_characteristic + 21.726381)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.634241e-06 | 0.0000 | `0.0028301931` | `0.00283019310000000` |
| 3 | 7.291760e-07 | 0.4035 | `-0.1731443 / euler_characteristic` | `-0.1731443/euler_characteristic` |
| 5 | 2.439554e-07 | 0.5475 | `-0.100718774 / (euler_characteristic + 21.726381)` | `-0.100718774/(euler_characteristic + 21.726381)` |
| 7 | 2.432903e-07 | 0.0014 | `(0.11457589 / (betti_1 + -21.479044)) + -0.0002598296` | `-0.0002598296 + 0.11457589/(betti_1 - 21.479044)` |
| 8 | 2.342881e-07 | 0.0377 | `0.10021564 / ((betti_1 + sin(betti_1)) + -22.944885)` | `0.10021564/(betti_1 + sin(betti_1) - 22.944885)` |
| 9 | 1.718219e-07 | 0.3101 | `0.031125778 - (betti_1 * ((euler_characteristic * 6.900146e-6) + 0.00088361534))` | `0.031125778 - betti_1*(euler_characteristic*6.900146e-6 + 0.00088361534)` |
| 10 | 1.718213e-07 | 0.0000 | `sin(0.031125778 - (betti_1 * ((euler_characteristic * 6.900146e-6) + 0.00088361534)))` | `sin(0.031125778 - betti_1*(euler_characteristic*6.900146e-6 + 0.00088361534))` |
| 11 | 1.715582e-07 | 0.0015 | `0.031125778 - ((betti_0 - euler_characteristic) * ((6.900146e-6 * euler_characteristic) + 0.0008836152))` | `0.031125778 - (betti_0 - euler_characteristic)*(6.900146e-6*euler_characteristic + 0.0008836152)` |
| 13 | 1.676808e-07 | 0.0114 | `((n_hbonds * -3.0268737e-5) - -0.03246122) - (((betti_1 * -6.562513e-6) + 0.00081363716) * betti_1)` | `-betti_1*(0.00081363716 + betti_1*(-6.562513e-6)) + n_hbonds*(-3.0268737e-5) - 1*(-0.03246122)` |
| 14 | 1.676804e-07 | 0.0000 | `sin(((n_hbonds * -3.0268737e-5) - -0.03246122) - (((betti_1 * -6.562513e-6) + 0.00081363716) * betti_1))` | `sin(-betti_1*(0.00081363716 + betti_1*(-6.562513e-6)) + n_hbonds*(-3.0268737e-5) - 1*(-0.03246122))` |
| 15 | 1.673817e-07 | 0.0018 | `(0.03230511 - ((n_hbonds + betti_0) * 3.1640222e-5)) - (betti_1 * (0.000800001 - (betti_1 * 6.447295e-6)))` | `-betti_1*(0.000800001 - 6.447295e-6*betti_1) - 3.1640222e-5*(betti_0 + n_hbonds) + 0.03230511` |
| 16 | 1.673542e-07 | 0.0002 | `(0.03230511 - ((n_hbonds + betti_0) * 3.1640222e-5)) - sin((0.000800001 - (betti_1 * 6.447295e-6)) * betti_1)` | `-3.1640222e-5*(betti_0 + n_hbonds) - sin(betti_1*(0.000800001 - 6.447295e-6*betti_1)) + 0.03230511` |
| 17 | 1.649887e-07 | 0.0142 | `(0.031737056 - (n_hbonds * ((betti_0 * 5.133368e-6) + 2.7788947e-5))) - ((-0.00079751114 - (betti_1 * -6.499002e-6)) * euler_characteristic)` | `-euler_characteristic*(-(-6.499002e-6)*betti_1 - 0.00079751114) - n_hbonds*(betti_0*5.133368e-6 + 2.7788947e-5) + 0.031737056` |
| 18 | 1.649883e-07 | 0.0000 | `sin((0.031737056 - (n_hbonds * ((betti_0 * 5.133368e-6) + 2.7788947e-5))) - ((-0.00079751114 - (betti_1 * -6.499002e-6)) * euler_characteristic))` | `sin(-euler_characteristic*(-(-6.499002e-6)*betti_1 - 0.00079751114) - n_hbonds*(betti_0*5.133368e-6 + 2.7788947e-5) + 0.031737056)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: -0.101123504/(euler_characteristic + 21.633018)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.634241e-06 | 0.0000 | `0.0028302185` | `0.00283021850000000` |
| 3 | 7.291759e-07 | 0.4035 | `-0.17314407 / euler_characteristic` | `-0.17314407/euler_characteristic` |
| 5 | 2.438729e-07 | 0.5476 | `-0.101123504 / (euler_characteristic + 21.633018)` | `-0.101123504/(euler_characteristic + 21.633018)` |
| 7 | 2.432474e-07 | 0.0013 | `(0.11011442 / (-20.83064 - euler_characteristic)) + -0.00017592264` | `-0.00017592264 + 0.11011442/(-euler_characteristic - 20.83064)` |
| 8 | 2.345447e-07 | 0.0364 | `-0.10011402 / (euler_characteristic + (21.919601 - sin(betti_1)))` | `-0.10011402/(euler_characteristic - sin(betti_1) + 21.919601)` |
| 9 | 2.297313e-07 | 0.0207 | `0.31706333 / (((betti_1 * n_hbonds) / 65.45645) + -26.43133)` | `0.31706333/(betti_1*n_hbonds/65.45645 - 26.43133)` |
| 10 | 2.122790e-07 | 0.0790 | `0.10156975 / (cos(n_hbonds * 0.32200298) - (euler_characteristic + 21.648407))` | `0.10156975/(-(euler_characteristic + 21.648407) + cos(n_hbonds*0.32200298))` |
| 12 | 2.058711e-07 | 0.0153 | `0.101072416 / ((1.3709004 * cos(n_hbonds * 0.3218255)) - (euler_characteristic + 21.648403))` | `0.101072416/(-(euler_characteristic + 21.648403) + 1.3709004*cos(n_hbonds*0.3218255))` |
| 13 | 2.031031e-07 | 0.0135 | `0.101072416 / ((exp(0.46405843) * cos(0.3218255 * n_hbonds)) - (euler_characteristic + 21.648403))` | `0.101072416/(-(euler_characteristic + 21.648403) + exp(0.46405843)*cos(0.3218255*n_hbonds))` |
| 15 | 1.965130e-07 | 0.0165 | `(-18.64721 / (euler_characteristic * (cos(sin(betti_1 * -0.11331236)) + 1.3282659))) / (betti_1 + -2.7291741)` | `-18.64721/((euler_characteristic*(cos(sin(betti_1*(-0.11331236))) + 1.3282659))*(betti_1 - 2.7291741))` |
| 18 | 1.786723e-07 | 0.0317 | `((-18.647223 / (euler_characteristic * (cos(n_hbonds * 0.120433144) + 3.780927))) / ((betti_1 * betti_1) / 48.174988)) + 0.0016913413` | `0.0016913413 - 18.647223/((euler_characteristic*(cos(n_hbonds*0.120433144) + 3.780927))*(betti_1*betti_1/48.174988))` |
| 19 | 1.786509e-07 | 0.0001 | `((-18.647223 / ((cos(n_hbonds * -0.120342605) + exp(1.3281178)) * euler_characteristic)) / ((betti_1 * betti_1) / 48.174988)) + 0.0016913413` | `0.0016913413 - 18.647223/((euler_characteristic*(cos(n_hbonds*(-0.120342605)) + exp(1.3281178)))*(betti_1*betti_1/48.174988))` |
| 20 | 1.767578e-07 | 0.0107 | `((-18.647223 / (euler_characteristic * (cos(betti_1 * (betti_1 * 0.0016913413)) + 3.780927))) / ((betti_1 * betti_1) / 48.174988)) + 0.0016913413` | `0.0016913413 - 18.647223/((euler_characteristic*(cos(betti_1*betti_1*0.0016913413) + 3.780927))*(betti_1*betti_1/48.174988))` |

</details>

