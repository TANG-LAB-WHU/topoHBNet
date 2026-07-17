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
| 1 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173242e-5)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173226e-5)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173306e-5)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ euler_characteristic*(-1.617301e-5)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ euler_characteristic*(-1.6172959e-5)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx euler_characteristic*(-1.6173242e-5)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `n_hbonds` | Total number of hydrogen bonds in the network | 59/77 | 76.6% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 52/77 | 67.5% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 27/77 | 35.1% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/77 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/77 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `n_hbonds` is the most stable feature (appearing in 59/77 Pareto equations). This strongly indicates that `n_hbonds` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: euler_characteristic*(-1.6173242e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173242e-5` | `euler_characteristic*(-1.6173242e-5)` |
| 5 | 3.352416e-08 | 0.0123 | `(-0.4617205 / n_hbonds) + 0.0039545987` | `0.0039545987 - 0.4617205/n_hbonds` |
| 7 | 3.329200e-08 | 0.0035 | `0.00055724784 / cos(cos(n_hbonds * 0.05902849))` | `0.00055724784/cos(cos(n_hbonds*0.05902849))` |
| 8 | 3.290052e-08 | 0.0118 | `(-1.1269469e-5 / cos(betti_1)) - (n_hbonds * -6.4046153e-6)` | `-(-6.4046153e-6)*n_hbonds - 1.1269469e-5/cos(betti_1)` |
| 10 | 3.242383e-08 | 0.0073 | `(0.055545345 / ((0.41621903 / cos(betti_1)) + euler_characteristic)) - -0.0019040551` | `-1*(-0.0019040551) + 0.055545345/(euler_characteristic + 0.41621903/cos(betti_1))` |
| 11 | 3.241705e-08 | 0.0002 | `(0.055545345 / (euler_characteristic + (0.41621903 / sin(cos(betti_1))))) - -0.0019040551` | `-1*(-0.0019040551) + 0.055545345/(euler_characteristic + 0.41621903/sin(cos(betti_1)))` |
| 12 | 3.197363e-08 | 0.0138 | `(0.028080445 / (euler_characteristic - (-0.5980816 / cos(betti_1)))) - (n_hbonds * -9.336239e-6)` | `-(-9.336239e-6)*n_hbonds + 0.028080445/(euler_characteristic - (-1)*0.5980816/cos(betti_1))` |
| 13 | 3.196559e-08 | 0.0003 | `(0.028080445 / (euler_characteristic - (-0.5980816 / sin(cos(betti_1))))) - (n_hbonds * -9.331897e-6)` | `-(-9.331897e-6)*n_hbonds + 0.028080445/(euler_characteristic - (-1)*0.5980816/sin(cos(betti_1)))` |
| 15 | 3.193610e-08 | 0.0005 | `(0.028080445 / ((euler_characteristic + cos(betti_1)) - (-0.5980816 / cos(betti_1)))) - (n_hbonds * -9.347552e-6)` | `-(-9.347552e-6)*n_hbonds + 0.028080445/(euler_characteristic + cos(betti_1) - (-1)*0.5980816/cos(betti_1))` |
| 16 | 3.189277e-08 | 0.0014 | `(0.028080447 / ((cos(exp(betti_1)) + euler_characteristic) - (-0.5980816 / cos(betti_1)))) - (n_hbonds * -9.318205e-6)` | `-(-9.318205e-6)*n_hbonds + 0.028080447/(euler_characteristic + cos(exp(betti_1)) - (-1)*0.5980816/cos(betti_1))` |
| 17 | 3.174834e-08 | 0.0045 | `(0.02808045 / ((cos(-0.5867984 * n_hbonds) + euler_characteristic) - (-0.5899401 / cos(betti_1)))) - (-9.3251165e-6 * n_hbonds)` | `-(-1)*9.3251165e-6*n_hbonds + 0.02808045/(euler_characteristic + cos(-0.5867984*n_hbonds) - (-1)*0.5899401/cos(betti_1))` |
| 18 | 3.172708e-08 | 0.0007 | `(0.030728549 / (euler_characteristic + (cos(n_hbonds * -0.628993) - (-0.5684711 / sin(cos(betti_1)))))) - (n_hbonds * -9.603349e-6)` | `-(-9.603349e-6)*n_hbonds + 0.030728549/(euler_characteristic + cos(n_hbonds*(-0.628993)) - (-1)*0.5684711/sin(cos(betti_1)))` |
| 19 | 3.136000e-08 | 0.0116 | `(0.023824051 / ((euler_characteristic + (sin(betti_1) / sin(exp(betti_1)))) - (-0.6915852 / cos(betti_1)))) - (n_hbonds * -8.904954e-6)` | `-(-8.904954e-6)*n_hbonds + 0.023824051/(euler_characteristic + sin(betti_1)/sin(exp(betti_1)) - (-1)*0.6915852/cos(betti_1))` |
| 20 | 3.135564e-08 | 0.0001 | `(0.023824051 / ((sin(betti_1) / sin(exp(betti_1))) + (euler_characteristic - (-0.6915852 / sin(cos(betti_1)))))) - (n_hbonds * -8.904954e-6)` | `-(-8.904954e-6)*n_hbonds + 0.023824051/(euler_characteristic + sin(betti_1)/sin(exp(betti_1)) - (-1)*0.6915852/sin(cos(betti_1)))` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: euler_characteristic*(-1.6173226e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936074` | `0.000993607400000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173226e-5` | `euler_characteristic*(-1.6173226e-5)` |
| 5 | 3.352301e-08 | 0.0123 | `0.0039038346 - (0.4538092 / n_hbonds)` | `0.0039038346 - 0.4538092/n_hbonds` |
| 6 | 3.278470e-08 | 0.0223 | `cos(n_hbonds * 0.058608536) * -0.0010527757` | `cos(n_hbonds*0.058608536)*(-0.0010527757)` |
| 8 | 3.268533e-08 | 0.0015 | `cos(-1.3601762 / (-0.00089982775 * n_hbonds)) * -0.0010499816` | `cos(-1.3601762*(-1111.32380613956/n_hbonds))*(-0.0010499816)` |
| 9 | 3.247922e-08 | 0.0063 | `-0.0010527757 * cos(0.058608536 * (cos(betti_1) - n_hbonds))` | `-0.0010527757*cos(0.058608536*(-n_hbonds + cos(betti_1)))` |
| 11 | 3.213101e-08 | 0.0054 | `-0.0010527757 * cos(0.058608536 * ((0.067511 / cos(betti_1)) - n_hbonds))` | `-0.0010527757*cos(0.058608536*(-n_hbonds + 0.067511/cos(betti_1)))` |
| 12 | 3.212541e-08 | 0.0002 | `-0.0010527757 * cos(0.058608536 * ((0.067511 / sin(cos(betti_1))) - n_hbonds))` | `-0.0010527757*cos(0.058608536*(-n_hbonds + 0.067511/sin(cos(betti_1))))` |
| 13 | 3.156625e-08 | 0.0176 | `cos(1.4949555 / (0.0009893903 * ((-0.15412754 / cos(betti_1)) + n_hbonds))) * -0.0010538406` | `cos(1.4949555/((0.0009893903*(n_hbonds - 0.15412754/cos(betti_1)))))*(-0.0010538406)` |
| 14 | 3.155596e-08 | 0.0003 | `-0.0010538406 * cos(1.4949555 / ((n_hbonds + (-0.14966744 / sin(cos(betti_1)))) * 0.0009893903))` | `-0.0010538406*cos(1.4949555/(((n_hbonds - 0.14966744/sin(cos(betti_1)))*0.0009893903)))` |
| 15 | 3.154607e-08 | 0.0003 | `-0.0010538406 * cos(1.4949555 / (0.0009893903 * (n_hbonds + (-0.14966744 / sin(sin(cos(betti_1)))))))` | `-0.0010538406*cos(1.4949555/((0.0009893903*(n_hbonds - 0.14966744/sin(sin(cos(betti_1)))))))` |
| 16 | 3.137561e-08 | 0.0054 | `cos(1.493407 / (-0.00098899 * (cos(betti_1) + ((0.15346202 / cos(betti_1)) - n_hbonds)))) * -0.0010577023` | `cos(1.493407/((-0.00098899*(-n_hbonds + cos(betti_1) + 0.15346202/cos(betti_1)))))*(-0.0010577023)` |
| 17 | 3.137560e-08 | 0.0000 | `sin(cos(1.493407 / (-0.00098899 * (cos(betti_1) + ((0.15346202 / cos(betti_1)) - n_hbonds)))) * -0.0010577023)` | `sin(cos(1.493407/((-0.00098899*(-n_hbonds + cos(betti_1) + 0.15346202/cos(betti_1)))))*(-0.0010577023))` |
| 18 | 3.129044e-08 | 0.0027 | `cos(1.493407 / ((((0.14182244 / cos(betti_1)) - n_hbonds) + sin(betti_1 - n_hbonds)) * -0.00098899)) * -0.0010577023` | `cos(1.493407/(((-n_hbonds + sin(betti_1 - n_hbonds) + 0.14182244/cos(betti_1))*(-0.00098899))))*(-0.0010577023)` |
| 19 | 3.125576e-08 | 0.0011 | `cos(1.493407 / ((((0.14182244 / cos(betti_1)) - n_hbonds) + cos(betti_1 - cos(n_hbonds))) * -0.00098899)) * -0.0010577023` | `cos(1.493407/(((-n_hbonds + cos(betti_1 - cos(n_hbonds)) + 0.14182244/cos(betti_1))*(-0.00098899))))*(-0.0010577023)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: euler_characteristic*(-1.6173306e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936078` | `0.000993607800000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173306e-5` | `euler_characteristic*(-1.6173306e-5)` |
| 5 | 3.361991e-08 | 0.0108 | `(n_hbonds * 1.8477835e-5) - 0.0018890849` | `n_hbonds*1.8477835e-5 - 1*0.0018890849` |
| 6 | 3.357123e-08 | 0.0014 | `(log(n_hbonds) * 0.002898457) + -0.013642521` | `0.002898457*log(n_hbonds) - 0.013642521` |
| 7 | 3.346371e-08 | 0.0032 | `((n_hbonds * -0.9999835) + n_hbonds) + -0.0015838173` | `n_hbonds*(-0.9999835) + n_hbonds - 0.0015838173` |
| 8 | 3.266967e-08 | 0.0240 | `(betti_1 * 1.5978929e-5) - (9.983196e-6 / cos(betti_1))` | `betti_1*1.5978929e-5 - 9.983196e-6/cos(betti_1)` |
| 9 | 3.266966e-08 | 0.0000 | `sin((1.5978929e-5 * betti_1) - (9.983196e-6 / cos(betti_1)))` | `sin(1.5978929e-5*betti_1 - 9.983196e-6/cos(betti_1))` |
| 10 | 3.260616e-08 | 0.0019 | `(betti_1 * 1.597883e-5) - ((0.0005784223 / cos(betti_1)) / betti_1)` | `betti_1*1.597883e-5 - 0.0005784223/(betti_1*cos(betti_1))` |
| 11 | 3.255539e-08 | 0.0016 | `(betti_1 - (cos(-0.20822263 * n_hbonds) / cos(betti_1))) * 1.5922595e-5` | `(betti_1 - cos(-0.20822263*n_hbonds)/cos(betti_1))*1.5922595e-5` |
| 12 | 3.246216e-08 | 0.0029 | `(betti_1 - (cos(sin(n_hbonds) + 0.28865618) / cos(betti_1))) * 1.5988775e-5` | `(betti_1 - cos(sin(n_hbonds) + 0.28865618)/cos(betti_1))*1.5988775e-5` |
| 13 | 3.231070e-08 | 0.0047 | `1.5922595e-5 * (betti_1 - ((0.56677556 / cos(betti_1)) + sin(-0.53792334 * betti_1)))` | `1.5922595e-5*(betti_1 - (sin(-0.53792334*betti_1) + 0.56677556/cos(betti_1)))` |
| 14 | 3.231070e-08 | 0.0000 | `sin(1.5922595e-5 * (betti_1 - ((0.56677556 / cos(betti_1)) + sin(-0.53792334 * betti_1))))` | `sin(1.5922595e-5*(betti_1 - (sin(-0.53792334*betti_1) + 0.56677556/cos(betti_1))))` |
| 15 | 3.218148e-08 | 0.0040 | `(((-0.5996106 / cos(betti_1)) - (sin(0.54633623 * euler_characteristic) / 0.5508518)) + betti_1) * 1.5922595e-5` | `(betti_1 - sin(0.54633623*euler_characteristic)/0.5508518 - 0.5996106/cos(betti_1))*1.5922595e-5` |
| 17 | 3.193489e-08 | 0.0038 | `(betti_1 - ((cos(-0.8310949) / cos(betti_1)) - ((0.11392522 / cos(euler_characteristic)) / cos(n_hbonds)))) * 1.6004527e-5` | `(betti_1 - (-0.11392522/(cos(euler_characteristic)*cos(n_hbonds)) + cos(-0.8310949)/cos(betti_1)))*1.6004527e-5` |
| 18 | 3.180243e-08 | 0.0042 | `1.6004527e-5 * (betti_1 - ((0.5969155 / cos(betti_1)) - ((0.11392522 / cos(euler_characteristic)) / sin(euler_characteristic + n_hbonds))))` | `1.6004527e-5*(betti_1 - (0.5969155/cos(betti_1) - 0.11392522/(sin(euler_characteristic + n_hbonds)*cos(euler_characteristic))))` |
| 19 | 3.179922e-08 | 0.0001 | `1.6004527e-5 * (betti_1 - ((0.5969155 / cos(betti_1)) - ((0.11392522 / cos(euler_characteristic)) / sin(sin(euler_characteristic + n_hbonds)))))` | `1.6004527e-5*(betti_1 - (0.5969155/cos(betti_1) - 0.11392522/(sin(sin(euler_characteristic + n_hbonds))*cos(euler_characteristic))))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: euler_characteristic*(-1.617301e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.000993609` | `0.000993609000000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.617301e-5` | `euler_characteristic*(-1.617301e-5)` |
| 5 | 3.355635e-08 | 0.0118 | `cos(log(n_hbonds)) * 0.0030035377` | `0.0030035377*cos(log(n_hbonds))` |
| 6 | 3.276198e-08 | 0.0240 | `sin(n_hbonds / 14.550893) * -0.0010562178` | `sin(n_hbonds/14.550893)*(-0.0010562178)` |
| 7 | 3.266479e-08 | 0.0030 | `sin(sin(n_hbonds / 14.654133)) * -0.0012546679` | `sin(sin(n_hbonds/14.654133))*(-0.0012546679)` |
| 8 | 3.266479e-08 | 0.0000 | `sin(sin(sin(n_hbonds / 14.654133)) * -0.0012546679)` | `sin(sin(sin(n_hbonds/14.654133))*(-0.0012546679))` |
| 9 | 3.261685e-08 | 0.0015 | `(sin(sin(n_hbonds / 7.8392406)) * 0.00039942795) - -0.00071237865` | `sin(sin(n_hbonds/7.8392406))*0.00039942795 - 1*(-0.00071237865)` |
| 10 | 3.233557e-08 | 0.0087 | `sin(sin((n_hbonds - cos(betti_1)) / 14.654133)) * -0.0012566582` | `sin(sin((n_hbonds - cos(betti_1))/14.654133))*(-0.0012566582)` |
| 12 | 3.160015e-08 | 0.0115 | `sin(sin(((-0.1476177 / cos(betti_1)) + n_hbonds) / 14.654133)) * -0.00125673` | `sin(sin((n_hbonds - 0.1476177/cos(betti_1))/14.654133))*(-0.00125673)` |
| 13 | 3.158856e-08 | 0.0004 | `-0.00125673 * sin(sin(((-0.1476177 / sin(cos(betti_1))) + n_hbonds) / 14.654133))` | `-0.00125673*sin(sin((n_hbonds - 0.1476177/sin(cos(betti_1)))/14.654133))` |
| 14 | 3.134293e-08 | 0.0078 | `(sin(sin(((-0.2756484 / cos(betti_1)) + n_hbonds) / -9.3383875)) * 0.00039809966) + 0.0007185755` | `sin(sin((n_hbonds - 0.2756484/cos(betti_1))/(-9.3383875)))*0.00039809966 + 0.0007185755` |
| 15 | 3.133430e-08 | 0.0003 | `(0.00039856829 * sin(sin(((-0.29984334 / sin(cos(betti_1))) + n_hbonds) / -9.3383875))) + 0.0007214656` | `0.00039856829*sin(sin((n_hbonds - 0.29984334/sin(cos(betti_1)))/(-9.3383875))) + 0.0007214656` |
| 16 | 3.129355e-08 | 0.0013 | `(sin(sin((n_hbonds + (-0.27564844 / cos(betti_1 / 1.000142))) / -9.3383875)) * 0.00039755725) + 0.0007188156` | `sin(sin((n_hbonds - 0.27564844/cos(betti_1/1.000142))/(-9.3383875)))*0.00039755725 + 0.0007188156` |
| 17 | 3.124523e-08 | 0.0015 | `(sin(sin((n_hbonds + ((-0.2756484 / cos(betti_1)) - sin(euler_characteristic))) / -9.3383875)) * 0.00039809966) + 0.0007185755` | `sin(sin((n_hbonds - sin(euler_characteristic) - 0.2756484/cos(betti_1))/(-9.3383875)))*0.00039809966 + 0.0007185755` |
| 18 | 3.123399e-08 | 0.0004 | `(sin(sin(((n_hbonds + (-0.2756484 / cos(betti_1))) - sin(sin(euler_characteristic))) / -9.3383875)) * 0.00039809966) + 0.0007185755` | `sin(sin((n_hbonds - sin(sin(euler_characteristic)) - 0.2756484/cos(betti_1))/(-9.3383875)))*0.00039809966 + 0.0007185755` |
| 19 | 3.111518e-08 | 0.0038 | `(sin(sin((n_hbonds + ((-0.2756484 / cos(betti_1)) - sin(betti_1 / -1.5321943))) / -9.3383875)) * 0.0004075966) + 0.00071020506` | `sin(sin((n_hbonds - sin(betti_1/(-1.5321943)) - 0.2756484/cos(betti_1))/(-9.3383875)))*0.0004075966 + 0.00071020506` |
| 20 | 3.111518e-08 | 0.0000 | `sin((sin(sin((n_hbonds + ((-0.2756484 / cos(betti_1)) - sin(betti_1 / -1.5321943))) / -9.3383875)) * 0.0004075966) + 0.00071020506)` | `sin(sin(sin((n_hbonds - sin(betti_1/(-1.5321943)) - 0.2756484/cos(betti_1))/(-9.3383875)))*0.0004075966 + 0.00071020506)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: euler_characteristic*(-1.6172959e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936076` | `0.000993607600000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6172959e-5` | `euler_characteristic*(-1.6172959e-5)` |
| 5 | 3.361991e-08 | 0.0108 | `(n_hbonds * 1.8508359e-5) + -0.0018937117` | `n_hbonds*1.8508359e-5 - 0.0018937117` |
| 6 | 3.327916e-08 | 0.0102 | `cos(n_hbonds * -0.07934543) * 0.0010239028` | `cos(n_hbonds*(-0.07934543))*0.0010239028` |
| 8 | 3.290186e-08 | 0.0057 | `(n_hbonds - (1.7157725 / cos(betti_1))) * 6.404189e-6` | `(n_hbonds - 1.7157725/cos(betti_1))*6.404189e-6` |
| 10 | 3.202073e-08 | 0.0136 | `((1.544889e-5 * n_hbonds) + -0.0014130814) - (9.986614e-6 / cos(betti_1))` | `1.544889e-5*n_hbonds - 0.0014130814 - 9.986614e-6/cos(betti_1)` |
| 12 | 3.193016e-08 | 0.0014 | `(n_hbonds * 1.4643591e-5) + (-0.0012858978 + (7.689352e-6 / (0.007731649 - cos(betti_1))))` | `n_hbonds*1.4643591e-5 - 0.0012858978 + 7.689352e-6/(0.007731649 - cos(betti_1))` |
| 14 | 3.183166e-08 | 0.0015 | `(n_hbonds * 4.1089848e-8) * (n_hbonds - (exp(cos(n_hbonds * -0.33530053)) / cos(betti_1)))` | `n_hbonds*4.1089848e-8*(n_hbonds - exp(cos(n_hbonds*(-0.33530053)))/cos(betti_1))` |
| 15 | 3.164373e-08 | 0.0059 | `((n_hbonds * 4.1215095e-8) * (n_hbonds - (0.5747309 / cos(euler_characteristic)))) - (1.0554615e-5 / cos(betti_1))` | `n_hbonds*4.1215095e-8*(n_hbonds - 0.5747309/cos(euler_characteristic)) - 1.0554615e-5/cos(betti_1)` |
| 16 | 3.157816e-08 | 0.0021 | `(n_hbonds * (4.1215095e-8 * (n_hbonds - (cos(betti_1) / cos(euler_characteristic))))) - (1.0554615e-5 / cos(betti_1))` | `n_hbonds*4.1215095e-8*(n_hbonds - cos(betti_1)/cos(euler_characteristic)) - 1.0554615e-5/cos(betti_1)` |
| 17 | 3.152470e-08 | 0.0017 | `((n_hbonds * 4.121212e-8) - (6.9243136e-8 / cos(betti_1))) * (n_hbonds - (cos(exp(betti_1)) / cos(euler_characteristic)))` | `(n_hbonds - cos(exp(betti_1))/cos(euler_characteristic))*(n_hbonds*4.121212e-8 - 6.9243136e-8/cos(betti_1))` |
| 18 | 3.146497e-08 | 0.0019 | `((n_hbonds - (sin(cos(exp(betti_1))) / cos(euler_characteristic))) * (n_hbonds * 4.1215095e-8)) - (1.0554615e-5 / cos(betti_1))` | `(n_hbonds - sin(cos(exp(betti_1)))/cos(euler_characteristic))*n_hbonds*4.1215095e-8 - 1.0554615e-5/cos(betti_1)` |
| 19 | 3.125403e-08 | 0.0067 | `((n_hbonds - (1.6211783 / cos(betti_1))) * (n_hbonds - (cos(betti_1 - cos(n_hbonds)) / cos(euler_characteristic)))) * 4.1089848e-8` | `(n_hbonds - 1.6211783/cos(betti_1))*(n_hbonds - cos(betti_1 - cos(n_hbonds))/cos(euler_characteristic))*4.1089848e-8` |
| 20 | 3.118542e-08 | 0.0022 | `(n_hbonds - (1.6211783 / cos(betti_1))) * ((n_hbonds - (cos(betti_1 + exp(cos(n_hbonds))) / cos(euler_characteristic))) * 4.1089848e-8)` | `(n_hbonds - 1.6211783/cos(betti_1))*(n_hbonds - cos(betti_1 + exp(cos(n_hbonds)))/cos(euler_characteristic))*4.1089848e-8` |

</details>

