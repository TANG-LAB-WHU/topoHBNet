# Discovering Robust H-Bond Topological Laws via Multi-Run Symbolic Regression

This report presents the robust physical equations discovered by running multi-run Symbolic Regression (PySR) with stability selection. By executing independent evolutionary runs with different random seeds, we identify equations and topological invariants that consistently govern proton transport properties.

## 1. Study Settings
- **Target Transport Property**: `LBHB_Fraction`
- **Total Independent PySR Runs**: 10
- **Iterations Per Run**: 150
- **Input Topological Invariants**: `n_hbonds`, `betti_0`, `betti_1`, `betti_2`, `euler_characteristic`, `state_0D1A`, `state_0D2A`, `state_0D3A`, `state_0D4A`, `state_1D0A`, `state_1D1A`, `state_1D2A`, `state_1D3A`, `state_1D4A`, `state_1D5A`, `state_2D0A`, `state_2D1A`, `state_2D2A`, `state_2D3A`, `state_2D4A`, `state_2D5A`, `state_3D0A`, `state_3D1A`, `state_3D2A`, `state_3D3A`, `state_3D4A`, `state_4D1A`, `state_4D2A`, `state_4D3A`, `state_5D1A`, `state_5D2A`, `state_free H2O`

## 2. Robust Consensus Physical Laws (Voting Analysis)
Below is the frequency table of the 'best' equations selected by PySR across all runs. The equation with the highest vote count represents the most robust mathematical representation of the underlying physical relationship.

