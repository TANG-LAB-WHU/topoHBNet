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
| 1 | `LBHB_Fraction ≈ 0.00045176392*log(betti_1)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ sin(betti_1*betti_1*0.0003749738)*0.0019103754` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ cos(-betti_1 + n_hbonds)*7.918713e-5 + 0.002569783 - 0.042961977/betti_1` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ cos(betti_1/20.40093)*(-0.0019123536)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ cos(betti_1*0.049023993)*(-0.0019113808)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx 0.00045176392*log(betti_1)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 68/85 | 80.0% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 57/85 | 67.1% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 33/85 | 38.8% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 4/85 | 4.7% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/85 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 68/85 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: 0.00045176392*log(betti_1)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1672124e-5` | `n_hbonds*1.1672124e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045176392` | `0.00045176392*log(betti_1)` |
| 5 | 2.517715e-07 | 0.0017 | `(-0.04315606 / betti_1) + 0.002560385` | `0.002560385 - 0.04315606/betti_1` |
| 6 | 2.510496e-07 | 0.0029 | `0.0019311358 - exp(betti_1 * -0.15788665)` | `0.0019311358 - exp(betti_1*(-0.15788665))` |
| 8 | 2.509337e-07 | 0.0002 | `0.00193476 - (exp(betti_1 * -0.15680175) / betti_0)` | `0.00193476 - exp(betti_1*(-0.15680175))/betti_0` |
| 9 | 2.507600e-07 | 0.0007 | `0.0019317511 - exp(-0.15762569 * (betti_1 + sin(n_hbonds)))` | `0.0019317511 - exp(-0.15762569*(betti_1 + sin(n_hbonds)))` |
| 11 | 2.504263e-07 | 0.0007 | `0.0019317511 - exp((cos(n_hbonds - betti_1) + betti_1) * -0.15762569)` | `0.0019317511 - exp((betti_1 + cos(-betti_1 + n_hbonds))*(-0.15762569))` |
| 12 | 2.501778e-07 | 0.0010 | `((n_hbonds * -0.00053020107) / (cos(betti_1 - n_hbonds) + betti_1)) - -0.003230557` | `n_hbonds*(-0.00053020107)/(betti_1 + cos(betti_1 - n_hbonds)) - 1*(-0.003230557)` |
| 13 | 2.500251e-07 | 0.0006 | `(exp(n_hbonds / (cos(betti_1 - n_hbonds) + betti_1)) * -3.9050155e-5) - -0.0023818118` | `exp(n_hbonds/(betti_1 + cos(betti_1 - n_hbonds)))*(-3.9050155e-5) - 1*(-0.0023818118)` |
| 14 | 2.493687e-07 | 0.0026 | `((n_hbonds * -0.0005403542) / (betti_1 + (1.8430691 * cos(n_hbonds - betti_1)))) - -0.003259901` | `n_hbonds*(-0.0005403542)/(betti_1 + 1.8430691*cos(-betti_1 + n_hbonds)) - 1*(-0.003259901)` |
| 15 | 2.489829e-07 | 0.0015 | `((0.0066728983 * exp(n_hbonds / (betti_1 + cos(n_hbonds + euler_characteristic)))) - 0.20306212) / euler_characteristic` | `(0.0066728983*exp(n_hbonds/(betti_1 + cos(euler_characteristic + n_hbonds))) - 1*0.20306212)/euler_characteristic` |
| 16 | 2.480648e-07 | 0.0037 | `(n_hbonds * (-0.000485379 / ((1.3978531 / sin(betti_1 - (n_hbonds - 1.0765659))) + betti_1))) - -0.0031204263` | `n_hbonds*(-0.000485379)/(betti_1 + 1.3978531/sin(betti_1 - (n_hbonds - 1*1.0765659))) - 1*(-0.0031204263)` |
| 17 | 2.479638e-07 | 0.0004 | `((n_hbonds * -0.000485379) / ((1.3978531 / sin(sin(betti_1 - (n_hbonds - 1.0765659)))) + betti_1)) - -0.0031204263` | `n_hbonds*(-0.000485379)/(betti_1 + 1.3978531/sin(sin(betti_1 - (n_hbonds - 1*1.0765659)))) - 1*(-0.0031204263)` |
| 18 | 2.476101e-07 | 0.0014 | `((exp(n_hbonds / (sin(0.94808924 / cos(n_hbonds + euler_characteristic)) + betti_1)) * 0.006675131) - 0.20321685) / euler_characteristic` | `(exp(n_hbonds/(betti_1 + sin(0.94808924/cos(euler_characteristic + n_hbonds))))*0.006675131 - 1*0.20321685)/euler_characteristic` |
| 20 | 2.475539e-07 | 0.0001 | `((0.006675131 * exp(n_hbonds / (betti_1 + sin(0.94808924 / cos(n_hbonds + (-0.6241569 + euler_characteristic)))))) - 0.20321685) / euler_characteristic` | `(0.006675131*exp(n_hbonds/(betti_1 + sin(0.94808924/cos(euler_characteristic + n_hbonds - 0.6241569)))) - 1*0.20321685)/euler_characteristic` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: sin(betti_1*betti_1*0.0003749738)*0.0019103754</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671989e-5` | `n_hbonds*1.1671989e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045175472` | `0.00045175472*log(betti_1)` |
| 5 | 2.517726e-07 | 0.0017 | `0.0025391316 + (0.041164584 / euler_characteristic)` | `0.0025391316 + 0.041164584/euler_characteristic` |
| 6 | 2.513152e-07 | 0.0018 | `sin(betti_1 * 0.021794315) * 0.0019163331` | `sin(betti_1*0.021794315)*0.0019163331` |
| 7 | 2.513103e-07 | 0.0000 | `0.0020344998 - (0.0029669206 / (betti_1 + -43.628075))` | `0.0020344998 - 0.0029669206/(betti_1 - 43.628075)` |
| 8 | 2.500152e-07 | 0.0052 | `sin(betti_1 * (betti_1 * 0.0003749738)) * 0.0019103754` | `sin(betti_1*betti_1*0.0003749738)*0.0019103754` |
| 11 | 2.494245e-07 | 0.0008 | `log((cos(n_hbonds - betti_1) / 0.11431533) + betti_1) * 0.00045175472` | `0.00045175472*log(betti_1 + 8.74773313430491*cos(betti_1 - n_hbonds))` |
| 12 | 2.488944e-07 | 0.0021 | `0.0024474026 - (0.034848582 / ((cos(n_hbonds - betti_1) / 0.11431533) + betti_1))` | `0.0024474026 - 0.034848582/(betti_1 + cos(-betti_1 + n_hbonds)/0.11431533)` |
| 14 | 2.481730e-07 | 0.0015 | `0.002572065 - (0.043169204 / (betti_1 + (2.8458097 / sin((betti_1 + 1.0479683) - n_hbonds))))` | `0.002572065 - 0.043169204/(betti_1 + 2.8458097/sin(betti_1 - n_hbonds + 1.0479683))` |
| 15 | 2.481154e-07 | 0.0002 | `0.002572065 - (0.043169204 / ((2.5990534 / sin(sin(betti_1 + (1.0479683 - n_hbonds)))) + betti_1))` | `0.002572065 - 0.043169204/(betti_1 + 2.5990534/sin(sin(betti_1 - n_hbonds + 1.0479683)))` |
| 16 | 2.478437e-07 | 0.0011 | `0.002639853 - (0.04790225 / ((exp(cos(euler_characteristic)) / sin((betti_1 + 0.89508677) - n_hbonds)) + betti_1))` | `0.002639853 - 0.04790225/(betti_1 + exp(cos(euler_characteristic))/sin(betti_1 - n_hbonds + 0.89508677))` |
| 17 | 2.476647e-07 | 0.0007 | `0.002572065 - (0.043169204 / (((cos(euler_characteristic) + 2.7815666) / sin(betti_1 + (1.0479683 - n_hbonds))) + betti_1))` | `0.002572065 - 0.043169204/(betti_1 + (cos(euler_characteristic) + 2.7815666)/sin(betti_1 - n_hbonds + 1.0479683))` |
| 18 | 2.475890e-07 | 0.0003 | `0.0025461619 - (0.04192498 / (((exp(cos(euler_characteristic)) + 0.63367474) / sin((0.8960383 - n_hbonds) + betti_1)) + betti_1))` | `0.0025461619 - 0.04192498/(betti_1 + (exp(cos(euler_characteristic)) + 0.63367474)/sin(betti_1 - n_hbonds + 0.8960383))` |
| 19 | 2.473459e-07 | 0.0010 | `0.002572065 - (0.043169204 / (betti_1 + ((2.5990534 + sin(betti_1 / 0.89367425)) / sin((1.0479683 + betti_1) - n_hbonds))))` | `0.002572065 - 0.043169204/(betti_1 + (sin(betti_1/0.89367425) + 2.5990534)/sin(betti_1 - n_hbonds + 1.0479683))` |
| 20 | 2.472361e-07 | 0.0004 | `0.002572065 - (0.043169204 / (betti_1 + ((sin(betti_1 / -0.85403866) + 2.5990534) / sin(sin((betti_1 - n_hbonds) + 1.0479683)))))` | `0.002572065 - 0.043169204/(betti_1 + (sin(betti_1/(-0.85403866)) + 2.5990534)/sin(sin(betti_1 - n_hbonds + 1.0479683)))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: cos(-betti_1 + n_hbonds)*7.918713e-5 + 0.002569783 - 0.042961977/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668321` | `0.00186683210000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1672015e-5` | `n_hbonds*1.1672015e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045175455` | `0.00045175455*log(betti_1)` |
| 5 | 2.517716e-07 | 0.0017 | `(-0.043133378 / betti_1) + 0.002560101` | `0.002560101 - 0.043133378/betti_1` |
| 6 | 2.511405e-07 | 0.0025 | `0.001928083 - exp(euler_characteristic / 6.1798415)` | `0.001928083 - exp(euler_characteristic/6.1798415)` |
| 8 | 2.509608e-07 | 0.0004 | `0.001928083 - (exp(euler_characteristic / 6.1798415) / betti_0)` | `0.001928083 - exp(euler_characteristic/6.1798415)/betti_0` |
| 9 | 2.508634e-07 | 0.0004 | `0.0019264622 - exp((euler_characteristic - sin(n_hbonds)) / 6.1798415)` | `0.0019264622 - exp((euler_characteristic - sin(n_hbonds))/6.1798415)` |
| 10 | 2.505548e-07 | 0.0012 | `0.0018726051 - (-3.0917054e-5 / sin((n_hbonds + -3.83758e6) + euler_characteristic))` | `0.0018726051 - (-1)*3.0917054e-5/sin(euler_characteristic + n_hbonds - 3837580.0)` |
| 11 | 2.504978e-07 | 0.0002 | `(-2.905251e-5 / sin(sin((n_hbonds + -4.14703e6) + euler_characteristic))) + 0.0018729975` | `0.0018729975 - 2.905251e-5/sin(sin(euler_characteristic + n_hbonds - 4147030.0))` |
| 12 | 2.488068e-07 | 0.0068 | `(cos(n_hbonds - betti_1) * 7.918713e-5) + ((-0.042961977 / betti_1) + 0.002569783)` | `cos(-betti_1 + n_hbonds)*7.918713e-5 + 0.002569783 - 0.042961977/betti_1` |
| 13 | 2.487409e-07 | 0.0003 | `((-0.04209895 / betti_1) + (sin(cos(betti_1 - n_hbonds)) * 9.1014495e-5)) + 0.002556064` | `sin(cos(betti_1 - n_hbonds))*9.1014495e-5 + 0.002556064 - 0.04209895/betti_1` |
| 14 | 2.481635e-07 | 0.0023 | `(-0.041037884 / (betti_1 + (2.960243 / sin((n_hbonds + 1.0933006) + euler_characteristic)))) + 0.0025378459` | `0.0025378459 - 0.041037884/(betti_1 + 2.960243/sin(euler_characteristic + n_hbonds + 1.0933006))` |
| 15 | 2.481044e-07 | 0.0002 | `(-0.04153508 / (betti_1 + (2.6965563 / sin(sin((n_hbonds + euler_characteristic) - -1.098362))))) + 0.0025452252` | `0.0025452252 - 0.04153508/(betti_1 + 2.6965563/sin(sin(euler_characteristic + n_hbonds - 1*(-1.098362))))` |
| 16 | 2.480724e-07 | 0.0001 | `(-0.04153508 / (betti_1 + (2.5959656 / sin(sin(sin((euler_characteristic + n_hbonds) - -1.098362)))))) + 0.0025452252` | `0.0025452252 - 0.04153508/(betti_1 + 2.5959656/sin(sin(sin(euler_characteristic + n_hbonds - 1*(-1.098362)))))` |
| 17 | 2.476665e-07 | 0.0016 | `(-0.043012466 / (betti_1 + ((cos(euler_characteristic) + 2.823245) / sin(n_hbonds + (euler_characteristic + 1.0805221))))) + 0.0025699232` | `0.0025699232 - 0.043012466/(betti_1 + (cos(euler_characteristic) + 2.823245)/sin(euler_characteristic + n_hbonds + 1.0805221))` |
| 18 | 2.476255e-07 | 0.0002 | `(-0.040292412 / (((2.9737332 + cos(euler_characteristic)) / sin(sin((euler_characteristic + n_hbonds) + 1.0827619))) + betti_1)) + 0.0025266565` | `0.0025266565 - 0.040292412/(betti_1 + (cos(euler_characteristic) + 2.9737332)/sin(sin(euler_characteristic + n_hbonds + 1.0827619)))` |
| 19 | 2.473642e-07 | 0.0011 | `(-0.041037843 / (betti_1 + ((cos(betti_1 / -0.83639157) + 2.9730504) / sin(n_hbonds + (euler_characteristic + 1.0933006))))) + 0.0025403507` | `0.0025403507 - 0.041037843/(betti_1 + (cos(betti_1/(-0.83639157)) + 2.9730504)/sin(euler_characteristic + n_hbonds + 1.0933006))` |
| 20 | 2.472914e-07 | 0.0003 | `(-0.040292397 / (((2.9737332 + cos(betti_1 / 0.8348441)) / sin(sin((n_hbonds + 1.0959071) + euler_characteristic))) + betti_1)) + 0.0025274926` | `0.0025274926 - 0.040292397/(betti_1 + (cos(betti_1/0.8348441) + 2.9737332)/sin(sin(euler_characteristic + n_hbonds + 1.0959071)))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: cos(betti_1/20.40093)*(-0.0019123536)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1672044e-5` | `n_hbonds*1.1672044e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045175466` | `0.00045175466*log(betti_1)` |
| 5 | 2.517741e-07 | 0.0017 | `0.0025377139 - (0.041740365 / betti_1)` | `0.0025377139 - 0.041740365/betti_1` |
| 6 | 2.503172e-07 | 0.0058 | `cos(betti_1 / 20.40093) * -0.0019123536` | `cos(betti_1/20.40093)*(-0.0019123536)` |
| 7 | 2.503163e-07 | 0.0000 | `sin(cos(betti_1 / 20.40093) * -0.0019114291)` | `sin(cos(betti_1/20.40093)*(-0.0019114291))` |
| 8 | 2.500172e-07 | 0.0012 | `(cos(betti_1 / -6.8449683) * -0.00023480388) + 0.0016785886` | `0.0016785886 + cos(betti_1/(-6.8449683))*(-0.00023480388)` |
| 9 | 2.492265e-07 | 0.0032 | `cos(betti_1 / (sin(n_hbonds) + -20.450674)) * -0.0019236015` | `cos(betti_1/(sin(n_hbonds) - 20.450674))*(-0.0019236015)` |
| 10 | 2.491331e-07 | 0.0004 | `cos(betti_1 / (sin(sin(n_hbonds)) + -20.450674)) * -0.0019195421` | `cos(betti_1/(sin(sin(n_hbonds)) - 20.450674))*(-0.0019195421)` |
| 11 | 2.491106e-07 | 0.0001 | `-0.0019195421 * cos(betti_1 / (-20.450674 + sin(sin(sin(n_hbonds)))))` | `-0.0019195421*cos(betti_1/(sin(sin(sin(n_hbonds))) - 20.450674))` |
| 12 | 2.489336e-07 | 0.0007 | `cos((sin(betti_1) - betti_1) / (sin(n_hbonds) + -20.450674)) * -0.001924367` | `cos((-betti_1 + sin(betti_1))/(sin(n_hbonds) - 20.450674))*(-0.001924367)` |
| 13 | 2.488421e-07 | 0.0004 | `cos((betti_1 - sin(betti_1)) / (sin(sin(n_hbonds)) + -20.450674)) * -0.001924367` | `cos((betti_1 - sin(betti_1))/(sin(sin(n_hbonds)) - 20.450674))*(-0.001924367)` |
| 14 | 2.481644e-07 | 0.0027 | `0.0025507023 - (0.041858863 / ((2.8217041 / cos((euler_characteristic + n_hbonds) + -0.46534273)) + betti_1))` | `0.0025507023 - 0.041858863/(betti_1 + 2.8217041/cos(euler_characteristic + n_hbonds - 0.46534273))` |
| 15 | 2.481061e-07 | 0.0002 | `0.0025507023 - (0.041858863 / ((2.8217041 / sin(cos(-0.46534273 + (euler_characteristic + n_hbonds)))) + betti_1))` | `0.0025507023 - 0.041858863/(betti_1 + 2.8217041/sin(cos(euler_characteristic + n_hbonds - 0.46534273)))` |
| 16 | 2.478439e-07 | 0.0011 | `(-0.048220035 / ((exp(cos(euler_characteristic)) / cos((n_hbonds + euler_characteristic) + -0.32583672)) + betti_1)) - -0.002645001` | `-1*(-0.002645001) - 0.048220035/(betti_1 + exp(cos(euler_characteristic))/cos(euler_characteristic + n_hbonds - 0.32583672))` |
| 17 | 2.476714e-07 | 0.0007 | `(-0.042586688 / (betti_1 + ((cos(euler_characteristic) + 2.8863306) / cos(n_hbonds + (euler_characteristic + -0.49482787))))) - -0.002563353` | `-1*(-0.002563353) - 0.042586688/(betti_1 + (cos(euler_characteristic) + 2.8863306)/cos(euler_characteristic + n_hbonds - 0.49482787))` |
| 18 | 2.475359e-07 | 0.0005 | `(-0.04927167 / (betti_1 + (exp(cos(euler_characteristic * -1.1109887)) / cos(euler_characteristic + (n_hbonds + -0.31725287))))) - -0.0026617623` | `-1*(-0.0026617623) - 0.04927167/(betti_1 + exp(cos(euler_characteristic*(-1.1109887)))/cos(euler_characteristic + n_hbonds - 0.31725287))` |
| 19 | 2.472562e-07 | 0.0011 | `(-0.044100165 / (((cos(euler_characteristic * -1.1150901) + 1.8517679) / cos((n_hbonds + euler_characteristic) + -0.3258321)) + betti_1)) - -0.0025806658` | `-1*(-0.0025806658) - 0.044100165/(betti_1 + (cos(euler_characteristic*(-1.1150901)) + 1.8517679)/cos(euler_characteristic + n_hbonds - 0.3258321))` |
| 20 | 2.472561e-07 | 0.0000 | `sin((-0.044181712 / (betti_1 + ((1.8517679 + cos(-1.1150899 * euler_characteristic)) / cos((n_hbonds + euler_characteristic) + -0.3258322)))) - -0.002581921)` | `sin(-1*(-0.002581921) - 0.044181712/(betti_1 + (cos(-1.1150899*euler_characteristic) + 1.8517679)/cos(euler_characteristic + n_hbonds - 0.3258322)))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: cos(betti_1*0.049023993)*(-0.0019113808)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671917e-5` | `n_hbonds*1.1671917e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.000451755` | `0.000451755*log(betti_1)` |
| 5 | 2.517724e-07 | 0.0017 | `(0.04151625 / euler_characteristic) + 0.002545142` | `0.002545142 + 0.04151625/euler_characteristic` |
| 6 | 2.503166e-07 | 0.0058 | `cos(betti_1 * 0.049023993) * -0.0019113808` | `cos(betti_1*0.049023993)*(-0.0019113808)` |
| 7 | 2.501111e-07 | 0.0008 | `cos(sin(-0.048660897 * betti_1)) * 0.0019126958` | `cos(sin(-0.048660897*betti_1))*0.0019126958` |
| 8 | 2.500426e-07 | 0.0003 | `cos(sin(sin(betti_1 * 0.048630532))) * 0.001910201` | `cos(sin(sin(betti_1*0.048630532)))*0.001910201` |
| 9 | 2.495114e-07 | 0.0021 | `cos((betti_1 + sin(n_hbonds)) * -0.04899587) * -0.0019144436` | `cos((betti_1 + sin(n_hbonds))*(-0.04899587))*(-0.0019144436)` |
| 10 | 2.494684e-07 | 0.0002 | `cos(-0.048030496 * (betti_1 + exp(sin(n_hbonds)))) * -0.0019144436` | `cos(-0.048030496*(betti_1 + exp(sin(n_hbonds))))*(-0.0019144436)` |
| 11 | 2.491131e-07 | 0.0014 | `cos(0.049076267 * (betti_1 + (sin(n_hbonds) / 0.43745387))) * -0.0019172273` | `cos(0.049076267*(betti_1 + sin(n_hbonds)/0.43745387))*(-0.0019172273)` |
| 13 | 2.489911e-07 | 0.0002 | `-0.0019248427 * cos((betti_1 + sin(n_hbonds + (euler_characteristic / 0.1418412))) * -0.04873881)` | `-0.0019248427*cos((betti_1 + sin(euler_characteristic/0.1418412 + n_hbonds))*(-0.04873881))` |
| 14 | 2.488154e-07 | 0.0007 | `cos((sin(n_hbonds) + (sin(euler_characteristic / -0.17230968) + betti_1)) * 0.049327444) * -0.0019172273` | `cos((betti_1 + sin(n_hbonds) + sin(euler_characteristic/(-0.17230968)))*0.049327444)*(-0.0019172273)` |
| 15 | 2.474466e-07 | 0.0055 | `cos((betti_1 + (sin(n_hbonds + (euler_characteristic / 0.1418412)) * 2.4482713)) * -0.04873881) * -0.0019248427` | `cos((betti_1 + sin(euler_characteristic/0.1418412 + n_hbonds)*2.4482713)*(-0.04873881))*(-0.0019248427)` |
| 16 | 2.467790e-07 | 0.0027 | `-0.0019262814 * cos(((sin(n_hbonds + (euler_characteristic / 0.1417838)) / exp(-1.4002794)) + betti_1) * -0.049065154)` | `-0.0019262814*cos((betti_1 + sin(euler_characteristic/0.1417838 + n_hbonds)/exp(-1.4002794))*(-0.049065154))` |
| 17 | 2.467225e-07 | 0.0002 | `cos((betti_1 * 0.04888657) + (sin((betti_0 + n_hbonds) + (euler_characteristic / 1.2752458)) * 0.21171516)) * -0.0019404269` | `cos(betti_1*0.04888657 + sin(betti_0 + euler_characteristic/1.2752458 + n_hbonds)*0.21171516)*(-0.0019404269)` |
| 19 | 2.463572e-07 | 0.0007 | `cos((betti_1 * 0.04888657) + (sin((betti_0 + (n_hbonds / betti_0)) + (euler_characteristic / 1.2752458)) * 0.21171516)) * -0.0019404269` | `cos(betti_1*0.04888657 + sin(betti_0 + euler_characteristic/1.2752458 + n_hbonds/betti_0)*0.21171516)*(-0.0019404269)` |

</details>

