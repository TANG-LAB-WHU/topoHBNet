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
| 1 | `LBHB_Fraction ≈ -0.13601975/euler_characteristic` | 4/5 | 80.0% |
| 2 | `LBHB_Fraction ≈ -0.13602005/euler_characteristic` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx -0.13601975/euler_characteristic$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 39/67 | 58.2% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 33/67 | 49.3% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 13/67 | 19.4% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 0/67 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/67 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 39/67 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: -0.13601975/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.934652e-07 | 0.0000 | `0.0021896516` | `0.00218965160000000` |
| 3 | 1.373526e-07 | 0.1713 | `-0.13601975 / euler_characteristic` | `-0.13601975/euler_characteristic` |
| 5 | 1.363518e-07 | 0.0037 | `-0.12119922 / (7.6104045 - betti_1)` | `-0.12119922/(7.6104045 - betti_1)` |
| 7 | 1.351219e-07 | 0.0045 | `-0.13639224 / (euler_characteristic + cos(exp(betti_1)))` | `-0.13639224/(euler_characteristic + cos(exp(betti_1)))` |
| 8 | 1.301977e-07 | 0.0371 | `-0.13676941 / (euler_characteristic + sin(0.3333965 * euler_characteristic))` | `-0.13676941/(euler_characteristic + sin(0.3333965*euler_characteristic))` |
| 9 | 1.292059e-07 | 0.0076 | `-0.13629916 / (exp(cos(0.35290146 * betti_1)) - betti_1)` | `-0.13629916/(-betti_1 + exp(cos(0.35290146*betti_1)))` |
| 10 | 1.115676e-07 | 0.1468 | `-0.13011545 / (exp(exp(sin(betti_1 / -3.0740614))) - betti_1)` | `-0.13011545/(-betti_1 + exp(exp(sin(betti_1/(-3.0740614)))))` |
| 11 | 1.089002e-07 | 0.0242 | `-0.1265224 / (exp(sin(betti_1 / -3.0736718) + 1.6930145) - betti_1)` | `-0.1265224/(-betti_1 + exp(sin(betti_1/(-3.0736718)) + 1.6930145))` |
| 13 | 1.088147e-07 | 0.0004 | `-0.12414485 / ((exp(sin(betti_1 / -3.0714922) + 1.6932725) + 1.0247481) - betti_1)` | `-0.12414485/(-betti_1 + exp(sin(betti_1/(-3.0714922)) + 1.6932725) + 1.0247481)` |
| 14 | 1.084009e-07 | 0.0038 | `-0.12647606 / ((exp(sin(betti_1 / -3.0714445) + 1.6933341) - betti_1) - sin(n_hbonds))` | `-0.12647606/(-betti_1 + exp(sin(betti_1/(-3.0714445)) + 1.6933341) - sin(n_hbonds))` |
| 15 | 1.083548e-07 | 0.0004 | `-0.12647606 / ((exp(sin(betti_1 / -3.0714445) + 1.6933341) - betti_1) - sin(sin(n_hbonds)))` | `-0.12647606/(-betti_1 + exp(sin(betti_1/(-3.0714445)) + 1.6933341) - sin(sin(n_hbonds)))` |
| 16 | 1.066723e-07 | 0.0156 | `-0.12631531 / (exp(sin(betti_1 / -3.0714445) + 1.6933043) - (betti_1 + sin(betti_1 * -0.5909723)))` | `-0.12631531/(-(betti_1 + sin(betti_1*(-0.5909723))) + exp(sin(betti_1/(-3.0714445)) + 1.6933043))` |
| 18 | 1.060964e-07 | 0.0027 | `-0.12631531 / (((cos(betti_1 / 1.6153673) * -2.204965) - betti_1) + exp(sin(betti_1 / -3.0714445) + 1.6933043))` | `-0.12631531/(-betti_1 + exp(sin(betti_1/(-3.0714445)) + 1.6933043) + cos(betti_1/1.6153673)*(-2.204965))` |
| 20 | 1.059690e-07 | 0.0006 | `-0.12631531 / ((exp(1.6933043 + sin(betti_1 / -3.0714445)) - betti_1) + (-1.9707433 * cos(-0.5817575 - (betti_1 / 1.6401267))))` | `-0.12631531/(-betti_1 + exp(sin(betti_1/(-3.0714445)) + 1.6933043) - 1.9707433*cos(-betti_1/1.6401267 - 0.5817575))` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: -0.13601975/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.934652e-07 | 0.0000 | `0.0021896518` | `0.00218965180000000` |
| 3 | 1.373526e-07 | 0.1713 | `-0.13601975 / euler_characteristic` | `-0.13601975/euler_characteristic` |
| 5 | 1.363525e-07 | 0.0037 | `0.12066692 / (betti_1 - 7.8468175)` | `0.12066692/(betti_1 - 1*7.8468175)` |
| 7 | 1.351219e-07 | 0.0045 | `-0.13639227 / (euler_characteristic + cos(exp(betti_1)))` | `-0.13639227/(euler_characteristic + cos(exp(betti_1)))` |
| 8 | 1.302105e-07 | 0.0370 | `-0.13670151 / (euler_characteristic - sin(euler_characteristic * -0.33241972))` | `-0.13670151/(euler_characteristic - sin(euler_characteristic*(-0.33241972)))` |
| 10 | 1.110500e-07 | 0.0796 | `0.1428703 / (betti_1 - (cos(betti_1 * -0.29996052) / -0.13828884))` | `0.1428703/(betti_1 - cos(betti_1*(-0.29996052))/(-0.13828884))` |
| 12 | 1.107361e-07 | 0.0014 | `0.14053237 / (betti_1 - ((0.1950842 - cos(betti_1 * -0.29996052)) / 0.14682452))` | `0.14053237/(betti_1 - (0.1950842 - cos(betti_1*(-0.29996052)))/0.14682452)` |
| 13 | 1.107361e-07 | 0.0000 | `sin(0.14053237 / (betti_1 - ((0.1950842 - cos(betti_1 * -0.29996052)) / 0.14682452)))` | `sin(0.14053237/(betti_1 - (0.1950842 - cos(betti_1*(-0.29996052)))/0.14682452))` |
| 14 | 1.092695e-07 | 0.0133 | `0.061163004 / ((betti_1 / 1.9248505) - ((1.9248475 - sin(betti_1 / 3.0530496)) * 2.8504953))` | `0.061163004/(betti_1/1.9248505 - 2.8504953*(1.9248475 - sin(betti_1/3.0530496)))` |
| 16 | 1.092523e-07 | 0.0001 | `0.061073568 / ((betti_1 / 1.9248469) - (2.8504949 * (1.9248469 - sin(-0.071583204 + (betti_1 / 3.0388985)))))` | `0.061073568/(betti_1/1.9248469 - 2.8504949*(1.9248469 - sin(betti_1/3.0388985 - 0.071583204)))` |
| 17 | 1.073360e-07 | 0.0177 | `0.060248733 / ((betti_1 / 1.9248167) - ((1.9248167 - sin((betti_1 - sin(euler_characteristic)) / 3.0650434)) * 3.0650434))` | `0.060248733/(betti_1/1.9248167 - 3.0650434*(1.9248167 - sin((betti_1 - sin(euler_characteristic))/3.0650434)))` |
| 20 | 1.066756e-07 | 0.0021 | `sin(0.060248733 / ((betti_1 / 1.9248167) - ((1.9248167 - sin((betti_1 - sin(n_hbonds * n_hbonds)) / 3.0650434)) * 3.0650434)))` | `sin(0.060248733/(betti_1/1.9248167 - 3.0650434*(1.9248167 - sin((betti_1 - sin(n_hbonds*n_hbonds))/3.0650434))))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: -0.13601975/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.934652e-07 | 0.0000 | `0.0021896518` | `0.00218965180000000` |
| 3 | 1.373526e-07 | 0.1713 | `-0.13601975 / euler_characteristic` | `-0.13601975/euler_characteristic` |
| 5 | 1.363523e-07 | 0.0037 | `-0.120727666 / (euler_characteristic - -6.8203464)` | `-0.120727666/(euler_characteristic - 1*(-6.8203464))` |
| 7 | 1.351632e-07 | 0.0044 | `(-0.054089315 / (euler_characteristic - -22.247227)) - -0.0008178865` | `-1*(-0.0008178865) - 0.054089315/(euler_characteristic - 1*(-22.247227))` |
| 8 | 1.301997e-07 | 0.0374 | `-0.13683626 / (euler_characteristic - sin(-0.33316693 * euler_characteristic))` | `-0.13683626/(euler_characteristic - sin(-0.33316693*euler_characteristic))` |
| 9 | 1.294453e-07 | 0.0058 | `-0.13979964 / (euler_characteristic - exp(sin(betti_1 * -0.27685097)))` | `-0.13979964/(euler_characteristic - exp(sin(betti_1*(-0.27685097))))` |
| 10 | 1.110601e-07 | 0.1532 | `-0.13979964 / (euler_characteristic - (6.5458126 * cos(euler_characteristic * 0.30502936)))` | `-0.13979964/(euler_characteristic - 6.5458126*cos(euler_characteristic*0.30502936))` |
| 11 | 1.086503e-07 | 0.0219 | `-0.12370321 / (euler_characteristic - (exp(cos(betti_1 * 0.35185778)) * -5.3319006))` | `-0.12370321/(euler_characteristic - (-5.3319006)*exp(cos(betti_1*0.35185778)))` |
| 16 | 1.077704e-07 | 0.0016 | `sin(-0.11949134 / (euler_characteristic - (6.0910897 * (-1.4103132 - cos((sin(euler_characteristic) + euler_characteristic) * 0.35841206)))))` | `sin(-0.11949134/(euler_characteristic - 6.0910897*(-cos((euler_characteristic + sin(euler_characteristic))*0.35841206) - 1.4103132)))` |
| 18 | 1.071662e-07 | 0.0028 | `sin(-0.12048531 / (euler_characteristic - ((-1.4103338 - cos((sin(n_hbonds * -0.3176463) - euler_characteristic) * 0.35994187)) * 6.0910926)))` | `sin(-0.12048531/(euler_characteristic - 6.0910926*(-cos((-euler_characteristic + sin(n_hbonds*(-0.3176463)))*0.35994187) - 1.4103338)))` |
| 20 | 1.070531e-07 | 0.0005 | `sin(-0.12048531 / (euler_characteristic - ((-1.4103338 - cos(0.35994187 * (cos(0.17597231 * (n_hbonds + betti_1)) - euler_characteristic))) * 6.0910926)))` | `sin(-0.12048531/(euler_characteristic - 6.0910926*(-cos(0.35994187*(-euler_characteristic + cos(0.17597231*(betti_1 + n_hbonds)))) - 1.4103338)))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -0.13601975/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.934653e-07 | 0.0000 | `0.002189652` | `0.00218965200000000` |
| 2 | 1.934652e-07 | 0.0000 | `sin(0.0021896793)` | `sin(0.0021896793)` |
| 3 | 1.373526e-07 | 0.3425 | `-0.13601975 / euler_characteristic` | `-0.13601975/euler_characteristic` |
| 5 | 1.355291e-07 | 0.0067 | `-0.15408087 / (86.74815 - n_hbonds)` | `-0.15408087/(86.74815 - n_hbonds)` |
| 6 | 1.355291e-07 | 0.0000 | `sin(-0.15408087 / (86.74815 - n_hbonds))` | `sin(-0.15408087/(86.74815 - n_hbonds))` |
| 7 | 1.349625e-07 | 0.0042 | `((4.518621 / betti_1) / betti_1) + 0.0010429949` | `0.0010429949 + 4.518621/(betti_1*betti_1)` |
| 8 | 1.302661e-07 | 0.0354 | `-0.1369077 / (euler_characteristic - cos(-0.30720556 * euler_characteristic))` | `-0.1369077/(euler_characteristic - cos(-0.30720556*euler_characteristic))` |
| 9 | 1.297376e-07 | 0.0041 | `-0.14062618 / (euler_characteristic - exp(cos(-0.3088159 * euler_characteristic)))` | `-0.14062618/(euler_characteristic - exp(cos(-0.3088159*euler_characteristic)))` |
| 10 | 1.108212e-07 | 0.1576 | `-0.14075024 / (euler_characteristic - (cos(euler_characteristic * -0.3048555) / 0.14440201))` | `-0.14075024/(euler_characteristic - cos(euler_characteristic*(-0.3048555))/0.14440201)` |
| 12 | 1.102164e-07 | 0.0027 | `(-0.15224455 / (euler_characteristic - (cos(euler_characteristic * 0.3059948) / 0.1520619))) - 0.00018250875` | `-1*0.00018250875 - 0.15224455/(euler_characteristic - cos(euler_characteristic*0.3059948)/0.1520619)` |
| 14 | 1.099472e-07 | 0.0012 | `-0.14075024 / ((euler_characteristic - (cos(-0.3048555 * euler_characteristic) / 0.14316826)) - sin(exp(betti_1)))` | `-0.14075024/(euler_characteristic - sin(exp(betti_1)) - cos(-0.3048555*euler_characteristic)/0.14316826)` |
| 15 | 1.083730e-07 | 0.0144 | `-0.1407324 / ((euler_characteristic - (cos(0.30477005 * euler_characteristic) / 0.14309274)) - cos(-0.6314676 * betti_1))` | `-0.1407324/(euler_characteristic - cos(-0.6314676*betti_1) - cos(0.30477005*euler_characteristic)/0.14309274)` |
| 17 | 1.080683e-07 | 0.0014 | `-0.1409552 / ((euler_characteristic - (cos(euler_characteristic * 0.30476657) / 0.14313011)) - (cos(euler_characteristic * -0.64411414) / 0.8109241))` | `-0.1409552/(euler_characteristic - cos(euler_characteristic*(-0.64411414))/0.8109241 - cos(euler_characteristic*0.30476657)/0.14313011)` |
| 18 | 1.073455e-07 | 0.0067 | `-0.1407324 / ((euler_characteristic - (cos(euler_characteristic * 0.30477005) / 0.14309274)) - (cos(euler_characteristic * -0.6441128) * exp(0.71018034)))` | `-0.1407324/(euler_characteristic - exp(0.71018034)*cos(euler_characteristic*(-0.6441128)) - cos(euler_characteristic*0.30477005)/0.14309274)` |
| 20 | 1.071933e-07 | 0.0007 | `-0.1407324 / (((euler_characteristic - (cos(0.30477005 * euler_characteristic) / 0.14309274)) - sin(euler_characteristic * 0.6082076)) - cos(euler_characteristic * -0.6441128))` | `-0.1407324/(euler_characteristic - sin(euler_characteristic*0.6082076) - cos(0.30477005*euler_characteristic)/0.14309274 - cos(euler_characteristic*(-0.6441128)))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: -0.13602005/euler_characteristic</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.934652e-07 | 0.0000 | `0.0021896511` | `0.00218965110000000` |
| 3 | 1.373526e-07 | 0.1713 | `-0.13602005 / euler_characteristic` | `-0.13602005/euler_characteristic` |
| 5 | 1.363517e-07 | 0.0037 | `0.12103967 / (betti_1 - 7.6812897)` | `0.12103967/(betti_1 - 1*7.6812897)` |
| 7 | 1.348368e-07 | 0.0056 | `((16.179554 / n_hbonds) / betti_1) + 0.0005549863` | `0.0005549863 + 16.179554/(betti_1*n_hbonds)` |
| 8 | 1.302023e-07 | 0.0350 | `-0.13672371 / (sin(0.33392715 * euler_characteristic) + euler_characteristic)` | `-0.13672371/(euler_characteristic + sin(0.33392715*euler_characteristic))` |
| 9 | 1.287691e-07 | 0.0111 | `-0.13382977 / (euler_characteristic + exp(cos(euler_characteristic * 0.35849035)))` | `-0.13382977/(euler_characteristic + exp(cos(euler_characteristic*0.35849035)))` |
| 10 | 1.107732e-07 | 0.1505 | `-0.14096707 / (euler_characteristic + (cos(-0.2999498 * betti_1) / -0.14181021))` | `-0.14096707/(euler_characteristic + cos(-0.2999498*betti_1)/(-0.14181021))` |
| 12 | 1.102911e-07 | 0.0022 | `-0.13423839 / ((cos(euler_characteristic * 0.30535164) / -0.14919196) + (3.9380918 - betti_1))` | `-0.13423839/(-betti_1 + cos(euler_characteristic*0.30535164)/(-0.14919196) + 3.9380918)` |
| 13 | 1.102490e-07 | 0.0004 | `-0.14096707 / (euler_characteristic + ((cos(euler_characteristic * 0.3048074) / -0.14181021) - sin(n_hbonds)))` | `-0.14096707/(euler_characteristic - sin(n_hbonds) + cos(euler_characteristic*0.3048074)/(-0.14181021))` |
| 14 | 1.098819e-07 | 0.0033 | `-0.14096707 / ((cos(0.30397168 * euler_characteristic) / -0.14096707) + (euler_characteristic - sin(exp(betti_1))))` | `-0.14096707/(euler_characteristic - sin(exp(betti_1)) + cos(0.30397168*euler_characteristic)/(-0.14096707))` |
| 15 | 1.083357e-07 | 0.0142 | `-0.14088668 / ((cos(euler_characteristic * 0.30476186) / -0.14088668) + (euler_characteristic - cos(0.49264196 * n_hbonds)))` | `-0.14088668/(euler_characteristic - cos(0.49264196*n_hbonds) + cos(euler_characteristic*0.30476186)/(-0.14088668))` |
| 17 | 1.070540e-07 | 0.0060 | `-0.14096707 / ((euler_characteristic + (cos(euler_characteristic * 0.3048074) / -0.14096707)) - (sin(-0.48297936 * n_hbonds) / 0.43328887))` | `-0.14096707/(euler_characteristic - sin(-0.48297936*n_hbonds)/0.43328887 + cos(euler_characteristic*0.3048074)/(-0.14096707))` |
| 18 | 1.070498e-07 | 0.0000 | `-0.14096707 / (euler_characteristic + ((cos(0.3048074 * euler_characteristic) / -0.14096707) - (sin(-0.48297936 * n_hbonds) / sin(0.43328887))))` | `-0.14096707/(euler_characteristic - sin(-0.48297936*n_hbonds)/sin(0.43328887) + cos(0.3048074*euler_characteristic)/(-0.14096707))` |
| 19 | 1.067704e-07 | 0.0026 | `-0.13742465 / ((((1.069558 - cos(betti_1 * 0.6305485)) / 0.42913175) - betti_1) + (cos(0.30505309 * euler_characteristic) / -0.13742465))` | `-0.13742465/(-betti_1 + (1.069558 - cos(betti_1*0.6305485))/0.42913175 + cos(0.30505309*euler_characteristic)/(-0.13742465))` |
| 20 | 1.065116e-07 | 0.0024 | `-0.14088668 / ((cos(euler_characteristic * 0.30476186) / -0.14088668) + ((euler_characteristic - cos(betti_1 * 0.6346606)) - cos(0.44912553 * n_hbonds)))` | `-0.14088668/(euler_characteristic - cos(0.44912553*n_hbonds) + cos(euler_characteristic*0.30476186)/(-0.14088668) - cos(betti_1*0.6346606))` |

</details>

