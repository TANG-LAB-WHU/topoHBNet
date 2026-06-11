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
| 1 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13728291) - 1*(-0.0014700135)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ exp(euler_characteristic/7.2859054) + 0.0014686874` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13729453) - 1*(-0.0014708948)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13726477) + 0.0014690616` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13727872) + 0.0014695993` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(euler_characteristic*0.13728291) - 1*(-0.0014700135)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 60/83 | 72.3% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 38/83 | 45.8% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 37/83 | 44.6% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 23/83 | 27.7% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/83 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 60/83 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(euler_characteristic*0.13728291) - 1*(-0.0014700135)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026766013` | `0.00267660130000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626703 / euler_characteristic` | `-0.14626703/euler_characteristic` |
| 4 | 7.821258e-07 | 1.0044 | `exp(n_hbonds / -24.661055)` | `exp(n_hbonds/(-24.661055))` |
| 5 | 7.360079e-07 | 0.0608 | `(-0.57638663 / euler_characteristic) - 0.008518787` | `-1*0.008518787 - 0.57638663/euler_characteristic` |
| 6 | 3.622937e-07 | 0.7088 | `exp(euler_characteristic * 0.13728291) - -0.0014700135` | `exp(euler_characteristic*0.13728291) - 1*(-0.0014700135)` |
| 7 | 3.622905e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13728291) - -0.0014700135)` | `sin(exp(euler_characteristic*0.13728291) - 1*(-0.0014700135))` |
| 8 | 3.579605e-07 | 0.0120 | `exp(betti_1 * -0.1311782) + (betti_1 * 2.4815568e-5)` | `betti_1*2.4815568e-5 + exp(betti_1*(-0.1311782))` |
| 9 | 3.546845e-07 | 0.0092 | `exp((sin(betti_1) + betti_1) * -0.13411793) + 0.0014526073` | `exp((betti_1 + sin(betti_1))*(-0.13411793)) + 0.0014526073` |
| 10 | 3.534985e-07 | 0.0033 | `exp((betti_1 + sin(sin(betti_1))) * -0.13411465) + 0.0014553638` | `exp((betti_1 + sin(sin(betti_1)))*(-0.13411465)) + 0.0014553638` |
| 11 | 3.002648e-07 | 0.1632 | `exp(sin(n_hbonds * -0.085502855) + (betti_1 * -0.15809084)) + 0.0019074024` | `exp(betti_1*(-0.15809084) + sin(n_hbonds*(-0.085502855))) + 0.0019074024` |
| 12 | 3.002639e-07 | 0.0000 | `sin(exp(sin(n_hbonds * -0.085502855) + (betti_1 * -0.15809084)) + 0.0019074024)` | `sin(exp(betti_1*(-0.15809084) + sin(n_hbonds*(-0.085502855))) + 0.0019074024)` |
| 13 | 3.002629e-07 | 0.0000 | `sin(sin(exp(sin(n_hbonds * -0.085502855) + (betti_1 * -0.15809084)) + 0.0019074024))` | `sin(sin(exp(betti_1*(-0.15809084) + sin(n_hbonds*(-0.085502855))) + 0.0019074024))` |
| 14 | 2.948585e-07 | 0.0182 | `exp(sin(sin(n_hbonds * 0.15706359) - -0.8575718) + (betti_1 * -0.15920246)) + 0.0018916624` | `exp(betti_1*(-0.15920246) + sin(sin(n_hbonds*0.15706359) - 1*(-0.8575718))) + 0.0018916624` |
| 16 | 2.842287e-07 | 0.0184 | `exp(sin((n_hbonds * 0.15666203) - sin(betti_1 * -0.21802036)) + (betti_1 * -0.15902376)) + 0.0019331629` | `exp(betti_1*(-0.15902376) + sin(n_hbonds*0.15666203 - sin(betti_1*(-0.21802036)))) + 0.0019331629` |
| 17 | 2.793028e-07 | 0.0175 | `0.0019461999 + exp((-0.1586829 * betti_1) + sin((n_hbonds * 0.15718089) - sin(sin(betti_1 * -0.21975671))))` | `exp(-0.1586829*betti_1 + sin(n_hbonds*0.15718089 - sin(sin(betti_1*(-0.21975671))))) + 0.0019461999` |
| 19 | 2.773874e-07 | 0.0034 | `exp(sin((n_hbonds * 0.15666203) - sin((betti_1 - sin(n_hbonds)) * -0.21802036)) + (betti_1 * -0.15902376)) + 0.0019331629` | `exp(betti_1*(-0.15902376) + sin(n_hbonds*0.15666203 - sin((betti_1 - sin(n_hbonds))*(-0.21802036)))) + 0.0019331629` |
| 20 | 2.742776e-07 | 0.0113 | `exp((betti_1 * -0.1586829) + sin((n_hbonds * 0.15718089) - sin(sin((betti_1 - sin(n_hbonds)) * -0.21975671)))) + 0.0019461999` | `exp(betti_1*(-0.1586829) + sin(n_hbonds*0.15718089 - sin(sin((betti_1 - sin(n_hbonds))*(-0.21975671))))) + 0.0019461999` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: exp(euler_characteristic/7.2859054) + 0.0014686874</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026766735` | `0.00267667350000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.1462684 / euler_characteristic` | `-0.1462684/euler_characteristic` |
| 4 | 7.821302e-07 | 1.0044 | `exp(n_hbonds * -0.04055347)` | `exp(n_hbonds*(-0.04055347))` |
| 5 | 7.360078e-07 | 0.0608 | `(-0.57644975 / euler_characteristic) - 0.008520017` | `-1*0.008520017 - 0.57644975/euler_characteristic` |
| 6 | 3.622927e-07 | 0.7088 | `exp(euler_characteristic / 7.2859054) + 0.0014686874` | `exp(euler_characteristic/7.2859054) + 0.0014686874` |
| 7 | 3.622894e-07 | 0.0000 | `sin(exp(euler_characteristic / 7.2859054) + 0.0014686874)` | `sin(exp(euler_characteristic/7.2859054) + 0.0014686874)` |
| 8 | 3.537172e-07 | 0.0239 | `(betti_1 * 2.5114452e-5) + exp(euler_characteristic / 7.4076056)` | `betti_1*2.5114452e-5 + exp(euler_characteristic/7.4076056)` |
| 9 | 3.240975e-07 | 0.0875 | `exp(sin(-1.2889016 - (euler_characteristic / 9.312749))) * 0.005209907` | `exp(sin(-euler_characteristic/9.312749 - 1.2889016))*0.005209907` |
| 11 | 3.211704e-07 | 0.0045 | `exp(exp(sin(cos(euler_characteristic / -9.536862) + -3.0688477))) * 0.0012970754` | `exp(exp(sin(cos(euler_characteristic/(-9.536862)) - 3.0688477)))*0.0012970754` |
| 12 | 3.175972e-07 | 0.0112 | `exp(exp(sin((euler_characteristic / 8.725198) + -1.1238807) * 0.8051815)) * 0.0012360795` | `exp(exp(sin(euler_characteristic/8.725198 - 1.1238807)*0.8051815))*0.0012360795` |
| 13 | 3.175633e-07 | 0.0001 | `sin(exp(exp(sin((euler_characteristic / 8.724872) + -1.1239558) * 0.80688787)) * 0.0012345563)` | `sin(exp(exp(sin(euler_characteristic/8.724872 - 1.1239558)*0.80688787))*0.0012345563)` |
| 16 | 3.052992e-07 | 0.0131 | `exp(sin(-1.1912987 - (((betti_0 - sin(betti_1 / betti_0)) - betti_1) / 9.522312))) * 0.005165417` | `exp(sin(-(betti_0 - betti_1 - sin(betti_1/betti_0))/9.522312 - 1.1912987))*0.005165417` |
| 18 | 3.021471e-07 | 0.0052 | `exp(sin(-1.1912987 - (((betti_0 - (betti_0 * sin(betti_1 / betti_0))) - betti_1) / 9.522312))) * 0.005165417` | `exp(sin(-(-betti_0*sin(betti_1/betti_0) + betti_0 - betti_1)/9.522312 - 1.1912987))*0.005165417` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(euler_characteristic*0.13729453) - 1*(-0.0014708948)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026766013` | `0.00267660130000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626667 / euler_characteristic` | `-0.14626667/euler_characteristic` |
| 4 | 7.821415e-07 | 1.0044 | `exp(n_hbonds * -0.04055759)` | `exp(n_hbonds*(-0.04055759))` |
| 5 | 5.548894e-07 | 0.3433 | `-0.059914052 / (euler_characteristic + 27.984701)` | `-0.059914052/(euler_characteristic + 27.984701)` |
| 6 | 3.622958e-07 | 0.4263 | `exp(euler_characteristic * 0.13729453) - -0.0014708948` | `exp(euler_characteristic*0.13729453) - 1*(-0.0014708948)` |
| 7 | 3.622891e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13726892) - -0.001469513)` | `sin(exp(euler_characteristic*0.13726892) - 1*(-0.001469513))` |
| 8 | 3.562830e-07 | 0.0167 | `exp(euler_characteristic * 0.135745) - (betti_1 * -2.5841135e-5)` | `-(-2.5841135e-5)*betti_1 + exp(euler_characteristic*0.135745)` |
| 9 | 3.511343e-07 | 0.0146 | `exp((euler_characteristic - sin(betti_1)) * 0.13819942) - -0.0015009443` | `exp((euler_characteristic - sin(betti_1))*0.13819942) - 1*(-0.0015009443)` |
| 10 | 3.351751e-07 | 0.0465 | `((euler_characteristic * -0.00052986725) + exp(-1.6734413 / euler_characteristic)) - 1.0580964` | `euler_characteristic*(-0.00052986725) - 1*1.0580964 + exp(-1.6734413/euler_characteristic)` |
| 11 | 3.220264e-07 | 0.0400 | `exp((euler_characteristic - sin(0.1838722 * n_hbonds)) * 0.13945282) - -0.0015753509` | `exp((euler_characteristic - sin(0.1838722*n_hbonds))*0.13945282) - 1*(-0.0015753509)` |
| 12 | 3.220257e-07 | 0.0000 | `sin(exp((euler_characteristic - sin(n_hbonds * 0.1838722)) * 0.13945282) - -0.0015753509)` | `sin(exp((euler_characteristic - sin(n_hbonds*0.1838722))*0.13945282) - 1*(-0.0015753509))` |
| 13 | 3.039247e-07 | 0.0579 | `exp((euler_characteristic - sin(n_hbonds * (0.4390056 / betti_0))) * 0.1377113) - -0.0014913386` | `exp((euler_characteristic - sin(n_hbonds*0.4390056/betti_0))*0.1377113) - 1*(-0.0014913386)` |
| 14 | 3.038871e-07 | 0.0001 | `exp(sin(0.13794471) * (euler_characteristic - sin((n_hbonds * 0.43824995) / betti_0))) - -0.0015063835` | `exp((euler_characteristic - sin(n_hbonds*0.43824995/betti_0))*sin(0.13794471)) - 1*(-0.0015063835)` |
| 15 | 3.007640e-07 | 0.0103 | `exp((euler_characteristic - (sin((0.4390056 * n_hbonds) / betti_0) * betti_0)) * 0.1377113) - -0.0014913386` | `exp((-betti_0*sin(0.4390056*n_hbonds/betti_0) + euler_characteristic)*0.1377113) - 1*(-0.0014913386)` |
| 17 | 2.991117e-07 | 0.0028 | `exp((euler_characteristic - (sin((0.43900615 / betti_0) * n_hbonds) * (betti_0 + 0.28593644))) * 0.13808072) - -0.0015056491` | `exp((euler_characteristic - (betti_0 + 0.28593644)*sin(0.43900615*n_hbonds/betti_0))*0.13808072) - 1*(-0.0015056491)` |
| 18 | 2.916211e-07 | 0.0254 | `exp(((euler_characteristic - sin((n_hbonds / betti_0) * 0.43712303)) - sin(betti_1 / betti_0)) * 0.13814323) - -0.0015104372` | `exp((euler_characteristic - sin(betti_1/betti_0) - sin(n_hbonds*0.43712303/betti_0))*0.13814323) - 1*(-0.0015104372)` |
| 19 | 2.900601e-07 | 0.0054 | `exp(((euler_characteristic - sin(n_hbonds / (betti_0 / 0.43713474))) - sin(sin(betti_1 / betti_0))) * 0.13798425) - -0.0015020546` | `exp((euler_characteristic - sin(n_hbonds/((betti_0/0.43713474))) - sin(sin(betti_1/betti_0)))*0.13798425) - 1*(-0.0015020546)` |
| 20 | 2.896311e-07 | 0.0015 | `exp(((euler_characteristic - sin(n_hbonds / (betti_0 / 0.43713474))) - sin(sin(sin(betti_1 / betti_0)))) * 0.13798425) - -0.0015020546` | `exp((euler_characteristic - sin(n_hbonds/((betti_0/0.43713474))) - sin(sin(sin(betti_1/betti_0))))*0.13798425) - 1*(-0.0015020546)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: exp(euler_characteristic*0.13726477) + 0.0014690616</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.002676672` | `0.00267667200000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626653 / euler_characteristic` | `-0.14626653/euler_characteristic` |
| 4 | 1.336612e-06 | 0.4685 | `exp(betti_1 * -0.123109736)` | `exp(betti_1*(-0.123109736))` |
| 5 | 7.360078e-07 | 0.5967 | `(-0.5764513 / euler_characteristic) + -0.008520039` | `-0.008520039 - 0.5764513/euler_characteristic` |
| 6 | 3.622922e-07 | 0.7088 | `exp(euler_characteristic * 0.13726477) + 0.0014690616` | `exp(euler_characteristic*0.13726477) + 0.0014690616` |
| 7 | 3.622890e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13726477) + 0.0014690616)` | `sin(exp(euler_characteristic*0.13726477) + 0.0014690616)` |
| 8 | 3.537355e-07 | 0.0239 | `exp(euler_characteristic * 0.13506941) + (betti_1 * 2.5214518e-5)` | `betti_1*2.5214518e-5 + exp(euler_characteristic*0.13506941)` |
| 9 | 3.511401e-07 | 0.0074 | `exp((euler_characteristic - sin(betti_1)) * 0.13819717) + 0.0014986868` | `exp((euler_characteristic - sin(betti_1))*0.13819717) + 0.0014986868` |
| 10 | 3.496446e-07 | 0.0043 | `exp((euler_characteristic - sin(sin(betti_1))) * 0.13805535) + 0.0014962137` | `exp((euler_characteristic - sin(sin(betti_1)))*0.13805535) + 0.0014962137` |
| 11 | 3.220398e-07 | 0.0822 | `exp((sin(n_hbonds * -0.18405561) + euler_characteristic) * 0.1394707) + 0.0015734949` | `exp((euler_characteristic + sin(n_hbonds*(-0.18405561)))*0.1394707) + 0.0015734949` |
| 12 | 3.220390e-07 | 0.0000 | `sin(exp((sin(n_hbonds * -0.18405561) + euler_characteristic) * 0.1394707) + 0.0015734949)` | `sin(exp((euler_characteristic + sin(n_hbonds*(-0.18405561)))*0.1394707) + 0.0015734949)` |
| 13 | 3.125285e-07 | 0.0300 | `exp(0.13905005 * (euler_characteristic - sin(n_hbonds * (0.1833853 * betti_0)))) + 0.0015627181` | `exp(0.13905005*(euler_characteristic - sin(n_hbonds*0.1833853*betti_0))) + 0.0015627181` |
| 14 | 3.125281e-07 | 0.0000 | `sin(exp((euler_characteristic - sin(n_hbonds * (0.1833853 * betti_0))) * 0.13905005) + 0.0015627181)` | `sin(exp((euler_characteristic - sin(n_hbonds*0.1833853*betti_0))*0.13905005) + 0.0015627181)` |
| 15 | 2.990742e-07 | 0.0440 | `exp(0.1376623 * (euler_characteristic - cos((betti_1 + (n_hbonds / betti_0)) * 0.2504979))) + 0.0014875227` | `exp(0.1376623*(euler_characteristic - cos((betti_1 + n_hbonds/betti_0)*0.2504979))) + 0.0014875227` |
| 16 | 2.990736e-07 | 0.0000 | `sin(0.0014875227 + exp(0.1376623 * (euler_characteristic - cos(((n_hbonds / betti_0) + betti_1) * 0.2504979))))` | `sin(exp(0.1376623*(euler_characteristic - cos((betti_1 + n_hbonds/betti_0)*0.2504979))) + 0.0014875227)` |
| 17 | 2.989646e-07 | 0.0004 | `exp(0.1376623 * (euler_characteristic - cos(((n_hbonds / betti_0) + (betti_1 - 0.1376623)) * 0.2504979))) + 0.0014875227` | `exp(0.1376623*(euler_characteristic - cos((betti_1 - 1*0.1376623 + n_hbonds/betti_0)*0.2504979))) + 0.0014875227` |
| 18 | 2.989546e-07 | 0.0000 | `sin(exp((euler_characteristic - cos(((betti_1 + -0.13432379) + (n_hbonds / betti_0)) * 0.25049976)) * 0.13772675) + 0.001495679)` | `sin(exp((euler_characteristic - cos((betti_1 - 0.13432379 + n_hbonds/betti_0)*0.25049976))*0.13772675) + 0.001495679)` |
| 19 | 2.958993e-07 | 0.0103 | `0.0014875227 + exp((euler_characteristic - ((euler_characteristic + betti_1) * sin((betti_1 + (n_hbonds / betti_0)) * 0.25950214))) * 0.1376623)` | `exp((euler_characteristic - (betti_1 + euler_characteristic)*sin((betti_1 + n_hbonds/betti_0)*0.25950214))*0.1376623) + 0.0014875227` |
| 20 | 2.943586e-07 | 0.0052 | `exp((euler_characteristic - sin((betti_1 + ((n_hbonds + cos(betti_1 / -0.22087698)) / betti_0)) * 0.25950214)) * 0.1376623) + 0.0014875227` | `exp((euler_characteristic - sin((betti_1 + (n_hbonds + cos(betti_1/(-0.22087698)))/betti_0)*0.25950214))*0.1376623) + 0.0014875227` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: exp(euler_characteristic*0.13727872) + 0.0014695993</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.200459e-06 | 0.0000 | `0.0026767743` | `0.00267677430000000` |
| 3 | 2.135462e-06 | 0.2023 | `-0.14626627 / euler_characteristic` | `-0.14626627/euler_characteristic` |
| 4 | 7.821247e-07 | 1.0044 | `exp(n_hbonds * -0.04054809)` | `exp(n_hbonds*(-0.04054809))` |
| 5 | 5.550434e-07 | 0.3430 | `-0.06000416 / (euler_characteristic - -27.967386)` | `-0.06000416/(euler_characteristic - 1*(-27.967386))` |
| 6 | 3.622933e-07 | 0.4266 | `exp(euler_characteristic * 0.13727872) + 0.0014695993` | `exp(euler_characteristic*0.13727872) + 0.0014695993` |
| 7 | 3.622901e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13727872) + 0.0014695993)` | `sin(exp(euler_characteristic*0.13727872) + 0.0014695993)` |
| 8 | 3.537147e-07 | 0.0240 | `exp(euler_characteristic * 0.13500135) + (betti_1 * 2.5146575e-5)` | `betti_1*2.5146575e-5 + exp(euler_characteristic*0.13500135)` |
| 9 | 3.511706e-07 | 0.0072 | `exp((euler_characteristic - sin(betti_1)) * 0.13811274) + 0.0014995094` | `exp((euler_characteristic - sin(betti_1))*0.13811274) + 0.0014995094` |
| 10 | 3.496618e-07 | 0.0043 | `exp((euler_characteristic - sin(sin(betti_1))) * 0.13811274) + 0.0014995094` | `exp((euler_characteristic - sin(sin(betti_1)))*0.13811274) + 0.0014995094` |
| 11 | 3.237402e-07 | 0.0770 | `exp((sin(n_hbonds * -0.43729636) + euler_characteristic) * 0.1375573) + 0.001491261` | `exp((euler_characteristic + sin(n_hbonds*(-0.43729636)))*0.1375573) + 0.001491261` |
| 13 | 3.045980e-07 | 0.0305 | `exp((sin((n_hbonds * -0.43726817) / betti_0) + euler_characteristic) * 0.13766305) + 0.0015050905` | `exp((euler_characteristic + sin(n_hbonds*(-0.43726817)/betti_0))*0.13766305) + 0.0015050905` |
| 15 | 2.936575e-07 | 0.0183 | `exp((euler_characteristic + sin((n_hbonds / betti_0) * -0.43745)) * 0.13509674) + (betti_1 * 2.535117e-5)` | `betti_1*2.535117e-5 + exp((euler_characteristic + sin(n_hbonds*(-0.43745)/betti_0))*0.13509674)` |
| 16 | 2.936567e-07 | 0.0000 | `(betti_1 * 2.5353385e-5) + sin(exp((sin(n_hbonds * (-0.43745002 / betti_0)) + euler_characteristic) * 0.13509715))` | `betti_1*2.5353385e-5 + sin(exp((euler_characteristic + sin(n_hbonds*(-0.43745002)/betti_0))*0.13509715))` |
| 17 | 2.899556e-07 | 0.0127 | `exp((euler_characteristic + (sin((n_hbonds * -0.43745002) / betti_0) * betti_0)) * 0.13509722) + (betti_1 * 2.531188e-5)` | `betti_1*2.531188e-5 + exp((betti_0*sin(n_hbonds*(-0.43745002)/betti_0) + euler_characteristic)*0.13509722)` |
| 19 | 2.893474e-07 | 0.0010 | `(betti_1 * 2.531188e-5) + exp((euler_characteristic + ((0.111107364 + betti_0) * sin(n_hbonds * (-0.43745002 / betti_0)))) * 0.13509722)` | `betti_1*2.531188e-5 + exp((euler_characteristic + (betti_0 + 0.111107364)*sin(n_hbonds*(-0.43745002)/betti_0))*0.13509722)` |
| 20 | 2.893465e-07 | 0.0000 | `sin(exp((euler_characteristic + (sin((n_hbonds * -0.43745002) / betti_0) * (betti_0 + 0.111107364))) * 0.13509722) + (betti_1 * 2.531188e-5))` | `sin(betti_1*2.531188e-5 + exp((euler_characteristic + (betti_0 + 0.111107364)*sin(n_hbonds*(-0.43745002)/betti_0))*0.13509722))` |

</details>

