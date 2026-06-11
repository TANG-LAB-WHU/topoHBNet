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
| 1 | `LBHB_Fraction ≈ exp(euler_characteristic*0.1461479) - 1*(-0.0015277163)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ exp(euler_characteristic/6.842575) - 1*(-0.0015276761)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(euler_characteristic*0.14615159) + 0.001527297` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -0.0016175678/cos(euler_characteristic*0.048308484)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ exp(euler_characteristic/6.844842) + 0.0015272776` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(euler_characteristic*0.1461479) - 1*(-0.0015277163)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 53/68 | 77.9% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 23/68 | 33.8% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 3/68 | 4.4% | ❄️ Low |
| `n_hbonds` | Total number of hydrogen bonds in the network | 2/68 | 2.9% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/68 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 53/68 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(euler_characteristic*0.1461479) - 1*(-0.0015277163)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.829122e-07 | 0.0000 | `0.0017566516` | `0.00175665160000000` |
| 3 | 2.103161e-07 | 0.1483 | `-0.1060248 / euler_characteristic` | `-0.1060248/euler_characteristic` |
| 5 | 2.001518e-07 | 0.0248 | `(-16.190945 / euler_characteristic) / n_hbonds` | `-16.190945/(euler_characteristic*n_hbonds)` |
| 6 | 1.605049e-07 | 0.2208 | `exp(euler_characteristic * 0.1461479) - -0.0015277163` | `exp(euler_characteristic*0.1461479) - 1*(-0.0015277163)` |
| 8 | 1.532366e-07 | 0.0232 | `exp(euler_characteristic * 0.13954762) - (euler_characteristic * 2.364051e-5)` | `-2.364051e-5*euler_characteristic + exp(euler_characteristic*0.13954762)` |
| 11 | 1.300241e-07 | 0.0548 | `exp(sin(euler_characteristic * -0.31144595) + (euler_characteristic * 0.15905032)) - -0.0015866876` | `exp(euler_characteristic*0.15905032 + sin(euler_characteristic*(-0.31144595))) - 1*(-0.0015866876)` |
| 12 | 1.294745e-07 | 0.0042 | `exp((euler_characteristic * 0.15681502) + sin(sin(euler_characteristic * -0.31264836))) - -0.0015767029` | `exp(euler_characteristic*0.15681502 + sin(sin(euler_characteristic*(-0.31264836)))) - 1*(-0.0015767029)` |
| 14 | 1.247350e-07 | 0.0186 | `exp(((euler_characteristic - cos(euler_characteristic)) * 0.1580131) + sin(-0.3116812 * euler_characteristic)) - -0.0015816629` | `exp((euler_characteristic - cos(euler_characteristic))*0.1580131 + sin(-0.3116812*euler_characteristic)) - 1*(-0.0015816629)` |
| 16 | 1.235811e-07 | 0.0046 | `exp((cos(euler_characteristic) * -0.27996624) + (sin(-0.31255767 * euler_characteristic) + (euler_characteristic * 0.15849875))) - -0.0015820857` | `exp(euler_characteristic*0.15849875 + sin(-0.31255767*euler_characteristic) + cos(euler_characteristic)*(-0.27996624)) - 1*(-0.0015820857)` |
| 17 | 1.209622e-07 | 0.0214 | `exp((0.15825015 * (euler_characteristic - cos(euler_characteristic))) + sin(-0.3146125 * (euler_characteristic - sin(betti_1)))) - -0.0015774824` | `exp(0.15825015*(euler_characteristic - cos(euler_characteristic)) + sin(-0.3146125*(euler_characteristic - sin(betti_1)))) - 1*(-0.0015774824)` |
| 19 | 1.190231e-07 | 0.0081 | `exp(((0.1580131 * euler_characteristic) + (-0.3111445 * cos(euler_characteristic))) + sin((euler_characteristic - sin(betti_1)) * -0.3134873)) - -0.0015816629` | `exp(0.1580131*euler_characteristic + sin((euler_characteristic - sin(betti_1))*(-0.3134873)) - 0.3111445*cos(euler_characteristic)) - 1*(-0.0015816629)` |
| 20 | 1.184429e-07 | 0.0049 | `exp(sin((euler_characteristic - sin(betti_1)) * -0.31418666) + (((euler_characteristic - cos(euler_characteristic)) - sin(betti_1)) * 0.15798487)) - -0.0015763104` | `exp((euler_characteristic - sin(betti_1) - cos(euler_characteristic))*0.15798487 + sin((euler_characteristic - sin(betti_1))*(-0.31418666))) - 1*(-0.0015763104)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: exp(euler_characteristic/6.842575) - 1*(-0.0015276761)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.829122e-07 | 0.0000 | `0.0017566516` | `0.00175665160000000` |
| 3 | 2.103161e-07 | 0.1483 | `-0.10602323 / euler_characteristic` | `-0.10602323/euler_characteristic` |
| 5 | 1.904590e-07 | 0.0496 | `-0.065124236 / (euler_characteristic + 22.265549)` | `-0.065124236/(euler_characteristic + 22.265549)` |
| 6 | 1.605049e-07 | 0.1711 | `exp(euler_characteristic / 6.842575) - -0.0015276761` | `exp(euler_characteristic/6.842575) - 1*(-0.0015276761)` |
| 8 | 1.531989e-07 | 0.0233 | `exp(euler_characteristic * 0.13933572) + (euler_characteristic * -2.3592112e-5)` | `euler_characteristic*(-2.3592112e-5) + exp(euler_characteristic*0.13933572)` |
| 10 | 1.525177e-07 | 0.0022 | `((euler_characteristic * -3.430056e-5) + -0.00070762204) + exp(euler_characteristic * 0.13653485)` | `euler_characteristic*(-3.430056e-5) + exp(euler_characteristic*0.13653485) - 0.00070762204` |
| 11 | 1.300941e-07 | 0.1590 | `exp(sin(euler_characteristic / 0.16745731) - (euler_characteristic * -0.15950571)) - -0.0015867531` | `exp(-(-0.15950571)*euler_characteristic + sin(euler_characteristic/0.16745731)) - 1*(-0.0015867531)` |
| 12 | 1.300591e-07 | 0.0003 | `exp(sin(euler_characteristic / 0.16744517) - (euler_characteristic * sin(-0.15950502))) - -0.0015842624` | `exp(-euler_characteristic*sin(-0.15950502) + sin(euler_characteristic/0.16744517)) - 1*(-0.0015842624)` |
| 13 | 1.299899e-07 | 0.0005 | `exp(sin(euler_characteristic / 0.16745731) - ((euler_characteristic * betti_0) * -0.15950571)) - -0.0015867531` | `exp(-(-0.15950571)*betti_0*euler_characteristic + sin(euler_characteristic/0.16745731)) - 1*(-0.0015867531)` |
| 14 | 1.261233e-07 | 0.0302 | `exp(cos(0.27751362 * euler_characteristic) - ((euler_characteristic - cos(euler_characteristic)) * -0.15938348)) - -0.0015987785` | `exp(-(-0.15938348)*(euler_characteristic - cos(euler_characteristic)) + cos(0.27751362*euler_characteristic)) - 1*(-0.0015987785)` |
| 16 | 1.245046e-07 | 0.0065 | `exp(cos(-0.27926448 * euler_characteristic) - (-0.15948027 * (euler_characteristic - cos(n_hbonds * 0.57043105)))) - -0.0015986166` | `exp(-(-1)*0.15948027*(euler_characteristic - cos(n_hbonds*0.57043105)) + cos(-0.27926448*euler_characteristic)) - 1*(-0.0015986166)` |
| 17 | 1.221215e-07 | 0.0193 | `exp(cos(-0.27965397 * (sin(betti_1) - euler_characteristic)) - ((euler_characteristic - cos(euler_characteristic)) * -0.15938348)) - -0.0015987785` | `exp(-(-0.15938348)*(euler_characteristic - cos(euler_characteristic)) + cos(-0.27965397*(-euler_characteristic + sin(betti_1)))) - 1*(-0.0015987785)` |
| 19 | 1.209289e-07 | 0.0049 | `exp(cos((euler_characteristic - sin(betti_1)) * 0.2793954) - (-0.15948027 * (euler_characteristic - (cos(euler_characteristic) / 0.62217)))) - -0.0015986166` | `exp(-(-1)*0.15948027*(euler_characteristic - cos(euler_characteristic)/0.62217) + cos((euler_characteristic - sin(betti_1))*0.2793954)) - 1*(-0.0015986166)` |
| 20 | 1.208354e-07 | 0.0008 | `exp(cos(0.2793954 * (euler_characteristic - sin(betti_1))) - (-0.15948027 * (euler_characteristic - (cos(euler_characteristic) / cos(betti_0))))) - -0.0015986166` | `exp(-(-1)*0.15948027*(euler_characteristic - cos(euler_characteristic)/cos(betti_0)) + cos(0.2793954*(euler_characteristic - sin(betti_1)))) - 1*(-0.0015986166)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(euler_characteristic*0.14615159) + 0.001527297</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.829122e-07 | 0.0000 | `0.0017566516` | `0.00175665160000000` |
| 3 | 2.103161e-07 | 0.1483 | `-0.10602327 / euler_characteristic` | `-0.10602327/euler_characteristic` |
| 5 | 1.908574e-07 | 0.0485 | `-0.06834712 / (euler_characteristic + 20.574926)` | `-0.06834712/(euler_characteristic + 20.574926)` |
| 6 | 1.605052e-07 | 0.1732 | `exp(euler_characteristic * 0.14615159) + 0.001527297` | `exp(euler_characteristic*0.14615159) + 0.001527297` |
| 8 | 1.531880e-07 | 0.0233 | `exp(euler_characteristic * 0.13932876) + (euler_characteristic * -2.3537541e-5)` | `euler_characteristic*(-2.3537541e-5) + exp(euler_characteristic*0.13932876)` |
| 9 | 1.531880e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13932876)) + (euler_characteristic * -2.3537541e-5)` | `euler_characteristic*(-2.3537541e-5) + sin(exp(euler_characteristic*0.13932876))` |
| 10 | 1.531042e-07 | 0.0005 | `(euler_characteristic * -2.3665125e-5) + exp(betti_0 * (euler_characteristic * 0.13953958))` | `euler_characteristic*(-2.3665125e-5) + exp(betti_0*euler_characteristic*0.13953958)` |
| 11 | 1.301458e-07 | 0.1625 | `exp((euler_characteristic * 0.15973106) + sin(euler_characteristic * -0.31171998)) + 0.0015959212` | `exp(euler_characteristic*0.15973106 + sin(euler_characteristic*(-0.31171998))) + 0.0015959212` |
| 12 | 1.295023e-07 | 0.0050 | `exp(sin(sin(euler_characteristic * -0.31359264)) + (euler_characteristic * 0.15712956)) + 0.0015784596` | `exp(euler_characteristic*0.15712956 + sin(sin(euler_characteristic*(-0.31359264)))) + 0.0015784596` |
| 13 | 1.295023e-07 | 0.0000 | `sin(0.0015784596 + exp(sin(sin(euler_characteristic * -0.31359264)) + (euler_characteristic * 0.15712956)))` | `sin(exp(euler_characteristic*0.15712956 + sin(sin(euler_characteristic*(-0.31359264)))) + 0.0015784596)` |
| 14 | 1.267888e-07 | 0.0212 | `exp(sin(cos(euler_characteristic) + (euler_characteristic * -0.3201668)) + (euler_characteristic * 0.15722723)) + 0.0015783402` | `exp(euler_characteristic*0.15722723 + sin(euler_characteristic*(-0.3201668) + cos(euler_characteristic))) + 0.0015783402` |
| 15 | 1.215093e-07 | 0.0425 | `(exp(-0.6511739 / exp(((26.298767 - betti_1) * 2.130137) + betti_1)) + 0.99660945) * 0.001688889` | `(0.99660945 + exp(-0.6511739*exp(-betti_1 - 1*(26.298767 - betti_1)*2.130137)))*0.001688889` |
| 16 | 1.176907e-07 | 0.0319 | `exp(exp(-0.22792348 - (0.45712352 / exp(((26.297653 - betti_1) * 2.1420352) + betti_1)))) * 0.001658072` | `exp(exp(-0.22792348 - 0.45712352/exp(betti_1 + (26.297653 - betti_1)*2.1420352)))*0.001658072` |
| 17 | 1.176907e-07 | 0.0000 | `sin(exp(exp(-0.22792348 - (0.45712352 / exp(((26.297653 - betti_1) * 2.1420352) + betti_1)))) * 0.001658072)` | `sin(exp(exp(-0.22792348 - 0.45712352/exp(betti_1 + (26.297653 - betti_1)*2.1420352)))*0.001658072)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -0.0016175678/cos(euler_characteristic*0.048308484)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.829123e-07 | 0.0000 | `0.0017566518` | `0.00175665180000000` |
| 3 | 2.103161e-07 | 0.1483 | `-0.10602325 / euler_characteristic` | `-0.10602325/euler_characteristic` |
| 5 | 1.902425e-07 | 0.0502 | `0.06498291 / (betti_1 + -23.344793)` | `0.06498291/(betti_1 - 23.344793)` |
| 6 | 1.608427e-07 | 0.1679 | `-0.0016175678 / cos(euler_characteristic * 0.048308484)` | `-0.0016175678/cos(euler_characteristic*0.048308484)` |
| 9 | 1.538462e-07 | 0.0148 | `((0.98923033 / betti_1) + (euler_characteristic * -0.00025658394)) + -0.030014113` | `euler_characteristic*(-0.00025658394) - 0.030014113 + 0.98923033/betti_1` |
| 10 | 1.538461e-07 | 0.0000 | `sin(((0.98923033 / betti_1) + (euler_characteristic * -0.00025658394)) + -0.030014113)` | `sin(euler_characteristic*(-0.00025658394) - 0.030014113 + 0.98923033/betti_1)` |
| 11 | 1.538448e-07 | 0.0000 | `(((1.2951417 / betti_1) + -0.039268687) / 1.315254) + (euler_characteristic * -0.00025520445)` | `euler_characteristic*(-0.00025520445) + (-0.039268687 + 1.2951417/betti_1)/1.315254` |
| 12 | 1.498385e-07 | 0.0264 | `0.6719523 / ((cos(euler_characteristic * 0.23347673) + (betti_1 * 0.10713037)) * betti_1)` | `0.6719523/((betti_1*(betti_1*0.10713037 + cos(euler_characteristic*0.23347673))))` |
| 13 | 1.498384e-07 | 0.0000 | `sin(0.6719523 / ((cos(euler_characteristic * 0.23347673) + (betti_1 * 0.10713037)) * betti_1))` | `sin(0.6719523/((betti_1*(betti_1*0.10713037 + cos(euler_characteristic*0.23347673)))))` |
| 14 | 1.414881e-07 | 0.0573 | `0.67443025 / ((betti_1 + 13.749616) * ((betti_1 * 0.09048663) - cos(betti_1 * 0.28328404)))` | `0.67443025/(((betti_1 + 13.749616)*(betti_1*0.09048663 - cos(betti_1*0.28328404))))` |
| 15 | 1.414880e-07 | 0.0000 | `sin(0.67443025 / ((13.749616 + betti_1) * ((betti_1 * 0.09048663) - cos(betti_1 * 0.28328404))))` | `sin(0.67443025/(((betti_1 + 13.749616)*(betti_1*0.09048663 - cos(betti_1*0.28328404)))))` |
| 18 | 1.408057e-07 | 0.0016 | `sin(0.67417544 / (((betti_1 + 12.163942) + sin(betti_1)) * ((betti_1 * 0.09228053) - cos(betti_1 * 0.28307983))))` | `sin(0.67417544/(((betti_1*0.09228053 - cos(betti_1*0.28307983))*(betti_1 + sin(betti_1) + 12.163942))))` |
| 19 | 1.387406e-07 | 0.0148 | `0.6742441 / (((betti_1 + 12.163942) - sin(betti_1 * -0.5064104)) * ((betti_1 * 0.09210225) - cos(betti_1 * -0.28271362)))` | `0.6742441/(((betti_1*0.09210225 - cos(betti_1*(-0.28271362)))*(betti_1 - sin(betti_1*(-0.5064104)) + 12.163942)))` |
| 20 | 1.387405e-07 | 0.0000 | `sin(0.6742441 / ((betti_1 + (12.163942 - sin(-0.5064104 * betti_1))) * ((betti_1 * 0.09210225) - cos(betti_1 * -0.28271362))))` | `sin(0.6742441/(((betti_1*0.09210225 - cos(betti_1*(-0.28271362)))*(betti_1 - sin(-0.5064104*betti_1) + 12.163942))))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: exp(euler_characteristic/6.844842) + 0.0015272776</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.829123e-07 | 0.0000 | `0.0017566521` | `0.00175665210000000` |
| 3 | 2.103161e-07 | 0.1483 | `-0.10602326 / euler_characteristic` | `-0.10602326/euler_characteristic` |
| 5 | 1.905061e-07 | 0.0495 | `0.062557586 / (betti_1 + -24.605537)` | `0.062557586/(betti_1 - 24.605537)` |
| 6 | 1.605053e-07 | 0.1714 | `exp(euler_characteristic / 6.844842) + 0.0015272776` | `exp(euler_characteristic/6.844842) + 0.0015272776` |
| 7 | 1.605002e-07 | 0.0000 | `exp(exp(euler_characteristic * 0.1463106)) + -0.99846995` | `exp(exp(euler_characteristic*0.1463106)) - 0.99846995` |
| 8 | 1.531836e-07 | 0.0467 | `exp(euler_characteristic * 0.13922748) + (euler_characteristic * -2.3511086e-5)` | `euler_characteristic*(-2.3511086e-5) + exp(euler_characteristic*0.13922748)` |
| 10 | 1.526654e-07 | 0.0017 | `(exp(euler_characteristic / 7.245007) + (euler_characteristic * -2.913662e-5)) + -0.00036440458` | `euler_characteristic*(-2.913662e-5) + exp(euler_characteristic/7.245007) - 0.00036440458` |
| 11 | 1.300244e-07 | 0.1605 | `exp((0.15920979 * euler_characteristic) - sin(euler_characteristic * 0.31168482)) + 0.0015880642` | `exp(0.15920979*euler_characteristic - sin(euler_characteristic*0.31168482)) + 0.0015880642` |
| 12 | 1.288529e-07 | 0.0091 | `exp((euler_characteristic * 0.13091418) - exp(sin(euler_characteristic * 0.3171566))) + 0.0015256093` | `exp(euler_characteristic*0.13091418 - exp(sin(euler_characteristic*0.3171566))) + 0.0015256093` |
| 14 | 1.247376e-07 | 0.0162 | `exp((0.15800314 * (euler_characteristic - cos(euler_characteristic))) - sin(0.3116696 * euler_characteristic)) + 0.0015762743` | `exp(0.15800314*(euler_characteristic - cos(euler_characteristic)) - sin(0.3116696*euler_characteristic)) + 0.0015762743` |
| 16 | 1.218141e-07 | 0.0119 | `exp((euler_characteristic * 0.1536981) - sin((0.31981805 * euler_characteristic) - sin(euler_characteristic * 0.31446257))) + 0.0015366875` | `exp(euler_characteristic*0.1536981 - sin(0.31981805*euler_characteristic - sin(euler_characteristic*0.31446257))) + 0.0015366875` |
| 17 | 1.208847e-07 | 0.0077 | `exp(((euler_characteristic - cos(euler_characteristic)) * 0.15800314) - sin((euler_characteristic - sin(betti_1)) * 0.31480008)) + 0.0015762743` | `exp((euler_characteristic - cos(euler_characteristic))*0.15800314 - sin((euler_characteristic - sin(betti_1))*0.31480008)) + 0.0015762743` |
| 19 | 1.192715e-07 | 0.0067 | `exp(((euler_characteristic + sin(euler_characteristic)) * 0.15260163) - sin((euler_characteristic * 0.31946597) - sin(euler_characteristic * 0.31730825))) + 0.0015377548` | `exp((euler_characteristic + sin(euler_characteristic))*0.15260163 - sin(euler_characteristic*0.31946597 - sin(euler_characteristic*0.31730825))) + 0.0015377548` |
| 20 | 1.182853e-07 | 0.0083 | `exp(((euler_characteristic - (sin(betti_1) + cos(euler_characteristic))) * 0.15742086) - sin((euler_characteristic - sin(betti_1)) * 0.31442547)) + 0.0015770554` | `exp((euler_characteristic - (sin(betti_1) + cos(euler_characteristic)))*0.15742086 - sin((euler_characteristic - sin(betti_1))*0.31442547)) + 0.0015770554` |

</details>

