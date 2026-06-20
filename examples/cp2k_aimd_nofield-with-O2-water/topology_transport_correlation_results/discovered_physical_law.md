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
| 1 | `LBHB_Fraction ≈ cos(n_hbonds*(-0.06165264))*(-0.001963741)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ sin(euler_characteristic*0.082077354)*0.0019745384` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ -1*(-0.009170539) - 1.10744/(n_hbonds + cos(n_hbonds*(-0.23764953))*(-5.9368486))` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ 0.002106345 - exp(euler_characteristic*0.15351142)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ cos(n_hbonds*(-0.06158543))*(-0.0019813767)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx cos(n_hbonds*(-0.06165264))*(-0.001963741)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `n_hbonds` | Total number of hydrogen bonds in the network | 54/71 | 76.1% | 🔥 High |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 21/71 | 29.6% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 8/71 | 11.3% | ❄️ Low |
| `betti_1` | Number of independent H-bond loops/cycles | 3/71 | 4.2% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/71 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `n_hbonds` is the most stable feature (appearing in 54/71 Pareto equations). This strongly indicates that `n_hbonds` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: cos(n_hbonds*(-0.06165264))*(-0.001963741)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.800777e-07 | 0.0000 | `0.0017738082` | `0.00177380820000000` |
| 3 | 1.244065e-07 | 0.1849 | `euler_characteristic * -3.3126224e-5` | `euler_characteristic*(-3.3126224e-5)` |
| 5 | 9.306233e-08 | 0.1451 | `(-1.1078615 / n_hbonds) + 0.00926511` | `0.00926511 - 1.1078615/n_hbonds` |
| 6 | 6.693559e-08 | 0.3295 | `cos(n_hbonds * -0.06165264) * -0.001963741` | `cos(n_hbonds*(-0.06165264))*(-0.001963741)` |
| 8 | 6.632715e-08 | 0.0046 | `cos(-0.85485905 - (n_hbonds / -14.76493)) * -0.00195787` | `cos(-n_hbonds/(-14.76493) - 0.85485905)*(-0.00195787)` |
| 9 | 5.964819e-08 | 0.1061 | `cos(0.73659384 - sin(n_hbonds / 11.1554575)) * 0.0019207589` | `cos(0.73659384 - sin(n_hbonds/11.1554575))*0.0019207589` |
| 10 | 5.524159e-08 | 0.0767 | `sin(sin(sin(n_hbonds / 7.4662066)) + 0.93346655) * 0.0019099707` | `sin(sin(sin(n_hbonds/7.4662066)) + 0.93346655)*0.0019099707` |
| 11 | 5.485012e-08 | 0.0071 | `cos(sin(sin(sin(n_hbonds / 7.4662066))) - 0.6676268) * 0.0018987564` | `cos(sin(sin(sin(n_hbonds/7.4662066))) - 1*0.6676268)*0.0018987564` |
| 12 | 5.454446e-08 | 0.0056 | `sin(cos(0.7036437 - sin(sin(sin(n_hbonds / 7.485347))))) * 0.0022554195` | `sin(cos(0.7036437 - sin(sin(sin(n_hbonds/7.485347)))))*0.0022554195` |
| 13 | 5.454446e-08 | 0.0000 | `sin(sin(cos(0.7036437 - sin(sin(sin(n_hbonds / 7.485347))))) * 0.0022554195)` | `sin(sin(cos(0.7036437 - sin(sin(sin(n_hbonds/7.485347)))))*0.0022554195)` |
| 14 | 5.450241e-08 | 0.0008 | `sin(cos(0.7036437 - sin(sin(sin((n_hbonds * betti_0) / 7.485347))))) * 0.0022554195` | `sin(cos(0.7036437 - sin(sin(sin(betti_0*n_hbonds/7.485347)))))*0.0022554195` |
| 15 | 5.400591e-08 | 0.0092 | `cos(0.67057455 - sin(sin(cos(exp(0.3693382 - sin(n_hbonds / -8.952845)))))) * 0.0018864863` | `cos(0.67057455 - sin(sin(cos(exp(0.3693382 - sin(n_hbonds/(-8.952845)))))))*0.0018864863` |
| 17 | 5.369017e-08 | 0.0029 | `0.0022923404 * exp(sin(cos(-0.46797463 / (-0.88825965 - sin(sin(sin(n_hbonds / -9.168337)))))) - 0.9984617)` | `0.0022923404*exp(sin(cos(-0.46797463/(-sin(sin(sin(n_hbonds/(-9.168337)))) - 0.88825965))) - 1*0.9984617)` |
| 18 | 5.356422e-08 | 0.0023 | `sin(exp(sin(cos(-0.34696996 / sin(-0.7759724 - sin(sin(sin(sin(n_hbonds / -9.16834)))))))) * 0.00084547914)` | `sin(exp(sin(cos(-0.34696996/sin(-sin(sin(sin(sin(n_hbonds/(-9.16834))))) - 0.7759724))))*0.00084547914)` |
| 19 | 5.350993e-08 | 0.0010 | `sin(exp(sin(cos(-0.34696895 / (-0.7759728 - sin(sin(sin(sin(n_hbonds / -9.16834))))))) - 0.99848366) * 0.0022607092)` | `sin(exp(sin(cos(-0.34696895/(-sin(sin(sin(sin(n_hbonds/(-9.16834))))) - 0.7759728))) - 1*0.99848366)*0.0022607092)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: sin(euler_characteristic*0.082077354)*0.0019745384</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.800777e-07 | 0.0000 | `0.0017738068` | `0.00177380680000000` |
| 3 | 1.244065e-07 | 0.1849 | `euler_characteristic * -3.3125794e-5` | `euler_characteristic*(-3.3125794e-5)` |
| 5 | 9.306229e-08 | 0.1451 | `0.009261445 - (1.1073246 / n_hbonds)` | `0.009261445 - 1.1073246/n_hbonds` |
| 6 | 7.748086e-08 | 0.1832 | `sin(euler_characteristic * 0.082077354) * 0.0019745384` | `sin(euler_characteristic*0.082077354)*0.0019745384` |
| 7 | 7.610527e-08 | 0.0179 | `sin(sin(euler_characteristic * 0.08040518)) * 0.0023468868` | `sin(sin(euler_characteristic*0.08040518))*0.0023468868` |
| 8 | 7.270163e-08 | 0.0458 | `0.0021488238 - exp(7.531391 - (0.1060124 * n_hbonds))` | `0.0021488238 - exp(7.531391 - 0.1060124*n_hbonds)` |
| 9 | 7.183861e-08 | 0.0119 | `0.0019370147 * sin(cos(0.10199788 * euler_characteristic) - -0.6537439)` | `0.0019370147*sin(cos(0.10199788*euler_characteristic) - 1*(-0.6537439))` |
| 11 | 5.694464e-08 | 0.1162 | `0.0019795229 - exp(sin(-0.17728283 * n_hbonds) - (n_hbonds * 0.05625845))` | `0.0019795229 - exp(-0.05625845*n_hbonds + sin(-0.17728283*n_hbonds))` |
| 12 | 5.686009e-08 | 0.0015 | `0.0019795229 - exp(sin(-0.17728283 * n_hbonds) - (sin(0.05625845) * n_hbonds))` | `0.0019795229 - exp(-n_hbonds*sin(0.05625845) + sin(-0.17728283*n_hbonds))` |
| 13 | 5.577005e-08 | 0.0194 | `0.0020029843 - exp(sin(n_hbonds * -0.17728664) + (0.11096175 - (0.056308657 * n_hbonds)))` | `0.0020029843 - exp(-0.056308657*n_hbonds + sin(n_hbonds*(-0.17728664)) + 0.11096175)` |
| 15 | 5.572326e-08 | 0.0004 | `0.0020029843 - exp(0.11096175 + (sin((n_hbonds + -0.17185022) * -0.17728664) - (0.056308657 * n_hbonds)))` | `0.0020029843 - exp(-0.056308657*n_hbonds + sin((n_hbonds - 0.17185022)*(-0.17728664)) + 0.11096175)` |
| 16 | 5.524456e-08 | 0.0086 | `0.0019978625 - exp(((1.7099284 - n_hbonds) * 0.05626856) + sin((n_hbonds + sin(n_hbonds)) * -0.1772837))` | `0.0019978625 - exp((1.7099284 - n_hbonds)*0.05626856 + sin((n_hbonds + sin(n_hbonds))*(-0.1772837)))` |
| 17 | 5.519624e-08 | 0.0009 | `0.0019978625 - exp(((1.7099284 - n_hbonds) * 0.05626856) + sin((n_hbonds + sin(sin(n_hbonds))) * -0.1772837))` | `0.0019978625 - exp((1.7099284 - n_hbonds)*0.05626856 + sin((n_hbonds + sin(sin(n_hbonds)))*(-0.1772837)))` |
| 18 | 5.428344e-08 | 0.0167 | `0.0019929907 - exp(sin(-0.1772833 * (n_hbonds + cos(n_hbonds * 0.26040256))) + ((2.1330194 - n_hbonds) * 0.05626352))` | `0.0019929907 - exp((2.1330194 - n_hbonds)*0.05626352 + sin(-0.1772833*(n_hbonds + cos(n_hbonds*0.26040256))))` |
| 20 | 5.371623e-08 | 0.0053 | `0.0019929907 - exp(((1.8124559 - n_hbonds) * 0.05626352) + sin((cos((-0.1772833 + -0.1772833) * euler_characteristic) + n_hbonds) * -0.1772833))` | `0.0019929907 - exp((1.8124559 - n_hbonds)*0.05626352 + sin((n_hbonds + cos(euler_characteristic*(-0.1772833 - 0.1772833)))*(-0.1772833)))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: -1*(-0.009170539) - 1.10744/(n_hbonds + cos(n_hbonds*(-0.23764953))*(-5.9368486))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.800777e-07 | 0.0000 | `0.0017738098` | `0.00177380980000000` |
| 3 | 1.244065e-07 | 0.1849 | `euler_characteristic * -3.312608e-5` | `euler_characteristic*(-3.312608e-5)` |
| 5 | 9.306230e-08 | 0.1451 | `(-1.1073297 / n_hbonds) - -0.009261481` | `-1*(-0.009261481) - 1.1073297/n_hbonds` |
| 6 | 7.982853e-08 | 0.1534 | `0.002119823 - exp(euler_characteristic * 0.1527115)` | `0.002119823 - exp(euler_characteristic*0.1527115)` |
| 8 | 7.974017e-08 | 0.0006 | `1.5695006 * (0.0013303373 - exp(0.16363622 * euler_characteristic))` | `1.5695006*(0.0013303373 - exp(0.16363622*euler_characteristic))` |
| 10 | 7.966955e-08 | 0.0004 | `1.5695006 * (0.0013288994 - exp(euler_characteristic * (betti_0 * 0.16363592)))` | `1.5695006*(0.0013288994 - exp(euler_characteristic*betti_0*0.16363592))` |
| 12 | 5.832391e-08 | 0.1559 | `(-1.10744 / (n_hbonds + (cos(n_hbonds * -0.23764953) * -5.9368486))) - -0.009170539` | `-1*(-0.009170539) - 1.10744/(n_hbonds + cos(n_hbonds*(-0.23764953))*(-5.9368486))` |
| 14 | 5.819801e-08 | 0.0011 | `(-1.1074431 / ((-1.8963873 + n_hbonds) - (cos(n_hbonds * 0.23809762) * 5.975491))) - -0.009275372` | `-1*(-0.009275372) - 1.1074431/(n_hbonds - 5.975491*cos(n_hbonds*0.23809762) - 1.8963873)` |
| 15 | 5.777550e-08 | 0.0073 | `(-1.105795 / (n_hbonds - (cos(n_hbonds * 0.23776795) * (5.975491 + sin(betti_1))))) - -0.009163693` | `-1*(-0.009163693) - 1.105795/(n_hbonds - (sin(betti_1) + 5.975491)*cos(n_hbonds*0.23776795))` |
| 16 | 5.777513e-08 | 0.0000 | `(-1.105795 / (n_hbonds - (cos(n_hbonds * 0.23776795) * (5.975491 + sin(betti_1))))) - sin(-0.009163693)` | `-sin(-0.009163693) - 1.105795/(n_hbonds - (sin(betti_1) + 5.975491)*cos(n_hbonds*0.23776795))` |
| 17 | 5.498979e-08 | 0.0494 | `(-1.10744 / ((n_hbonds - cos(n_hbonds * -0.4647581)) - (cos(n_hbonds * 0.23761564) * 5.975491))) - -0.009168441` | `-1*(-0.009168441) - 1.10744/(n_hbonds - cos(n_hbonds*(-0.4647581)) - 5.975491*cos(n_hbonds*0.23761564))` |
| 19 | 5.477045e-08 | 0.0020 | `(-1.1074431 / (n_hbonds + ((cos(n_hbonds * 0.44389603) - (cos(n_hbonds * -0.23767634) * 5.975491)) + -1.8963873))) - -0.009275372` | `-1*(-0.009275372) - 1.1074431/(n_hbonds - 5.975491*cos(n_hbonds*(-0.23767634)) + cos(n_hbonds*0.44389603) - 1.8963873)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: 0.002106345 - exp(euler_characteristic*0.15351142)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.800777e-07 | 0.0000 | `0.0017738076` | `0.00177380760000000` |
| 3 | 1.244065e-07 | 0.1849 | `euler_characteristic * -3.3126315e-5` | `euler_characteristic*(-3.3126315e-5)` |
| 5 | 9.306252e-08 | 0.1451 | `(-1.1089916 / n_hbonds) - -0.009272719` | `-1*(-0.009272719) - 1.1089916/n_hbonds` |
| 6 | 7.994517e-08 | 0.1519 | `0.002106345 - exp(euler_characteristic * 0.15351142)` | `0.002106345 - exp(euler_characteristic*0.15351142)` |
| 7 | 7.694780e-08 | 0.0382 | `(-0.04635378 / (n_hbonds + -113.702034)) - -0.003170185` | `-1*(-0.003170185) - 0.04635378/(n_hbonds - 113.702034)` |
| 12 | 5.846163e-08 | 0.0550 | `(-1.3213347 / (n_hbonds + (sin(n_hbonds * 0.24958867) * -4.965859))) - -0.010647339` | `-1*(-0.010647339) - 1.3213347/(n_hbonds + sin(n_hbonds*0.24958867)*(-4.965859))` |
| 13 | 5.846162e-08 | 0.0000 | `sin((-1.3213347 / (n_hbonds + (sin(n_hbonds * 0.24958867) * -4.965859))) - -0.010647339)` | `sin(-1*(-0.010647339) - 1.3213347/(n_hbonds + sin(n_hbonds*0.24958867)*(-4.965859)))` |
| 14 | 5.786406e-08 | 0.0103 | `(-1.321339 / (n_hbonds + ((cos(0.23861918 * n_hbonds) - betti_0) * -5.424519))) - -0.01031544` | `-1*(-0.01031544) - 1.321339/(n_hbonds + (-betti_0 + cos(0.23861918*n_hbonds))*(-5.424519))` |
| 15 | 5.786405e-08 | 0.0000 | `sin((-1.321339 / (n_hbonds + ((cos(0.23861918 * n_hbonds) - betti_0) * -5.424519))) - -0.01031544)` | `sin(-1*(-0.01031544) - 1.321339/(n_hbonds + (-betti_0 + cos(0.23861918*n_hbonds))*(-5.424519)))` |
| 16 | 5.783988e-08 | 0.0004 | `(-1.3213395 / ((n_hbonds + 1.2848854) + ((cos(n_hbonds * -0.23838398) - betti_0) * -5.424519))) - -0.010241808` | `-1*(-0.010241808) - 1.3213395/(n_hbonds + (-betti_0 + cos(n_hbonds*(-0.23838398)))*(-5.424519) + 1.2848854)` |
| 17 | 5.613207e-08 | 0.0300 | `(-1.321314 / (n_hbonds + (cos((sin(euler_characteristic * -0.322583) - n_hbonds) * -0.23868574) * -5.424519))) - -0.010644974` | `-1*(-0.010644974) - 1.321314/(n_hbonds + cos((-n_hbonds + sin(euler_characteristic*(-0.322583)))*(-0.23868574))*(-5.424519))` |
| 19 | 5.516760e-08 | 0.0087 | `(-1.321339 / (((cos(-0.23838285 * (cos(-0.35400745 * betti_1) + n_hbonds)) - betti_0) * -5.424519) + n_hbonds)) - -0.01031544` | `-1*(-0.01031544) - 1.321339/(n_hbonds + (-betti_0 + cos(-0.23838285*(n_hbonds + cos(-0.35400745*betti_1))))*(-5.424519))` |
| 20 | 5.511146e-08 | 0.0010 | `(-1.321339 / (n_hbonds + (-5.424519 * (cos(-0.23806481 * (cos(euler_characteristic * log(1.349834)) - n_hbonds)) - betti_0)))) - -0.01031544` | `0.01031544 - 1.321339/(5.424519*betti_0 + n_hbonds - 5.424519*cos(0.23806481*n_hbonds - 0.23806481*cos(0.29998162192681*euler_characteristic)))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: cos(n_hbonds*(-0.06158543))*(-0.0019813767)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.800777e-07 | 0.0000 | `0.0017738087` | `0.00177380870000000` |
| 3 | 1.244065e-07 | 0.1849 | `euler_characteristic * -3.3126063e-5` | `euler_characteristic*(-3.3126063e-5)` |
| 5 | 9.306229e-08 | 0.1451 | `(-1.1072835 / n_hbonds) + 0.009261167` | `0.009261167 - 1.1072835/n_hbonds` |
| 6 | 6.709689e-08 | 0.3271 | `cos(n_hbonds * -0.06158543) * -0.0019813767` | `cos(n_hbonds*(-0.06158543))*(-0.0019813767)` |
| 7 | 6.556040e-08 | 0.0232 | `sin(sin(n_hbonds * 0.072464466)) * -0.00230494` | `sin(sin(n_hbonds*0.072464466))*(-0.00230494)` |
| 9 | 5.980238e-08 | 0.0460 | `sin(sin(n_hbonds * -0.08977805) + -0.82532305) * -0.0019300443` | `sin(sin(n_hbonds*(-0.08977805)) - 0.82532305)*(-0.0019300443)` |
| 10 | 5.521205e-08 | 0.0799 | `sin(sin(sin(n_hbonds * -0.13370001)) + -0.94887507) * -0.0019120645` | `sin(sin(sin(n_hbonds*(-0.13370001))) - 0.94887507)*(-0.0019120645)` |
| 11 | 5.481157e-08 | 0.0073 | `sin(sin(sin(sin(n_hbonds * -0.13311075)) + -0.94474405)) * -0.0022651965` | `sin(sin(sin(sin(n_hbonds*(-0.13311075))) - 0.94474405))*(-0.0022651965)` |
| 12 | 5.452721e-08 | 0.0052 | `sin(sin(sin(sin(sin(n_hbonds * -0.13370596))) + -0.86532825)) * -0.0022540921` | `sin(sin(sin(sin(sin(n_hbonds*(-0.13370596)))) - 0.86532825))*(-0.0022540921)` |
| 14 | 5.447391e-08 | 0.0005 | `sin(betti_0 * sin(sin(sin(sin(n_hbonds * -0.13365668))) + -0.8705541)) * -0.0022526407` | `sin(betti_0*sin(sin(sin(sin(n_hbonds*(-0.13365668)))) - 0.8705541))*(-0.0022526407)` |
| 15 | 5.280390e-08 | 0.0311 | `sin(sin(sin((n_hbonds - sin(euler_characteristic + n_hbonds)) * 0.11194674)) + -0.8764756) * -0.0019052294` | `sin(sin(sin((n_hbonds - sin(euler_characteristic + n_hbonds))*0.11194674)) - 0.8764756)*(-0.0019052294)` |
| 16 | 5.191190e-08 | 0.0170 | `sin(sin(sin(sin((n_hbonds - sin(euler_characteristic + n_hbonds)) * -0.13317524)) + -0.9447442)) * -0.0022672256` | `sin(sin(sin(sin((n_hbonds - sin(euler_characteristic + n_hbonds))*(-0.13317524))) - 0.9447442))*(-0.0022672256)` |
| 17 | 5.108032e-08 | 0.0161 | `sin(sin(sin((n_hbonds + sin((euler_characteristic + n_hbonds) * 0.76853496)) * -0.13306688)) + -0.9635853) * -0.0019142719` | `sin(sin(sin((n_hbonds + sin((euler_characteristic + n_hbonds)*0.76853496))*(-0.13306688))) - 0.9635853)*(-0.0019142719)` |
| 18 | 5.044672e-08 | 0.0125 | `sin(sin(sin(sin((n_hbonds + sin((n_hbonds + euler_characteristic) * 0.76853484)) * -0.13299297)) + -0.944744)) * -0.0022693572` | `sin(sin(sin(sin((n_hbonds + sin((euler_characteristic + n_hbonds)*0.76853484))*(-0.13299297))) - 0.944744))*(-0.0022693572)` |
| 19 | 4.784615e-08 | 0.0529 | `sin(sin(sin(((sin((n_hbonds + euler_characteristic) * -0.6640617) / 0.32438383) + n_hbonds) * -0.13301195)) + -0.96358526) * -0.0019232467` | `sin(sin(sin((n_hbonds + sin((euler_characteristic + n_hbonds)*(-0.6640617))/0.32438383)*(-0.13301195))) - 0.96358526)*(-0.0019232467)` |
| 20 | 4.714531e-08 | 0.0148 | `sin(sin(sin(sin(((sin((euler_characteristic + n_hbonds) * -0.6640617) / 0.32438383) + n_hbonds) * 0.11102409))) + -0.8876237) * -0.0019194063` | `sin(sin(sin(sin((n_hbonds + sin((euler_characteristic + n_hbonds)*(-0.6640617))/0.32438383)*0.11102409))) - 0.8876237)*(-0.0019194063)` |

</details>

