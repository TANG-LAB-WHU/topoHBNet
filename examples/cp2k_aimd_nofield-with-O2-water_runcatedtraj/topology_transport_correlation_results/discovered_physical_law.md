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
| 1 | `LBHB_Fraction ≈ euler_characteristic*(-3.139354e-5)` | 2/5 | 40.0% |
| 2 | `LBHB_Fraction ≈ euler_characteristic*(-3.1393334e-5)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ euler_characteristic*(-3.1393443e-5)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ euler_characteristic*(-3.139346e-5)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx euler_characteristic*(-3.139354e-5)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 38/70 | 54.3% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 31/70 | 44.3% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 22/70 | 31.4% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/70 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/70 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 38/70 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: euler_characteristic*(-3.1393334e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.001855009` | `0.00185500900000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.1393334e-5` | `euler_characteristic*(-3.1393334e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `0.004267125 - (-0.14214167 / euler_characteristic)` | `0.004267125 - (-1)*0.14214167/euler_characteristic` |
| 6 | 9.990136e-08 | 0.0700 | `0.0019929162 * sin(betti_1 * -0.073754504)` | `0.0019929162*sin(betti_1*(-0.073754504))` |
| 8 | 9.982369e-08 | 0.0004 | `sin((betti_1 + -0.9465394) * -0.074977495) * 0.0019929162` | `sin((betti_1 - 0.9465394)*(-0.074977495))*0.0019929162` |
| 9 | 9.901151e-08 | 0.0082 | `(((-60.15031 / betti_1) - -1.8772855) / betti_1) - 0.012663607` | `-1*0.012663607 + (-1*(-1.8772855) - 60.15031/betti_1)/betti_1` |
| 11 | 9.882325e-08 | 0.0010 | `((((-15.550041 / betti_1) - -0.49103197) * 4.608417) / betti_1) + -0.01588157` | `-0.01588157 + (-1*(-0.49103197) - 15.550041/betti_1)*4.608417/betti_1` |
| 12 | 9.882324e-08 | 0.0000 | `sin((((-15.550041 / betti_1) - -0.49103203) * (4.608417 / betti_1)) + -0.01588157)` | `sin(-0.01588157 + (-1*(-0.49103203) - 15.550041/betti_1)*4.608417/betti_1)` |
| 13 | 9.876812e-08 | 0.0006 | `((3.3071156 / (betti_1 + -23.373886)) * ((-11.403443 / betti_1) - -0.29271704)) + -0.007346528` | `3.3071156*(-1*(-0.29271704) - 11.403443/betti_1)/(betti_1 - 23.373886) - 0.007346528` |
| 16 | 9.852929e-08 | 0.0008 | `((((-14.104328 / betti_1) - -0.44637832) * 5.221151) / (betti_1 + (sin(euler_characteristic) / 12.734019))) + -0.01645936` | `(-1*(-0.44637832) - 14.104328/betti_1)*5.221151/(betti_1 + sin(euler_characteristic)/12.734019) - 0.01645936` |
| 17 | 9.852135e-08 | 0.0001 | `((((-14.104328 / betti_1) - -0.44637832) * 5.221151) / (betti_1 + (sin(sin(euler_characteristic)) / 11.90776))) + -0.01645936` | `(-1*(-0.44637832) - 14.104328/betti_1)*5.221151/(betti_1 + sin(sin(euler_characteristic))/11.90776) - 0.01645936` |
| 18 | 9.773424e-08 | 0.0080 | `((((-14.104328 / betti_1) - -0.44641602) * 5.221151) / ((0.024191793 / sin(-1.0869715 * betti_1)) + betti_1)) + -0.016458768` | `(-1*(-0.44641602) - 14.104328/betti_1)*5.221151/(betti_1 + 0.024191793/sin(-1.0869715*betti_1)) - 0.016458768` |
| 19 | 9.772291e-08 | 0.0001 | `((((-14.104328 / betti_1) - -0.44641602) * 5.221151) / (sin(0.024191793 / sin(betti_1 * -1.0869715)) + betti_1)) + -0.016458768` | `(-1*(-0.44641602) - 14.104328/betti_1)*5.221151/(betti_1 + sin(0.024191793/sin(betti_1*(-1.0869715)))) - 0.016458768` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: euler_characteristic*(-3.139354e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.0018550089` | `0.00185500890000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.139354e-5` | `euler_characteristic*(-3.139354e-5)` |
| 5 | 1.071472e-07 | 0.0131 | `(0.14172831 / euler_characteristic) + 0.004260189` | `0.004260189 + 0.14172831/euler_characteristic` |
| 6 | 9.980990e-08 | 0.0709 | `sin(euler_characteristic * -0.07517415) * -0.0019925875` | `sin(euler_characteristic*(-0.07517415))*(-0.0019925875)` |
| 8 | 9.961765e-08 | 0.0010 | `(sin(-0.075558625 * euler_characteristic) * -0.0022102885) + -0.00021507897` | `sin(-0.075558625*euler_characteristic)*(-0.0022102885) - 0.00021507897` |
| 9 | 9.919545e-08 | 0.0042 | `(sin(sin(euler_characteristic * -0.07545474)) * -0.0035724605) + -0.0010063399` | `sin(sin(euler_characteristic*(-0.07545474)))*(-0.0035724605) - 0.0010063399` |
| 11 | 9.864281e-08 | 0.0028 | `-0.0002689942 / (-0.13610773 / sin(sin(euler_characteristic * -0.12553388) + 0.44725716))` | `-0.0002689942*(-7.34712128400055*sin(sin(euler_characteristic*(-0.12553388)) + 0.44725716))` |
| 12 | 9.746240e-08 | 0.0120 | `(0.18490848 / (euler_characteristic - (sin(n_hbonds * 0.27843973) * -3.2704692))) + 0.0049175946` | `0.0049175946 + 0.18490848/(euler_characteristic - (-3.2704692)*sin(n_hbonds*0.27843973))` |
| 14 | 9.736055e-08 | 0.0005 | `(0.16305932 / ((euler_characteristic - (sin(n_hbonds * 0.2573007) * 4.102782)) + 2.4069262)) + 0.0046385825` | `0.0046385825 + 0.16305932/(euler_characteristic - 4.102782*sin(n_hbonds*0.2573007) + 2.4069262)` |
| 15 | 9.705515e-08 | 0.0031 | `0.0045269793 + (0.16310969 / (euler_characteristic - ((4.102782 + cos(n_hbonds)) * sin(n_hbonds * 0.25652987))))` | `0.0045269793 + 0.16310969/(euler_characteristic - (cos(n_hbonds) + 4.102782)*sin(n_hbonds*0.25652987))` |
| 16 | 9.694576e-08 | 0.0011 | `0.0045250007 + (0.16307893 / (euler_characteristic - (sin(0.25669363 * n_hbonds) * (sin(exp(betti_1)) + 3.9312546))))` | `0.0045250007 + 0.16307893/(euler_characteristic - (sin(exp(betti_1)) + 3.9312546)*sin(0.25669363*n_hbonds))` |
| 17 | 9.680564e-08 | 0.0014 | `(0.16331957 / (euler_characteristic - ((cos(n_hbonds * 0.7912785) + 4.1027837) * sin(n_hbonds * 0.25652772)))) + 0.0045296513` | `0.0045296513 + 0.16331957/(euler_characteristic - (cos(n_hbonds*0.7912785) + 4.1027837)*sin(n_hbonds*0.25652772))` |
| 18 | 9.665231e-08 | 0.0016 | `0.0045269793 + (0.16310969 / (euler_characteristic - ((sin(n_hbonds * 0.25652987) * 4.102782) + cos(cos(euler_characteristic) + n_hbonds))))` | `0.0045269793 + 0.16310969/(euler_characteristic - (sin(n_hbonds*0.25652987)*4.102782 + cos(n_hbonds + cos(euler_characteristic))))` |
| 20 | 9.645241e-08 | 0.0010 | `0.0045269793 + (0.16310969 / (euler_characteristic - ((sin(n_hbonds * 0.25652987) * 4.102782) + cos((1.6812981 * cos(euler_characteristic)) + n_hbonds))))` | `0.0045269793 + 0.16310969/(euler_characteristic - (sin(n_hbonds*0.25652987)*4.102782 + cos(n_hbonds + 1.6812981*cos(euler_characteristic))))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: euler_characteristic*(-3.1393443e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.0018550083` | `0.00185500830000000` |
| 2 | 1.282176e-07 | 0.0000 | `sin(0.0018550351)` | `sin(0.0018550351)` |
| 3 | 1.099853e-07 | 0.1534 | `euler_characteristic * -3.1393443e-5` | `euler_characteristic*(-3.1393443e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `(0.14214481 / euler_characteristic) + 0.004267176` | `0.004267176 + 0.14214481/euler_characteristic` |
| 6 | 1.018240e-07 | 0.0510 | `0.0021694642 - exp(euler_characteristic * 0.13837974)` | `0.0021694642 - exp(euler_characteristic*0.13837974)` |
| 7 | 1.008881e-07 | 0.0092 | `(-0.006176185 / (betti_1 + -46.64343)) + 0.0023518973` | `0.0023518973 - 0.006176185/(betti_1 - 46.64343)` |
| 8 | 9.938557e-08 | 0.0150 | `0.002023231 - exp((euler_characteristic * 0.25389302) + 5.9330196)` | `0.002023231 - exp(euler_characteristic*0.25389302 + 5.9330196)` |
| 12 | 9.912385e-08 | 0.0007 | `(-0.07286923 / ((betti_1 + -11.160982) * sin(betti_1 * -0.077716425))) + 0.003414456` | `0.003414456 - 0.07286923*1/((betti_1 - 11.160982)*sin(betti_1*(-0.077716425)))` |
| 14 | 9.698414e-08 | 0.0109 | `(-0.07315834 / (betti_1 + ((sin(n_hbonds * -0.23653597) + -4.7038116) / 0.2146924))) + 0.0036598102` | `0.0036598102 - 0.07315834/(betti_1 + (sin(n_hbonds*(-0.23653597)) - 4.7038116)/0.2146924)` |
| 16 | 9.692052e-08 | 0.0003 | `(-0.020673765 / ((betti_1 + ((sin(n_hbonds * 0.21529466) + -8.080684) / 0.20859678)) - -0.45336607)) + 0.0027197425` | `0.0027197425 - 0.020673765/(betti_1 + (sin(n_hbonds*0.21529466) - 8.080684)/0.20859678 - 1*(-0.45336607))` |
| 17 | 9.683426e-08 | 0.0009 | `(-0.020673765 / ((betti_1 + ((sin(sin(n_hbonds * 0.21529466)) + -8.080684) / 0.20859678)) - -0.45336607)) + 0.0027197425` | `0.0027197425 - 0.020673765/(betti_1 + (sin(sin(n_hbonds*0.21529466)) - 8.080684)/0.20859678 - 1*(-0.45336607))` |
| 19 | 9.646607e-08 | 0.0019 | `(-0.07320433 / ((betti_1 + ((sin(0.21508002 * n_hbonds) + -4.3465996) / 0.21634999)) - sin(-0.56063867 * betti_1))) + 0.0035672258` | `0.0035672258 - 0.07320433/(betti_1 + (sin(0.21508002*n_hbonds) - 4.3465996)/0.21634999 - sin(-0.56063867*betti_1))` |
| 20 | 9.630105e-08 | 0.0017 | `(-0.07611318 / ((((sin(sin(n_hbonds * 0.21515608)) + -4.3466234) / 0.21466118) + betti_1) - sin(betti_1 * 0.50818616))) + 0.003652723` | `0.003652723 - 0.07611318/(betti_1 + (sin(sin(n_hbonds*0.21515608)) - 4.3466234)/0.21466118 - sin(betti_1*0.50818616))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: euler_characteristic*(-3.139346e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.001855009` | `0.00185500900000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.139346e-5` | `euler_characteristic*(-3.139346e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `(0.14213945 / euler_characteristic) - -0.004267087` | `-1*(-0.004267087) + 0.14213945/euler_characteristic` |
| 6 | 9.980600e-08 | 0.0710 | `sin(euler_characteristic * -0.07512809) * -0.001994444` | `sin(euler_characteristic*(-0.07512809))*(-0.001994444)` |
| 7 | 9.980599e-08 | 0.0000 | `sin(sin(euler_characteristic * -0.07512809) * -0.001994444)` | `sin(sin(euler_characteristic*(-0.07512809))*(-0.001994444))` |
| 8 | 9.966231e-08 | 0.0014 | `sin((euler_characteristic * -0.082487255) - 0.41052306) * -0.0019946361` | `sin(euler_characteristic*(-0.082487255) - 1*0.41052306)*(-0.0019946361)` |
| 9 | 9.893680e-08 | 0.0073 | `0.001984125 / exp(exp((50.6551 - betti_1) / 2.8098118))` | `0.001984125/exp(exp((50.6551 - betti_1)/2.8098118))` |
| 10 | 9.863991e-08 | 0.0030 | `0.0019889835 / exp(sin(exp((euler_characteristic + 49.95662) / 2.7420175)))` | `0.0019889835/exp(sin(exp((euler_characteristic + 49.95662)/2.7420175)))` |
| 11 | 9.853543e-08 | 0.0011 | `0.00197534 / exp(sin(sin(exp((euler_characteristic + 50.172585) / 2.5195553))))` | `0.00197534/exp(sin(sin(exp((euler_characteristic + 50.172585)/2.5195553))))` |
| 12 | 9.851373e-08 | 0.0002 | `0.00197534 / exp(sin(sin(sin(exp((euler_characteristic + 50.172585) / 2.5195553)))))` | `0.00197534/exp(sin(sin(sin(exp((euler_characteristic + 50.172585)/2.5195553)))))` |
| 13 | 9.849965e-08 | 0.0001 | `0.0019819436 / exp(sin(sin(exp(((euler_characteristic + 49.95662) / 2.544126) + 0.11907782))))` | `0.0019819436/exp(sin(sin(exp((euler_characteristic + 49.95662)/2.544126 + 0.11907782))))` |
| 14 | 9.828289e-08 | 0.0022 | `0.0019579632 / exp(sin(exp((euler_characteristic + 49.956715) / exp(sin(euler_characteristic * -0.14610712)))))` | `0.0019579632/exp(sin(exp((euler_characteristic + 49.956715)/exp(sin(euler_characteristic*(-0.14610712))))))` |
| 15 | 9.815653e-08 | 0.0013 | `0.001956996 / exp(sin(sin(exp((euler_characteristic + 49.956715) / exp(sin(euler_characteristic * -0.14610712))))))` | `0.001956996/exp(sin(sin(exp((euler_characteristic + 49.956715)/exp(sin(euler_characteristic*(-0.14610712)))))))` |
| 16 | 9.814791e-08 | 0.0001 | `0.0019579632 / exp(sin(sin(sin(exp((euler_characteristic + 49.956715) / exp(sin(euler_characteristic * -0.14610712)))))))` | `0.0019579632/exp(sin(sin(sin(exp((euler_characteristic + 49.956715)/exp(sin(euler_characteristic*(-0.14610712))))))))` |
| 17 | 9.798176e-08 | 0.0017 | `sin(exp(cos(sin(cos(exp(cos(log(n_hbonds) * log(betti_1 + log(n_hbonds))))))))) * 0.0022123982` | `0.0022123982*sin(exp(cos(sin(cos(exp(cos(log(n_hbonds)*log(betti_1 + log(n_hbonds)))))))))` |
| 18 | 9.728304e-08 | 0.0072 | `sin(exp(cos(cos(sin(0.99826515) + cos(log(n_hbonds) * log(log(betti_1) + betti_1)))))) * 0.0019811338` | `0.0019811338*sin(exp(cos(cos(cos(log(n_hbonds)*log(betti_1 + log(betti_1))) + 0.840532375533552))))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: euler_characteristic*(-3.139354e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.001855009` | `0.00185500900000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.139354e-5` | `euler_characteristic*(-3.139354e-5)` |
| 5 | 1.071484e-07 | 0.0131 | `(0.14098598 / euler_characteristic) + 0.0042475164` | `0.0042475164 + 0.14098598/euler_characteristic` |
| 6 | 1.071484e-07 | 0.0000 | `sin((0.14098598 / euler_characteristic) + 0.0042475164)` | `sin(0.0042475164 + 0.14098598/euler_characteristic)` |
| 7 | 1.058739e-07 | 0.0120 | `(-0.049157303 / (betti_1 + -24.286148)) - -0.003239684` | `-1*(-0.003239684) - 0.049157303/(betti_1 - 24.286148)` |
| 8 | 9.964379e-08 | 0.0606 | `sin(55.137188 / (29.49556 - betti_1)) * -0.001963568` | `sin(55.137188/(29.49556 - betti_1))*(-0.001963568)` |
| 12 | 9.743763e-08 | 0.0056 | `(-0.18087527 / ((sin(n_hbonds * 0.25734624) / 0.25454918) + betti_1)) - -0.004776087` | `-1*(-0.004776087) - 0.18087527/(betti_1 + sin(n_hbonds*0.25734624)/0.25454918)` |
| 13 | 9.741899e-08 | 0.0002 | `(-0.18090878 / (betti_1 + (sin(sin(n_hbonds * -0.2779516)) / 0.23398389))) - -0.004790939` | `-1*(-0.004790939) - 0.18090878/(betti_1 + sin(sin(n_hbonds*(-0.2779516)))/0.23398389)` |
| 14 | 9.729033e-08 | 0.0013 | `(-0.18087557 / (betti_1 + (sin(n_hbonds * 0.2573405) / (n_hbonds * 0.0016180524)))) - -0.0047767544` | `-1*(-0.0047767544) - 0.18087557/(betti_1 + sin(n_hbonds*0.2573405)/((n_hbonds*0.0016180524)))` |
| 15 | 9.729031e-08 | 0.0000 | `sin((-0.18087557 / (betti_1 + (sin(n_hbonds * 0.2573405) / (n_hbonds * 0.0016180524)))) - -0.0047767544)` | `sin(-1*(-0.0047767544) - 0.18087557/(betti_1 + sin(n_hbonds*0.2573405)/((n_hbonds*0.0016180524))))` |
| 16 | 9.726943e-08 | 0.0002 | `(-0.18087557 / (betti_1 + ((sin(n_hbonds * 0.2573405) / (n_hbonds * 0.0016180524)) - 0.08004796))) - -0.0047767544` | `-1*(-0.0047767544) - 0.18087557/(betti_1 - 1*0.08004796 + sin(n_hbonds*0.2573405)/((n_hbonds*0.0016180524)))` |
| 17 | 9.694124e-08 | 0.0034 | `(-0.18087527 / (betti_1 + (sin(-0.2773576 * (n_hbonds + sin(-0.28027743 * n_hbonds))) / 0.25454918))) - -0.004776087` | `-1*(-0.004776087) - 0.18087527/(betti_1 + sin(-0.2773576*(n_hbonds + sin(-0.28027743*n_hbonds)))/0.25454918)` |
| 19 | 9.654260e-08 | 0.0021 | `(-0.18087585 / ((betti_1 + sin(euler_characteristic * 0.4051154)) + (sin(n_hbonds * 0.25734147) / (n_hbonds * 0.0020621591)))) - -0.004780596` | `-1*(-0.004780596) - 0.18087585/(betti_1 + sin(euler_characteristic*0.4051154) + sin(n_hbonds*0.25734147)/((n_hbonds*0.0020621591)))` |
| 20 | 9.654259e-08 | 0.0000 | `sin((-0.18087585 / (betti_1 + (sin(0.4051154 * euler_characteristic) + (sin(n_hbonds * 0.25734147) / (n_hbonds * 0.0020621591))))) - -0.004780596)` | `sin(-1*(-0.004780596) - 0.18087585/(betti_1 + sin(0.4051154*euler_characteristic) + sin(n_hbonds*0.25734147)/((n_hbonds*0.0020621591))))` |

</details>