| Rank | Discovered Consensus Equation | Vote Count | Frequency | 
| :--- | :--- | :--- | :--- |
| 1 | `LBHB_Fraction ≈ -3.11e-5*state_1D1A*exp(-state_2D0A) + 0.00111` | 3/10 | 30.0% |
| 2 | `LBHB_Fraction ≈ 0.0012 - 0.000466/(state_2D0A + 11.8/state_1D1A)` | 1/10 | 10.0% |
| 3 | `LBHB_Fraction ≈ -1.73e-5*euler_characteristic - 1.73e-5*state_1D1A*exp(-state_2D0A)` | 1/10 | 10.0% |
| 4 | `LBHB_Fraction ≈ 0.00109*cos(0.327*state_2D0A - 0.327*log(state_1D1A))` | 1/10 | 10.0% |
| 5 | `LBHB_Fraction ≈ 0.00109 - 17.825311942959*exp(0.18*euler_characteristic - state_1D0A - state_2D0A)` | 1/10 | 10.0% |
| 6 | `LBHB_Fraction ≈ -7.88e-6*state_1D1A/(state_2D0A + 0.27) + 0.00108` | 1/10 | 10.0% |
| 7 | `LBHB_Fraction ≈ 9.12e-5*state_2D0A + 0.000869` | 1/10 | 10.0% |
| 8 | `LBHB_Fraction ≈ 1.7e-5*betti_1 - 1.7e-5*state_1D1A*exp(-state_2D0A)` | 1/10 | 10.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB\_Fraction \approx -3.11e-5*state\_1D1A*exp(-state\_2D0A) + 0.00111$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `state_2D0A` | Water donating 2 and accepting 0 H-bonds (extreme donor defect) | 100/128 | 78.1% | 🔥 High |
| `state_1D1A` | Water donating 1 and accepting 1 H-bonds (wire/chain intermediate) | 59/128 | 46.1% | ⚡ Medium |
| `state_3D0A` | Water donating 3 and accepting 0 H-bonds (extreme donor defect) | 33/128 | 25.8% | ❄️ Low |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 31/128 | 24.2% | ❄️ Low |
| `state_1D0A` | Water donating 1 and accepting 0 H-bonds | 29/128 | 22.7% | ❄️ Low |
| `state_0D4A` | Water donating 0 and accepting 4 H-bonds | 17/128 | 13.3% | ❄️ Low |
| `betti_1` | Number of independent H-bond loops/cycles | 8/128 | 6.2% | ❄️ Low |
| `state_1D3A` | Water donating 1 and accepting 3 H-bonds | 3/128 | 2.3% | ❄️ Low |
| `n_hbonds` | Total number of hydrogen bonds in the network | 0/128 | 0.0% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 0/128 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/128 | 0.0% | ❄️ Low |
| `state_0D1A` | Water donating 0 and accepting 1 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_0D2A` | Water donating 0 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_0D3A` | Water donating 0 and accepting 3 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_1D2A` | Water donating 1 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_1D4A` | Water donating 1 and accepting 4 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_1D5A` | Water donating 1 and accepting 5 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_2D1A` | Water donating 2 and accepting 1 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_2D2A` | Water donating 2 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_2D3A` | Water donating 2 and accepting 3 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_2D4A` | Water donating 2 and accepting 4 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_2D5A` | Water donating 2 and accepting 5 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_3D1A` | Water donating 3 and accepting 1 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_3D2A` | Water donating 3 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_3D3A` | Water donating 3 and accepting 3 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_3D4A` | Water donating 3 and accepting 4 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_4D1A` | Water donating 4 and accepting 1 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_4D2A` | Water donating 4 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_4D3A` | Water donating 4 and accepting 3 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_5D1A` | Water donating 5 and accepting 1 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_5D2A` | Water donating 5 and accepting 2 H-bonds | 0/128 | 0.0% | ❄️ Low |
| `state_free H2O` | Topological descriptor | 0/128 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `state_2D0A` is the most stable feature (appearing in 100/128 Pareto equations). This strongly indicates that `state_2D0A` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: 0.0012 - 0.000466/(state_2D0A + 11.8/state_1D1A)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936001` | `0.000993600100000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936034)` | `sin(0.0009936034)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.6172933e-5` | `euler_characteristic*(-1.6172933e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.121752e-5) + 0.00086871115` | `state_2D0A*9.121752e-5 + 0.00086871115` |
| 6 | 2.708107e-08 | 0.0940 | `0.0011099349 - (0.00031167018 / exp(state_2D0A))` | `0.0011099349 - 0.00031167018/exp(state_2D0A)` |
| 7 | 2.696226e-08 | 0.0044 | `0.0011368453 - (0.00019960971 / (state_2D0A + 0.5763613))` | `0.0011368453 - 0.00019960971/(state_2D0A + 0.5763613)` |
| 8 | 2.516755e-08 | 0.0689 | `0.0011146746 - (0.00036065798 / exp(state_2D0A + state_3D0A))` | `0.0011146746 - 0.00036065798/exp(state_2D0A + state_3D0A)` |
| 9 | 2.159497e-08 | 0.1531 | `0.0012042727 + (-0.0004658493 / (state_2D0A - (-11.833755 / state_1D1A)))` | `0.0012042727 - 0.0004658493/(state_2D0A - (-1)*11.833755/state_1D1A)` |
| 11 | 2.043757e-08 | 0.0275 | `0.0012120336 - (0.0004797607 / ((state_0D4A + state_2D0A) - (-11.7325735 / state_1D1A)))` | `0.0012120336 - 0.0004797607/(state_0D4A + state_2D0A - (-1)*11.7325735/state_1D1A)` |
| 13 | 1.910029e-08 | 0.0338 | `0.0012042727 - (0.0004797607 / (((state_0D4A + state_2D0A) + state_3D0A) - (-11.170434 / state_1D1A)))` | `0.0012042727 - 0.0004797607/(state_0D4A + state_2D0A + state_3D0A - (-1)*11.170434/state_1D1A)` |
| 14 | 1.910028e-08 | 0.0000 | `sin(0.0012042727 - (0.0004797607 / (((state_0D4A + state_2D0A) + state_3D0A) - (-11.170434 / state_1D1A))))` | `sin(0.0012042727 - 0.0004797607/(state_0D4A + state_2D0A + state_3D0A - (-1)*11.170434/state_1D1A))` |
| 15 | 1.889609e-08 | 0.0107 | `0.0012042727 - (0.00046746287 / (state_0D4A + (((state_2D0A + state_3D0A) - (-11.833755 / state_1D1A)) - 0.09452321)))` | `0.0012042727 - 0.00046746287/(state_0D4A + state_2D0A + state_3D0A - 1*0.09452321 - (-1)*11.833755/state_1D1A)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: -1.73e-5*euler_characteristic - 1.73e-5*state_1D1A*exp(-state_2D0A)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936038` | `0.000993603800000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936034)` | `sin(0.0009936034)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.617298e-5` | `euler_characteristic*(-1.617298e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.122079e-5) + 0.0008687059` | `state_2D0A*9.122079e-5 + 0.0008687059` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.0003116763 / exp(state_2D0A)) + 0.0011099394` | `0.0011099394 - 0.0003116763*exp(-state_2D0A)` |
| 7 | 2.696224e-08 | 0.0044 | `(-0.00020119753 / (state_2D0A + 0.58009386)) + 0.0011374118` | `0.0011374118 - 0.00020119753/(state_2D0A + 0.58009386)` |
| 8 | 2.413511e-08 | 0.1108 | `(euler_characteristic + (state_1D1A / exp(state_2D0A))) * -1.7252647e-5` | `(euler_characteristic + state_1D1A/exp(state_2D0A))*(-1.7252647e-5)` |
| 9 | 2.272037e-08 | 0.0604 | `-1.8148032e-5 * (euler_characteristic + (state_1D1A / (state_2D0A - -0.6109844)))` | `-1.8148032e-5*(euler_characteristic + state_1D1A/(state_2D0A - 1*(-0.6109844)))` |
| 10 | 2.234479e-08 | 0.0167 | `(euler_characteristic + (state_1D1A / (exp(state_2D0A) + -0.34610367))) * -1.7586686e-5` | `(euler_characteristic + state_1D1A/(exp(state_2D0A) - 0.34610367))*(-1.7586686e-5)` |
| 11 | 2.119634e-08 | 0.0528 | `((state_1D1A / (state_2D0A + (state_1D0A - -0.51853746))) + euler_characteristic) * -1.8021703e-5` | `(euler_characteristic + state_1D1A/(state_1D0A + state_2D0A - 1*(-0.51853746)))*(-1.8021703e-5)` |
| 12 | 2.070365e-08 | 0.0235 | `-1.7792085e-5 * ((exp(0.62722594 - (state_2D0A + state_1D0A)) * state_1D1A) + euler_characteristic)` | `-1.7792085e-5*(euler_characteristic + state_1D1A*exp(0.62722594 - (state_1D0A + state_2D0A)))` |
| 13 | 1.920284e-08 | 0.0753 | `-1.7792085e-5 * ((exp(sin(state_1D3A) - (state_2D0A + state_1D0A)) * state_1D1A) + euler_characteristic)` | `-1.7792085e-5*(euler_characteristic + state_1D1A*exp(-(state_1D0A + state_2D0A) + sin(state_1D3A)))` |
| 14 | 1.902595e-08 | 0.0093 | `((state_1D1A * exp(sin(sin(state_1D3A)) - (state_2D0A + state_1D0A))) + euler_characteristic) * -1.7644188e-5` | `(euler_characteristic + state_1D1A*exp(-(state_1D0A + state_2D0A) + sin(sin(state_1D3A))))*(-1.7644188e-5)` |
| 15 | 1.801138e-08 | 0.0548 | `((state_1D1A * exp(sin(state_1D3A) - (state_3D0A + (state_2D0A + state_1D0A)))) + euler_characteristic) * -1.7644188e-5` | `(euler_characteristic + state_1D1A*exp(-(state_1D0A + state_2D0A + state_3D0A) + sin(state_1D3A)))*(-1.7644188e-5)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.00109*cos(0.327*state_2D0A - 0.327*log(state_1D1A))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936225` | `0.000993622500000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173259e-5` | `euler_characteristic*(-1.6173259e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.1219015e-5) + 0.0008687092` | `state_2D0A*9.1219015e-5 + 0.0008687092` |
| 6 | 2.973710e-08 | 0.0005 | `sin((state_2D0A * -9.001365e-5) + 9.423907)` | `sin(9.423907 + state_2D0A*(-9.001365e-5))` |
| 7 | 2.709130e-08 | 0.0932 | `cos(exp(-0.30917287 - state_2D0A)) * 0.0010602358` | `cos(exp(-state_2D0A - 0.30917287))*0.0010602358` |
| 8 | 2.680952e-08 | 0.0105 | `cos((state_1D1A - state_2D0A) * 0.057768483) * 0.0011321885` | `cos((state_1D1A - state_2D0A)*0.057768483)*0.0011321885` |
| 9 | 2.389564e-08 | 0.1151 | `cos((log(state_1D1A) - state_2D0A) * 0.32672217) * 0.0010896147` | `0.0010896147*cos(0.32672217*state_2D0A - 0.32672217*log(state_1D1A))` |
| 10 | 2.133806e-08 | 0.1132 | `cos(state_1D1A * (0.047738146 / (-0.7248841 - state_2D0A))) * 0.0010648256` | `cos(state_1D1A*0.047738146/(-state_2D0A - 0.7248841))*0.0010648256` |
| 12 | 1.994303e-08 | 0.0338 | `cos(state_1D1A * (0.049986444 / ((state_2D0A - -0.7233804) + state_0D4A))) * 0.0010648256` | `cos(state_1D1A*0.049986444/(state_0D4A + state_2D0A - 1*(-0.7233804)))*0.0010648256` |
| 13 | 1.993782e-08 | 0.0003 | `cos(state_1D1A * (-0.04990987 / ((state_2D0A - -0.7233804) + sin(state_0D4A)))) * 0.0010648256` | `cos(state_1D1A*(-0.04990987)/(state_2D0A + sin(state_0D4A) - 1*(-0.7233804)))*0.0010648256` |
| 14 | 1.941886e-08 | 0.0264 | `cos((state_1D0A - state_1D1A) * (0.051434297 / ((state_2D0A - -0.7248841) + state_0D4A))) * 0.0010648256` | `cos((state_1D0A - state_1D1A)*0.051434297/(state_0D4A + state_2D0A - 1*(-0.7248841)))*0.0010648256` |
| 15 | 1.941392e-08 | 0.0003 | `cos(((state_1D0A - state_1D1A) * 0.051434297) / ((state_2D0A - -0.7248841) + sin(state_0D4A))) * 0.0010648256` | `cos((state_1D0A - state_1D1A)*0.051434297/(state_2D0A + sin(state_0D4A) - 1*(-0.7248841)))*0.0010648256` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: 0.00109 - 17.825311942959*exp(0.18*euler_characteristic - state_1D0A - state_2D0A)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.000993602` | `0.000993602000000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936035)` | `sin(0.0009936035)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.617321e-5` | `euler_characteristic*(-1.617321e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.122644e-5) + 0.00086868333` | `state_2D0A*9.122644e-5 + 0.00086868333` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.0003116741 / exp(state_2D0A)) + 0.0011099379` | `0.0011099379 - 0.0003116741*exp(-state_2D0A)` |
| 7 | 2.696228e-08 | 0.0044 | `(-0.00019860399 / (state_2D0A + 0.5740066)) + 0.0011364832` | `0.0011364832 - 0.00019860399/(state_2D0A + 0.5740066)` |
| 8 | 2.515184e-08 | 0.0695 | `(-0.00035592922 / exp(state_3D0A + state_2D0A)) + 0.0011167298` | `0.0011167298 - 0.00035592922*exp(-state_2D0A - state_3D0A)` |
| 9 | 2.493110e-08 | 0.0088 | `0.0011382138 - (0.00019911924 / (state_2D0A + (state_3D0A + 0.51084775)))` | `0.0011382138 - 0.00019911924/(state_2D0A + state_3D0A + 0.51084775)` |
| 10 | 2.234509e-08 | 0.1095 | `(exp((0.18347834 * euler_characteristic) - state_2D0A) / -0.067277096) - -0.0010861373` | `exp(0.18347834*euler_characteristic - state_2D0A)/(-0.067277096) - 1*(-0.0010861373)` |
| 11 | 2.193686e-08 | 0.0184 | `(-0.0012195992 / exp(state_1D0A + exp(state_3D0A + state_2D0A))) + 0.0010663427` | `0.0010663427 - 0.0012195992*exp(-state_1D0A - exp(state_2D0A + state_3D0A))` |
| 12 | 1.927261e-08 | 0.1295 | `(exp(((0.18014003 * euler_characteristic) - state_1D0A) - state_2D0A) / -0.05605183) - -0.0010861373` | `exp(0.18014003*euler_characteristic - state_1D0A - state_2D0A)/(-0.05605183) - 1*(-0.0010861373)` |
| 13 | 1.905408e-08 | 0.0114 | `(exp(cos(state_1D0A) + ((euler_characteristic * 0.19496842) - state_2D0A)) / -0.067277096) - -0.0010861373` | `exp(euler_characteristic*0.19496842 - state_2D0A + cos(state_1D0A))/(-0.067277096) - 1*(-0.0010861373)` |
| 14 | 1.812132e-08 | 0.0502 | `(exp(((0.18014003 * euler_characteristic) - state_1D0A) - (state_3D0A + state_2D0A)) / -0.0548617) - -0.0010861373` | `exp(0.18014003*euler_characteristic - state_1D0A - (state_2D0A + state_3D0A))/(-0.0548617) - 1*(-0.0010861373)` |
| 15 | 1.809998e-08 | 0.0012 | `(exp(cos(state_1D0A) + ((euler_characteristic * 0.19496842) - (state_3D0A + state_2D0A))) / -0.0652801) - -0.0010861373` | `exp(euler_characteristic*0.19496842 - (state_2D0A + state_3D0A) + cos(state_1D0A))/(-0.0652801) - 1*(-0.0010861373)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: -3.11e-5*state_1D1A*exp(-state_2D0A) + 0.00111</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936038` | `0.000993603800000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936227)` | `sin(0.0009936227)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.6173464e-5` | `euler_characteristic*(-1.6173464e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.128706e-5) + 0.0008686059` | `state_2D0A*9.128706e-5 + 0.0008686059` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.000311672 / exp(state_2D0A)) - -0.0011099378` | `-1*(-0.0011099378) - 0.000311672*exp(-state_2D0A)` |
| 7 | 2.698569e-08 | 0.0035 | `(-0.000281766 / (state_2D0A + 0.758779)) - -0.0011640907` | `-1*(-0.0011640907) - 0.000281766/(state_2D0A + 0.758779)` |
| 8 | 2.217356e-08 | 0.1964 | `((state_1D1A * -3.1134696e-5) / exp(state_2D0A)) - -0.0011099378` | `state_1D1A*(-3.1134696e-5)/exp(state_2D0A) - 1*(-0.0011099378)` |
| 9 | 2.217356e-08 | 0.0000 | `sin(((state_1D1A * -3.1134696e-5) / exp(state_2D0A)) - -0.0011099378)` | `sin(state_1D1A*(-3.1134696e-5)/exp(state_2D0A) - 1*(-0.0011099378))` |
| 10 | 2.086231e-08 | 0.0610 | `(state_1D1A * (-3.6476176e-5 / (state_1D0A + exp(state_2D0A)))) - -0.0011099378` | `state_1D1A*(-3.6476176e-5)/(state_1D0A + exp(state_2D0A)) - 1*(-0.0011099378)` |
| 12 | 1.887976e-08 | 0.0499 | `((state_1D1A * -3.970491e-5) / (state_1D0A + exp(state_3D0A + state_2D0A))) - -0.0011099378` | `state_1D1A*(-3.970491e-5)/(state_1D0A + exp(state_2D0A + state_3D0A)) - 1*(-0.0011099378)` |
| 14 | 1.798920e-08 | 0.0242 | `((state_1D1A * -4.0854306e-5) / (state_1D0A + exp((state_0D4A + state_3D0A) + state_2D0A))) - -0.0011099378` | `state_1D1A*(-4.0854306e-5)/(state_1D0A + exp(state_0D4A + state_2D0A + state_3D0A)) - 1*(-0.0011099378)` |

