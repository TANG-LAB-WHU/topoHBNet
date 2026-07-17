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
| 1 | `LBHB_Fraction ≈ 0.18348736/betti_1` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ 0.1834876/betti_1` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.18348704/betti_1` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ 0.18348734/betti_1` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.18348749/betti_1` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx 0.18348736/betti_1$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 47/67 | 70.1% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 40/67 | 59.7% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 22/67 | 32.8% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 14/67 | 20.9% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/67 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 47/67 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: 0.18348736/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535803` | `0.00285358030000000` |
| 3 | 1.806214e-07 | 0.0919 | `0.18348736 / betti_1` | `0.18348736/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348756 / betti_1)` | `sin(0.18348756/betti_1)` |
| 5 | 1.796619e-07 | 0.0053 | `(0.15725112 / betti_1) - -0.00040970184` | `-1*(-0.00040970184) + 0.15725112/betti_1` |
| 6 | 1.776502e-07 | 0.0113 | `exp(euler_characteristic * 0.13069943) + 0.002555587` | `exp(euler_characteristic*0.13069943) + 0.002555587` |
| 7 | 1.768643e-07 | 0.0044 | `(n_hbonds * (0.0016492459 / betti_1)) + -0.0013280835` | `-0.0013280835 + n_hbonds*0.0016492459/betti_1` |
| 8 | 1.742947e-07 | 0.0146 | `-0.0023818456 / sin(n_hbonds * (-0.84345263 / betti_1))` | `-0.0023818456/sin(n_hbonds*(-0.84345263)/betti_1)` |
| 10 | 1.733369e-07 | 0.0028 | `-0.014142922 / (-4.4477344 + sin((-3.4733543 / betti_1) * n_hbonds))` | `-0.014142922/(sin(-3.4733543*n_hbonds/betti_1) - 4.4477344)` |
| 11 | 1.733369e-07 | 0.0000 | `sin(-0.014142922 / (-4.4477344 + sin((-3.4733543 / betti_1) * n_hbonds)))` | `sin(-0.014142922/(sin(-3.4733543*n_hbonds/betti_1) - 4.4477344))` |
| 12 | 1.725803e-07 | 0.0044 | `-0.014349711 / (sin(betti_0 + ((n_hbonds * -3.820718) / betti_1)) + -4.4442997)` | `-0.014349711/(sin(betti_0 + n_hbonds*(-3.820718)/betti_1) - 4.4442997)` |
| 13 | 1.725802e-07 | 0.0000 | `sin(-0.014349711 / (sin(betti_0 + ((n_hbonds * -3.820718) / betti_1)) + -4.4442997))` | `sin(-0.014349711/(sin(betti_0 + n_hbonds*(-3.820718)/betti_1) - 4.4442997))` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.1834876/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535791` | `0.00285357910000000` |
| 3 | 1.806214e-07 | 0.0919 | `0.1834876 / betti_1` | `0.1834876/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348743 / betti_1)` | `sin(0.18348743/betti_1)` |
| 5 | 1.796604e-07 | 0.0053 | `0.00039524215 - (-0.15820639 / betti_1)` | `0.00039524215 - (-1)*0.15820639/betti_1` |
| 6 | 1.796582e-07 | 0.0000 | `exp(0.15850994 / betti_1) - 0.9996126` | `exp(0.15850994/betti_1) - 1*0.9996126` |
| 7 | 1.764989e-07 | 0.0177 | `0.0019408707 / cos(cos(n_hbonds / betti_1))` | `0.0019408707/cos(cos(n_hbonds/betti_1))` |
| 8 | 1.745114e-07 | 0.0113 | `0.0025485833 / sin((n_hbonds / betti_1) + -0.51930714)` | `0.0025485833/sin(-0.51930714 + n_hbonds/betti_1)` |
| 9 | 1.735574e-07 | 0.0055 | `0.00259253 / cos(sin((n_hbonds / -0.71361566) / betti_1))` | `0.00259253/cos(sin(n_hbonds/((-0.71361566)*betti_1)))` |
| 10 | 1.735574e-07 | 0.0000 | `sin(0.00259253 / cos(sin((n_hbonds / -0.71361566) / betti_1)))` | `sin(0.00259253/cos(sin(n_hbonds/((-0.71361566)*betti_1))))` |
| 11 | 1.723327e-07 | 0.0071 | `0.0023077528 / cos(sin(cos(sin(3.2903008 / (betti_1 / n_hbonds)))))` | `0.0023077528/cos(sin(cos(sin(3.2903008/((betti_1/n_hbonds))))))` |
| 12 | 1.723327e-07 | 0.0000 | `sin(0.0023077528 / cos(sin(cos(sin(3.2903008 / (betti_1 / n_hbonds))))))` | `sin(0.0023077528/cos(sin(cos(sin(3.2903008/((betti_1/n_hbonds)))))))` |
| 13 | 1.718300e-07 | 0.0029 | `0.0023077528 / cos(sin(cos(sin(-3.2926533 / (betti_1 / n_hbonds)) * betti_0)))` | `0.0023077528/cos(sin(cos(betti_0*sin(-3.2926533*n_hbonds/betti_1))))` |
| 19 | 1.717054e-07 | 0.0001 | `sin(0.0023136116 / cos(sin(cos(sin(2.944526 / sin((betti_0 * 1.5294906) / ((n_hbonds / -0.59748983) / betti_1)))))))` | `sin(0.0023136116/cos(sin(cos(sin(2.944526/sin(betti_0*1.5294906/(n_hbonds/((-0.59748983)*betti_1))))))))` |
| 20 | 1.717054e-07 | 0.0000 | `sin(sin(0.0023136116 / cos(sin(cos(sin(2.944526 / sin((betti_0 * 1.5294906) / ((n_hbonds / -0.59748983) / betti_1))))))))` | `sin(sin(0.0023136116/cos(sin(cos(sin(2.944526/sin(betti_0*1.5294906/(n_hbonds/((-0.59748983)*betti_1)))))))))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.18348704/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535798` | `0.00285357980000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348704 / betti_1` | `0.18348704/betti_1` |
| 5 | 1.796604e-07 | 0.0027 | `(0.15820564 / betti_1) + 0.00039527568` | `0.00039527568 + 0.15820564/betti_1` |
| 6 | 1.776563e-07 | 0.0112 | `exp(euler_characteristic * 0.13092798) + 0.0025603233` | `exp(euler_characteristic*0.13092798) + 0.0025603233` |
| 7 | 1.766363e-07 | 0.0058 | `n_hbonds / ((14.416215 - betti_1) / -0.0008719526)` | `n_hbonds/(((14.416215 - betti_1)/(-0.0008719526)))` |
| 10 | 1.757250e-07 | 0.0017 | `n_hbonds / (euler_characteristic / (-0.0010780772 - exp(euler_characteristic * 0.16958745)))` | `n_hbonds/((euler_characteristic/(-exp(euler_characteristic*0.16958745) - 0.0010780772)))` |
| 12 | 1.751845e-07 | 0.0015 | `n_hbonds / (euler_characteristic / (-0.0010768465 - exp((euler_characteristic * 0.16852242) * betti_0)))` | `n_hbonds/((euler_characteristic/(-exp(euler_characteristic*0.16852242*betti_0) - 0.0010768465)))` |
| 15 | 1.751578e-07 | 0.0001 | `exp(0.15676972 * euler_characteristic) + (n_hbonds / ((euler_characteristic + cos(-0.239109 * euler_characteristic)) / -0.0010918295))` | `n_hbonds/(((euler_characteristic + cos(-0.239109*euler_characteristic))/(-0.0010918295))) + exp(0.15676972*euler_characteristic)` |
| 16 | 1.715021e-07 | 0.0211 | `(euler_characteristic + n_hbonds) / ((11.774071 / sin((euler_characteristic * -0.13806865) * n_hbonds)) + (euler_characteristic / -0.0018095624))` | `(euler_characteristic + n_hbonds)/(euler_characteristic/(-0.0018095624) + 11.774071/sin(euler_characteristic*(-0.13806865)*n_hbonds))` |
| 18 | 1.714148e-07 | 0.0003 | `((0.788351 - betti_1) + n_hbonds) / ((11.774071 / sin((n_hbonds * euler_characteristic) * -0.13806865)) + (euler_characteristic / -0.0018095624))` | `(-betti_1 + n_hbonds + 0.788351)/(euler_characteristic/(-0.0018095624) + 11.774071/sin(n_hbonds*euler_characteristic*(-0.13806865)))` |
| 19 | 1.713336e-07 | 0.0005 | `sin((euler_characteristic + n_hbonds) / ((euler_characteristic / -0.0018133168) - (7.5921736 / (sin((0.0065466356 - euler_characteristic) * n_hbonds) + 0.0026999651))))` | `sin((euler_characteristic + n_hbonds)/(euler_characteristic/(-0.0018133168) - 7.5921736/(sin(n_hbonds*(0.0065466356 - euler_characteristic)) + 0.0026999651)))` |
| 20 | 1.713335e-07 | 0.0000 | `sin(sin((euler_characteristic + n_hbonds) / ((euler_characteristic / -0.0018133168) - (7.5921736 / (sin((0.0065466356 - euler_characteristic) * n_hbonds) + 0.0026999651)))))` | `sin(sin((euler_characteristic + n_hbonds)/(euler_characteristic/(-0.0018133168) - 7.5921736/(sin(n_hbonds*(0.0065466356 - euler_characteristic)) + 0.0026999651))))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: 0.18348734/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535808` | `0.00285358080000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348734 / betti_1` | `0.18348734/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348685 / betti_1)` | `sin(0.18348685/betti_1)` |
| 5 | 1.796606e-07 | 0.0053 | `(0.15785664 / betti_1) - -0.00040069222` | `-1*(-0.00040069222) + 0.15785664/betti_1` |
| 6 | 1.773841e-07 | 0.0128 | `exp(betti_1 * -0.1282341) + 0.0025500348` | `exp(betti_1*(-0.1282341)) + 0.0025500348` |
| 7 | 1.773835e-07 | 0.0000 | `sin(exp(betti_1 * -0.12817253) + 0.0025489859)` | `sin(exp(betti_1*(-0.12817253)) + 0.0025489859)` |
| 8 | 1.767417e-07 | 0.0036 | `exp((betti_1 * betti_0) * -0.1282327) + 0.0025519948` | `exp(betti_1*betti_0*(-0.1282327)) + 0.0025519948` |
| 9 | 1.767417e-07 | 0.0000 | `sin(0.0025519948 + exp((betti_1 * betti_0) * -0.1282327))` | `sin(exp(betti_1*betti_0*(-0.1282327)) + 0.0025519948)` |
| 10 | 1.725966e-07 | 0.0237 | `0.020901145 / (cos(-5.3401866 * (n_hbonds / betti_1)) + 6.889499)` | `0.020901145/(cos(-5.3401866*n_hbonds/betti_1) + 6.889499)` |
| 11 | 1.725962e-07 | 0.0000 | `sin(0.020901145 / (6.889499 + cos(n_hbonds * (-5.340548 / betti_1))))` | `sin(0.020901145/(cos(n_hbonds*(-5.340548)/betti_1) + 6.889499))` |
| 12 | 1.718176e-07 | 0.0045 | `0.020938644 / (sin((n_hbonds / betti_0) * (-5.8387 / euler_characteristic)) + 6.889499)` | `0.020938644/(sin(n_hbonds*(-5.8387)/(betti_0*euler_characteristic)) + 6.889499)` |
| 14 | 1.717778e-07 | 0.0001 | `0.020895302 / (sin(((n_hbonds / betti_0) * -5.8815455) / (euler_characteristic + -0.34945095)) + 6.889499)` | `0.020895302/(sin(n_hbonds*(-5.8815455)/(betti_0*(euler_characteristic - 0.34945095))) + 6.889499)` |
| 15 | 1.716990e-07 | 0.0005 | `0.020567153 / (sin(sin((((n_hbonds * -5.9821663) / euler_characteristic) + -0.23149696) / betti_0)) + 6.8895802)` | `0.020567153/(sin(sin((-0.23149696 + n_hbonds*(-5.9821663)/euler_characteristic)/betti_0)) + 6.8895802)` |
| 17 | 1.710536e-07 | 0.0019 | `0.020831557 / (sin(((n_hbonds / betti_0) * -5.8386993) / (euler_characteristic - cos(2.0616803 * euler_characteristic))) + 6.8894997)` | `0.020831557/(sin(n_hbonds*(-5.8386993)/(betti_0*(euler_characteristic - cos(2.0616803*euler_characteristic)))) + 6.8894997)` |
| 19 | 1.708245e-07 | 0.0007 | `0.020831557 / (sin(((n_hbonds / betti_0) * -5.8386993) / (euler_characteristic - (cos(2.0616803 * euler_characteristic) * 0.5616185))) + 6.8894997)` | `0.020831557/(sin(n_hbonds*(-5.8386993)/(betti_0*(euler_characteristic - 0.5616185*cos(2.0616803*euler_characteristic)))) + 6.8894997)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.18348749/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.170629e-07 | 0.0000 | `0.0028535794` | `0.00285357940000000` |
| 3 | 1.806213e-07 | 0.0919 | `0.18348749 / betti_1` | `0.18348749/betti_1` |
| 4 | 1.806213e-07 | 0.0000 | `sin(0.18348749 / betti_1)` | `sin(0.18348749/betti_1)` |
| 5 | 1.796604e-07 | 0.0053 | `(0.15820615 / betti_1) - -0.0003952684` | `-1*(-0.0003952684) + 0.15820615/betti_1` |
| 6 | 1.790100e-07 | 0.0036 | `0.0032363445 / (log(betti_1) + -3.0277834)` | `0.0032363445/(log(betti_1) - 3.0277834)` |
| 7 | 1.768643e-07 | 0.0121 | `(n_hbonds * (0.0016492336 / betti_1)) - 0.0013280528` | `-1*0.0013280528 + n_hbonds*0.0016492336/betti_1` |
| 9 | 1.767908e-07 | 0.0002 | `(((0.020480923 / betti_1) - -0.00080611964) * n_hbonds) / betti_1` | `n_hbonds*(-1*(-0.00080611964) + 0.020480923/betti_1)/betti_1` |
| 10 | 1.753228e-07 | 0.0083 | `0.0043337042 - ((sin(n_hbonds / euler_characteristic) * 0.17909554) / euler_characteristic)` | `0.0043337042 - 0.17909554*sin(n_hbonds/euler_characteristic)/euler_characteristic` |
| 12 | 1.741725e-07 | 0.0033 | `0.004388292 - (((sin(n_hbonds / betti_1) / euler_characteristic) * -0.0010627937) * n_hbonds)` | `0.004388292 - (-0.0010627937)*n_hbonds*sin(n_hbonds/betti_1)/euler_characteristic` |
| 13 | 1.739459e-07 | 0.0013 | `0.018114474 - ((n_hbonds / euler_characteristic) * (-0.013336689 - ((n_hbonds * 0.0028707911) / euler_characteristic)))` | `0.018114474 - n_hbonds*(-0.013336689 - 0.0028707911*n_hbonds/euler_characteristic)/euler_characteristic` |
| 14 | 1.738893e-07 | 0.0003 | `(sin((n_hbonds * (n_hbonds / betti_1)) * (-0.29146758 / euler_characteristic)) * -0.0029280882) + 0.0055693923` | `0.0055693923 + sin(n_hbonds*n_hbonds*(-0.29146758)/(betti_1*euler_characteristic))*(-0.0029280882)` |
| 15 | 1.729839e-07 | 0.0052 | `0.0034469983 - ((n_hbonds - (betti_1 * 2.806214)) * (0.00013211112 - ((n_hbonds * -6.5617e-5) / euler_characteristic)))` | `0.0034469983 - (0.00013211112 - (-6.5617e-5)*n_hbonds/euler_characteristic)*(-2.806214*betti_1 + n_hbonds)` |
| 16 | 1.729839e-07 | 0.0000 | `sin(0.0034469983 - ((0.00013211112 - (n_hbonds * (-6.5617e-5 / euler_characteristic))) * (n_hbonds - (betti_1 * 2.806214))))` | `sin(0.0034469983 - (0.00013211112 - (-6.5617e-5)*n_hbonds/euler_characteristic)*(-2.806214*betti_1 + n_hbonds))` |
| 17 | 1.725982e-07 | 0.0022 | `(euler_characteristic * ((2.7780666e-6 - (n_hbonds * (-1.2809622e-6 / euler_characteristic))) * (n_hbonds - (betti_1 * 2.6949754)))) + 0.0031415739` | `euler_characteristic*(2.7780666e-6 - (-1.2809622e-6)*n_hbonds/euler_characteristic)*(-2.6949754*betti_1 + n_hbonds) + 0.0031415739` |
| 19 | 1.723715e-07 | 0.0007 | `0.0026431642 - (((-3.1067766e-6 - (n_hbonds * (1.3032618e-6 / euler_characteristic))) * euler_characteristic) * ((n_hbonds - (betti_1 * 2.3769553)) / betti_0))` | `0.0026431642 - euler_characteristic*(-3.1067766e-6 - 1.3032618e-6*n_hbonds/euler_characteristic)*(-2.3769553*betti_1 + n_hbonds)/betti_0` |

</details>