</details>

<details>
<summary><b>Run 6 (Seed: 47) — Best Equation: -7.88e-6*state_1D1A/(state_2D0A + 0.27) + 0.00108</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.000993622` | `0.000993622000000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.617301e-5` | `euler_characteristic*(-1.617301e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.121831e-5) + 0.00086870993` | `state_2D0A*9.121831e-5 + 0.00086870993` |
| 6 | 2.708107e-08 | 0.0940 | `0.0011099422 - (0.00031168043 / exp(state_2D0A))` | `0.0011099422 - 0.00031168043/exp(state_2D0A)` |
| 7 | 2.696225e-08 | 0.0044 | `0.001137953 - (0.0002027075 / (state_2D0A + 0.5836146))` | `0.001137953 - 0.0002027075/(state_2D0A + 0.5836146)` |
| 8 | 2.515184e-08 | 0.0695 | `0.0011167387 - (0.00035595708 / exp(state_2D0A + state_3D0A))` | `0.0011167387 - 0.00035595708/exp(state_2D0A + state_3D0A)` |
| 9 | 2.243079e-08 | 0.1145 | `0.0010846015 - ((state_1D1A * 7.8757585e-6) / (state_2D0A - -0.26973924))` | `0.0010846015 - 7.8757585e-6*state_1D1A/(state_2D0A - 1*(-0.26973924))` |
| 11 | 2.105985e-08 | 0.0315 | `0.0010846015 - ((state_1D1A * 7.8757585e-6) / ((state_3D0A + state_2D0A) - -0.24719627))` | `0.0010846015 - 7.8757585e-6*state_1D1A/(state_2D0A + state_3D0A - 1*(-0.24719627))` |
| 12 | 2.105985e-08 | 0.0000 | `sin(0.0010846015 - ((state_1D1A * 7.8757585e-6) / (state_3D0A + (state_2D0A - -0.24719627))))` | `sin(0.0010846015 - 7.8757585e-6*state_1D1A/(state_2D0A + state_3D0A - 1*(-0.24719627)))` |
| 13 | 1.995408e-08 | 0.0539 | `0.0010846015 + ((state_1D1A * -7.764246e-6) / (((state_3D0A + state_0D4A) + state_2D0A) - -0.23275135))` | `state_1D1A*(-7.764246e-6)/(state_0D4A + state_2D0A + state_3D0A - 1*(-0.23275135)) + 0.0010846015` |
| 14 | 1.980806e-08 | 0.0073 | `0.0010801663 - ((state_1D1A * -8.58742e-6) / (sin(-0.22169162 - state_1D0A) - (state_3D0A + state_2D0A)))` | `0.0010801663 - (-8.58742e-6)*state_1D1A/(-(state_2D0A + state_3D0A) + sin(-state_1D0A - 0.22169162))` |
| 15 | 1.936806e-08 | 0.0225 | `0.0010801663 - ((state_1D1A * -8.58742e-6) / ((-0.22169162 - state_1D0A) - ((state_3D0A + state_0D4A) + state_2D0A)))` | `0.0010801663 - (-8.58742e-6)*state_1D1A/(-state_1D0A - (state_0D4A + state_2D0A + state_3D0A) - 0.22169162)` |

</details>

<details>
<summary><b>Run 7 (Seed: 48) — Best Equation: -3.11e-5*state_1D1A*exp(-state_2D0A) + 0.00111</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936206` | `0.000993620600000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936433)` | `sin(0.0009936433)` |
| 3 | 3.435609e-08 | 0.0735 | `euler_characteristic * -1.617276e-5` | `euler_characteristic*(-1.617276e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.1219496e-5) - -0.00086870836` | `state_2D0A*9.1219496e-5 - 1*(-0.00086870836)` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.0003116723 / exp(state_2D0A)) + 0.0011099376` | `0.0011099376 - 0.0003116723*exp(-state_2D0A)` |
| 7 | 2.696225e-08 | 0.0044 | `(-0.00020312717 / (state_2D0A + 0.58459765)) + 0.0011381031` | `0.0011381031 - 0.00020312717/(state_2D0A + 0.58459765)` |
| 8 | 2.217348e-08 | 0.1955 | `((state_1D1A / exp(state_2D0A)) * -3.1118157e-5) + 0.0011096029` | `state_1D1A*(-3.1118157e-5)/exp(state_2D0A) + 0.0011096029` |
| 9 | 2.199860e-08 | 0.0079 | `(state_1D1A * (-2.4937639e-5 / (state_2D0A - -0.7268348))) + 0.0011464816` | `state_1D1A*(-2.4937639e-5)/(state_2D0A - 1*(-0.7268348)) + 0.0011464816` |
| 10 | 2.080420e-08 | 0.0558 | `((state_1D1A * -3.3118213e-5) / exp(state_3D0A + state_2D0A)) + 0.001109184` | `state_1D1A*(-3.3118213e-5)/exp(state_2D0A + state_3D0A) + 0.001109184` |
| 12 | 1.886291e-08 | 0.0490 | `((state_1D1A * -4.02249e-5) / (state_1D0A + exp(state_2D0A + state_3D0A))) + 0.0011152271` | `state_1D1A*(-4.02249e-5)/(state_1D0A + exp(state_2D0A + state_3D0A)) + 0.0011152271` |
| 14 | 1.795492e-08 | 0.0247 | `((state_1D1A * -4.2037747e-5) / (state_1D0A + exp(state_0D4A + (state_3D0A + state_2D0A)))) + 0.0011152271` | `state_1D1A*(-4.2037747e-5)/(state_1D0A + exp(state_0D4A + state_2D0A + state_3D0A)) + 0.0011152271` |

</details>

<details>
<summary><b>Run 8 (Seed: 49) — Best Equation: 9.12e-5*state_2D0A + 0.000869</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.000993622` | `0.000993622000000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173197e-5` | `euler_characteristic*(-1.6173197e-5)` |
| 4 | 3.435608e-08 | 0.0000 | `sin(euler_characteristic * -1.6173197e-5)` | `sin(euler_characteristic*(-1.6173197e-5))` |
| 5 | 2.975064e-08 | 0.1439 | `(state_2D0A * 9.122121e-5) + 0.00086870586` | `state_2D0A*9.122121e-5 + 0.00086870586` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.00031167397 / exp(state_2D0A)) + 0.0011099378` | `0.0011099378 - 0.00031167397*exp(-state_2D0A)` |
| 7 | 2.696224e-08 | 0.0044 | `(-0.00020144884 / (state_2D0A + 0.5806491)) + 0.0011375048` | `0.0011375048 - 0.00020144884/(state_2D0A + 0.5806491)` |
| 8 | 2.515184e-08 | 0.0695 | `(-0.00035591738 / exp(state_2D0A + state_3D0A)) + 0.0011167241` | `0.0011167241 - 0.00035591738*exp(-state_2D0A - state_3D0A)` |
| 9 | 2.486891e-08 | 0.0113 | `(0.00237656 / ((euler_characteristic / state_1D1A) - state_2D0A)) - -0.001303311` | `-1*(-0.001303311) + 0.00237656/(euler_characteristic/state_1D1A - state_2D0A)` |
| 10 | 2.155192e-08 | 0.1432 | `((state_1D1A * (0.0018924914 / euler_characteristic)) / exp(state_2D0A)) + 0.0011099378` | `0.0011099378 + state_1D1A*0.0018924914/(euler_characteristic*exp(state_2D0A))` |
| 11 | 2.103275e-08 | 0.0244 | `(0.031792045 / ((state_1D1A / (state_2D0A - -0.5892713)) + euler_characteristic)) - -0.0015941678` | `-1*(-0.0015941678) + 0.031792045/(euler_characteristic + state_1D1A/(state_2D0A - 1*(-0.5892713)))` |
| 12 | 2.037509e-08 | 0.0318 | `(((state_1D1A * 0.0018924914) / euler_characteristic) / exp(state_2D0A + state_3D0A)) + 0.0011099378` | `0.0011099378 + state_1D1A*0.0018924914/(euler_characteristic*exp(state_2D0A + state_3D0A))` |
| 13 | 2.000231e-08 | 0.0185 | `(0.033491194 / (euler_characteristic + (state_1D1A / ((state_0D4A + 0.58416474) + state_2D0A)))) - -0.0016238539` | `-1*(-0.0016238539) + 0.033491194/(euler_characteristic + state_1D1A/(state_0D4A + state_2D0A + 0.58416474))` |
| 14 | 1.972470e-08 | 0.0140 | `(0.034593727 / (((state_1D1A / exp(state_0D4A + state_2D0A)) * 1.6729786) + euler_characteristic)) - -0.0016348892` | `-1*(-0.0016348892) + 0.034593727/(euler_characteristic + state_1D1A*1.6729786/exp(state_0D4A + state_2D0A))` |
| 15 | 1.878880e-08 | 0.0486 | `(0.0016412532 / (euler_characteristic / (state_1D1A / (((state_3D0A + state_2D0A) + state_1D0A) + 0.65031147)))) - -0.0011379127` | `-1*(-0.0011379127) + 0.0016412532/((euler_characteristic/((state_1D1A/(state_1D0A + state_2D0A + state_3D0A + 0.65031147)))))` |

</details>

<details>
<summary><b>Run 9 (Seed: 50) — Best Equation: -3.11e-5*state_1D1A*exp(-state_2D0A) + 0.00111</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936087` | `0.000993608700000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936226)` | `sin(0.0009936226)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.617341e-5` | `euler_characteristic*(-1.617341e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.1215625e-5) + 0.00086871337` | `state_2D0A*9.1215625e-5 + 0.00086871337` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.00031167487 / exp(state_2D0A)) + 0.0011099395` | `0.0011099395 - 0.00031167487*exp(-state_2D0A)` |
| 7 | 2.696389e-08 | 0.0043 | `(-0.00022068873 / (state_2D0A + 0.62521833)) + 0.0011442405` | `0.0011442405 - 0.00022068873/(state_2D0A + 0.62521833)` |
| 8 | 2.217348e-08 | 0.1956 | `((state_1D1A * -3.1117754e-5) / exp(state_2D0A)) + 0.0011096011` | `state_1D1A*(-3.1117754e-5)/exp(state_2D0A) + 0.0011096011` |
| 9 | 2.200058e-08 | 0.0078 | `((state_1D1A * -2.6359367e-5) / (state_2D0A + 0.76304555)) + 0.0011502083` | `state_1D1A*(-2.6359367e-5)/(state_2D0A + 0.76304555) + 0.0011502083` |
| 10 | 2.080420e-08 | 0.0559 | `0.0011091831 - (state_1D1A * (3.3117976e-5 / exp(state_2D0A + state_3D0A)))` | `0.0011091831 - 3.3117976e-5*state_1D1A/exp(state_2D0A + state_3D0A)` |
| 11 | 2.080419e-08 | 0.0000 | `((state_1D1A * -3.3116477e-5) / (exp(state_3D0A) * exp(state_2D0A))) + 0.001109172` | `state_1D1A*(-3.3116477e-5)/(exp(state_2D0A)*exp(state_3D0A)) + 0.001109172` |
| 12 | 1.889387e-08 | 0.0963 | `0.0011099395 + ((-4.03136e-5 * state_1D1A) / (exp(state_2D0A + state_3D0A) + state_1D0A))` | `-4.03136e-5*state_1D1A/(state_1D0A + exp(state_2D0A + state_3D0A)) + 0.0011099395` |
| 13 | 1.873306e-08 | 0.0085 | `(((-4.03136e-5 * state_1D1A) / (state_1D0A + exp(state_3D0A))) / exp(state_2D0A)) + 0.0011099395` | `-4.03136e-5*state_1D1A/((state_1D0A + exp(state_3D0A))*exp(state_2D0A)) + 0.0011099395` |
| 14 | 1.799653e-08 | 0.0401 | `0.0011099395 + ((-4.03136e-5 * state_1D1A) / (exp(state_0D4A + (state_2D0A + state_3D0A)) + state_1D0A))` | `-4.03136e-5*state_1D1A/(state_1D0A + exp(state_0D4A + state_2D0A + state_3D0A)) + 0.0011099395` |
| 15 | 1.787216e-08 | 0.0069 | `0.0011099395 + (((-4.03136e-5 * state_1D1A) / (exp(state_0D4A + state_3D0A) + state_1D0A)) / exp(state_2D0A))` | `-4.03136e-5*state_1D1A/((state_1D0A + exp(state_0D4A + state_3D0A))*exp(state_2D0A)) + 0.0011099395` |

</details>

<details>
<summary><b>Run 10 (Seed: 51) — Best Equation: 1.7e-5*betti_1 - 1.7e-5*state_1D1A*exp(-state_2D0A)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936038` | `0.000993603800000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936221)` | `sin(0.0009936221)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.617301e-5` | `euler_characteristic*(-1.617301e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.121681e-5) - -0.0008687162` | `state_2D0A*9.121681e-5 - 1*(-0.0008687162)` |
| 6 | 2.897216e-08 | 0.0265 | `log(state_2D0A + 4.420034) * 0.0005699106` | `0.0005699106*log(state_2D0A + 4.420034)` |
| 7 | 2.720014e-08 | 0.0631 | `(-5.5287503e-5 / (0.20125188 + state_2D0A)) - -0.0010671105` | `-1*(-0.0010671105) - 5.5287503e-5/(state_2D0A + 0.20125188)` |
| 8 | 2.420965e-08 | 0.1165 | `(betti_1 - (state_1D1A / exp(state_2D0A))) * 1.695693e-5` | `(betti_1 - state_1D1A/exp(state_2D0A))*1.695693e-5` |
| 9 | 2.266176e-08 | 0.0661 | `(betti_1 + (state_1D1A / (-0.6038021 - state_2D0A))) * 1.783325e-5` | `(betti_1 + state_1D1A/(-state_2D0A - 0.6038021))*1.783325e-5` |
| 10 | 2.232845e-08 | 0.0148 | `(betti_1 - (state_1D1A / (exp(state_2D0A) - 0.34774244))) * 1.7207134e-5` | `(betti_1 - state_1D1A/(exp(state_2D0A) - 1*0.34774244))*1.7207134e-5` |
| 11 | 2.117929e-08 | 0.0528 | `(betti_1 - (state_1D1A / (state_1D0A - (-0.5086417 - state_2D0A)))) * 1.7802793e-5` | `(betti_1 - state_1D1A/(state_1D0A - (-state_2D0A - 0.5086417)))*1.7802793e-5` |
| 12 | 2.083931e-08 | 0.0162 | `1.7601988e-5 * (betti_1 + ((state_1D1A / exp(state_2D0A)) / (-0.55344844 - state_1D0A)))` | `1.7601988e-5*(betti_1 + state_1D1A/((-state_1D0A - 0.55344844)*exp(state_2D0A)))` |
| 13 | 1.967962e-08 | 0.0573 | `1.7601988e-5 * (betti_1 - (state_1D1A / (state_1D0A - ((-0.46835008 - state_2D0A) - state_3D0A))))` | `1.7601988e-5*(betti_1 - state_1D1A/(state_1D0A - (-state_2D0A - state_3D0A - 0.46835008)))` |
| 14 | 1.920382e-08 | 0.0245 | `1.7601988e-5 * (betti_1 - ((state_1D1A / exp(state_2D0A)) / (state_1D0A - (-0.46835008 - state_3D0A))))` | `1.7601988e-5*(betti_1 - state_1D1A/((state_1D0A - (-state_3D0A - 0.46835008))*exp(state_2D0A)))` |
| 15 | 1.890373e-08 | 0.0158 | `(betti_1 - (state_1D1A / (state_1D0A - ((-0.43635207 - state_2D0A) - (state_3D0A + state_0D4A))))) * 1.7601988e-5` | `(betti_1 - state_1D1A/(state_1D0A - (-state_2D0A - (state_0D4A + state_3D0A) - 0.43635207)))*1.7601988e-5` |

</details>

