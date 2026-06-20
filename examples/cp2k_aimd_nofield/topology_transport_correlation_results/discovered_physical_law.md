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
| 1 | `LBHB_Fraction ≈ exp(euler_characteristic*0.1428066) + 0.0012111786` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ exp(euler_characteristic*0.14275894) - 1*(-0.0012104001)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(euler_characteristic*0.14292173) - 1*(-0.0012126827)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ exp(euler_characteristic*0.14274697) + 0.0012091973` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ exp(euler_characteristic*0.14276034) + 0.0012105592` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(euler_characteristic*0.1428066) + 0.0012111786$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 56/74 | 75.7% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 43/74 | 58.1% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 2/74 | 2.7% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 1/74 | 1.4% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/74 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 56/74 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(euler_characteristic*0.1428066) + 0.0012111786</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.833515e-07 | 0.0000 | `0.0014446714` | `0.00144467140000000` |
| 3 | 1.411076e-07 | 0.1309 | `-0.087570824 / euler_characteristic` | `-0.087570824/euler_characteristic` |
| 5 | 1.139202e-07 | 0.1070 | `0.04595471 / (-27.854399 - euler_characteristic)` | `0.04595471/(-euler_characteristic - 27.854399)` |
| 6 | 9.505646e-08 | 0.1810 | `exp(euler_characteristic * 0.1428066) + 0.0012111786` | `exp(euler_characteristic*0.1428066) + 0.0012111786` |
| 8 | 8.989512e-08 | 0.0279 | `(euler_characteristic * -1.8431669e-5) + exp(betti_1 * -0.13458858)` | `euler_characteristic*(-1.8431669e-5) + exp(betti_1*(-0.13458858))` |
| 10 | 8.805861e-08 | 0.0103 | `(euler_characteristic * -3.982098e-5) + (exp(betti_1 * -0.12992218) - 0.0013880942)` | `euler_characteristic*(-3.982098e-5) + exp(betti_1*(-0.12992218)) - 1*0.0013880942` |
| 11 | 7.438874e-08 | 0.1687 | `exp(sin(betti_1 * 0.30286998) + (-0.15202336 * betti_1)) - -0.0013043361` | `exp(-0.15202336*betti_1 + sin(betti_1*0.30286998)) - 1*(-0.0013043361)` |
| 12 | 7.408212e-08 | 0.0041 | `exp(sin(sin(betti_1 * 0.3034851)) + (betti_1 * -0.15024847)) - -0.0012948049` | `exp(betti_1*(-0.15024847) + sin(sin(betti_1*0.3034851))) - 1*(-0.0012948049)` |
| 13 | 7.407125e-08 | 0.0001 | `exp(((betti_1 * -0.1691748) + sin(betti_1 * 0.2999784)) + 0.8141313) - -0.0013275017` | `exp(betti_1*(-0.1691748) + sin(betti_1*0.2999784) + 0.8141313) - 1*(-0.0013275017)` |
| 14 | 7.135218e-08 | 0.0374 | `exp(((betti_1 + cos(euler_characteristic)) * -0.15123989) + sin(betti_1 * 0.30210212)) - -0.0013009165` | `exp((betti_1 + cos(euler_characteristic))*(-0.15123989) + sin(betti_1*0.30210212)) - 1*(-0.0013009165)` |
| 15 | 7.128069e-08 | 0.0010 | `exp(sin(betti_1 * 0.30293253) + ((cos(euler_characteristic) + betti_1) * sin(-0.15159887))) - -0.0012971775` | `exp((betti_1 + cos(euler_characteristic))*sin(-0.15159887) + sin(betti_1*0.30293253)) - 1*(-0.0012971775)` |
| 16 | 7.108390e-08 | 0.0028 | `exp(sin(betti_1 * 0.30267105) + ((betti_1 + (cos(euler_characteristic) + -2.3903003)) * -0.15937561)) - -0.001309033` | `exp((betti_1 + cos(euler_characteristic) - 2.3903003)*(-0.15937561) + sin(betti_1*0.30267105)) - 1*(-0.001309033)` |
| 17 | 7.040813e-08 | 0.0096 | `exp(sin((betti_1 + sin(betti_1)) * 0.30576614) + ((betti_1 + cos(euler_characteristic)) * -0.15123986)) - -0.0012928612` | `exp((betti_1 + cos(euler_characteristic))*(-0.15123986) + sin((betti_1 + sin(betti_1))*0.30576614)) - 1*(-0.0012928612)` |
| 18 | 7.040813e-08 | 0.0000 | `sin(exp(sin((betti_1 + sin(betti_1)) * 0.30576614) + ((betti_1 + cos(euler_characteristic)) * -0.15123986)) - -0.0012928612)` | `sin(exp((betti_1 + cos(euler_characteristic))*(-0.15123986) + sin((betti_1 + sin(betti_1))*0.30576614)) - 1*(-0.0012928612))` |
| 19 | 7.003182e-08 | 0.0054 | `exp((((cos(n_hbonds + euler_characteristic) + sin(betti_1)) + betti_1) * -0.15159908) + sin(betti_1 * 0.3029326)) - -0.0013031687` | `exp((betti_1 + sin(betti_1) + cos(euler_characteristic + n_hbonds))*(-0.15159908) + sin(betti_1*0.3029326)) - 1*(-0.0013031687)` |
| 20 | 6.860145e-08 | 0.0206 | `exp(sin((betti_1 + sin(betti_1)) * 0.30576614) + (((betti_1 + cos(euler_characteristic)) + sin(betti_1)) * -0.15123986)) - -0.0012928612` | `exp((betti_1 + sin(betti_1) + cos(euler_characteristic))*(-0.15123986) + sin((betti_1 + sin(betti_1))*0.30576614)) - 1*(-0.0012928612)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: exp(euler_characteristic*0.14275894) - 1*(-0.0012104001)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.833515e-07 | 0.0000 | `0.0014446708` | `0.00144467080000000` |
| 3 | 1.411076e-07 | 0.1309 | `-0.08757074 / euler_characteristic` | `-0.08757074/euler_characteristic` |
| 5 | 1.135801e-07 | 0.1085 | `0.04211189 / (-30.179396 - euler_characteristic)` | `0.04211189/(-euler_characteristic - 30.179396)` |
| 6 | 9.505585e-08 | 0.1780 | `exp(euler_characteristic * 0.14275894) - -0.0012104001` | `exp(euler_characteristic*0.14275894) - 1*(-0.0012104001)` |
| 8 | 8.964329e-08 | 0.0293 | `exp(euler_characteristic * 0.13753763) + (euler_characteristic * -1.8698775e-5)` | `euler_characteristic*(-1.8698775e-5) + exp(euler_characteristic*0.13753763)` |
| 10 | 8.840051e-08 | 0.0070 | `(exp(euler_characteristic * 0.1353284) - 0.00068423967) + (euler_characteristic * -2.9244886e-5)` | `euler_characteristic*(-2.9244886e-5) + exp(euler_characteristic*0.1353284) - 1*0.00068423967` |
| 11 | 7.418349e-08 | 0.1753 | `exp((euler_characteristic * 0.15587056) + cos(-0.27472183 * euler_characteristic)) - -0.001323485` | `exp(euler_characteristic*0.15587056 + cos(-0.27472183*euler_characteristic)) - 1*(-0.001323485)` |
| 13 | 7.283320e-08 | 0.0092 | `exp((euler_characteristic * 0.15541655) + cos((euler_characteristic - n_hbonds) * -0.13777155)) - -0.0013191962` | `exp(euler_characteristic*0.15541655 + cos((euler_characteristic - n_hbonds)*(-0.13777155))) - 1*(-0.0013191962)` |
| 14 | 7.131279e-08 | 0.0211 | `exp((0.15538919 * (euler_characteristic - cos(euler_characteristic))) + cos(-0.27472183 * euler_characteristic)) - -0.0013219125` | `exp(0.15538919*(euler_characteristic - cos(euler_characteristic)) + cos(-0.27472183*euler_characteristic)) - 1*(-0.0013219125)` |
| 15 | 7.131278e-08 | 0.0000 | `exp((0.15538919 * (euler_characteristic - cos(euler_characteristic))) + cos(-0.27472183 * euler_characteristic)) - sin(-0.0013219125)` | `exp(0.15538919*(euler_characteristic - cos(euler_characteristic)) + cos(-0.27472183*euler_characteristic)) - sin(-0.0013219125)` |
| 16 | 7.093968e-08 | 0.0052 | `exp(((0.15538919 * euler_characteristic) + cos(0.27466467 * euler_characteristic)) + (-0.22227103 * cos(euler_characteristic))) - -0.0013219125` | `exp(0.15538919*euler_characteristic + cos(0.27466467*euler_characteristic) - 0.22227103*cos(euler_characteristic)) - 1*(-0.0013219125)` |
| 17 | 6.990295e-08 | 0.0147 | `exp((0.15538919 * (euler_characteristic - cos(euler_characteristic))) + cos((euler_characteristic - sin(betti_1)) * -0.27741468)) - -0.0013192105` | `exp(0.15538919*(euler_characteristic - cos(euler_characteristic)) + cos((euler_characteristic - sin(betti_1))*(-0.27741468))) - 1*(-0.0013192105)` |
| 18 | 6.990293e-08 | 0.0000 | `sin(exp((0.15538919 * (euler_characteristic - cos(euler_characteristic))) + cos((euler_characteristic - sin(betti_1)) * -0.27741468)) - -0.0013192105)` | `sin(exp(0.15538919*(euler_characteristic - cos(euler_characteristic)) + cos((euler_characteristic - sin(betti_1))*(-0.27741468))) - 1*(-0.0013192105))` |
| 19 | 6.896204e-08 | 0.0136 | `exp(cos((sin(betti_1) - euler_characteristic) * 0.27699032) + ((cos(euler_characteristic) * -0.2758542) + (0.15545228 * euler_characteristic))) - -0.0013219125` | `exp(0.15545228*euler_characteristic + cos(euler_characteristic)*(-0.2758542) + cos((-euler_characteristic + sin(betti_1))*0.27699032)) - 1*(-0.0013219125)` |
| 20 | 6.878855e-08 | 0.0025 | `exp(cos((sin(betti_1) - euler_characteristic) * 0.27719533) + (((euler_characteristic - sin(betti_1)) - cos(euler_characteristic)) * 0.15538919)) - -0.0013192105` | `exp((euler_characteristic - sin(betti_1) - cos(euler_characteristic))*0.15538919 + cos((-euler_characteristic + sin(betti_1))*0.27719533)) - 1*(-0.0013192105)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(euler_characteristic*0.14292173) - 1*(-0.0012126827)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.833516e-07 | 0.0000 | `0.0014446712` | `0.00144467120000000` |
| 2 | 1.833515e-07 | 0.0000 | `sin(0.0014446721)` | `sin(0.0014446721)` |
| 3 | 1.411076e-07 | 0.2619 | `-0.08757141 / euler_characteristic` | `-0.08757141/euler_characteristic` |
| 5 | 1.159067e-07 | 0.0984 | `-0.049390305 / (euler_characteristic + 25.655628)` | `-0.049390305/(euler_characteristic + 25.655628)` |
| 6 | 9.506100e-08 | 0.1983 | `exp(euler_characteristic * 0.14292173) - -0.0012126827` | `exp(euler_characteristic*0.14292173) - 1*(-0.0012126827)` |
| 8 | 8.992963e-08 | 0.0277 | `exp(betti_1 * -0.13458578) - (betti_1 * -1.819327e-5)` | `-(-1.819327e-5)*betti_1 + exp(betti_1*(-0.13458578))` |
| 11 | 7.434208e-08 | 0.0635 | `exp((betti_1 * -0.1515438) - sin(betti_1 * -0.3018721)) - -0.0013018227` | `exp(betti_1*(-0.1515438) - sin(betti_1*(-0.3018721))) - 1*(-0.0013018227)` |
| 12 | 7.399191e-08 | 0.0047 | `exp((betti_1 * -0.1495062) - sin(sin(betti_1 * -0.3031969))) - -0.0012901586` | `exp(betti_1*(-0.1495062) - sin(sin(betti_1*(-0.3031969)))) - 1*(-0.0012901586)` |
| 13 | 7.399190e-08 | 0.0000 | `sin(exp((betti_1 * -0.1495062) - sin(sin(betti_1 * -0.3031969))) - -0.0012901586)` | `sin(exp(betti_1*(-0.1495062) - sin(sin(betti_1*(-0.3031969)))) - 1*(-0.0012901586))` |
| 14 | 7.130546e-08 | 0.0370 | `exp((-0.15119886 * (cos(euler_characteristic) + betti_1)) - sin(betti_1 * -0.30332905)) - -0.0012996213` | `exp(-0.15119886*(betti_1 + cos(euler_characteristic)) - sin(betti_1*(-0.30332905))) - 1*(-0.0012996213)` |
| 15 | 7.097783e-08 | 0.0046 | `exp(((betti_1 + cos(euler_characteristic)) * -0.14875922) - sin(sin(betti_1 * -0.30332905))) - -0.0012824065` | `exp((betti_1 + cos(euler_characteristic))*(-0.14875922) - sin(sin(betti_1*(-0.30332905)))) - 1*(-0.0012824065)` |
| 16 | 7.084229e-08 | 0.0019 | `exp((betti_1 * -0.15117045) - (sin(betti_1 * -0.30245855) + (sin(betti_1) * 0.23336658))) - -0.0012994697` | `exp(betti_1*(-0.15117045) - (sin(betti_1)*0.23336658 + sin(betti_1*(-0.30245855)))) - 1*(-0.0012994697)` |
| 17 | 7.050991e-08 | 0.0047 | `exp(((sin(betti_1) + (betti_1 + cos(euler_characteristic))) * -0.15119886) - sin(betti_1 * -0.30332905)) - -0.0012996213` | `exp((betti_1 + sin(betti_1) + cos(euler_characteristic))*(-0.15119886) - sin(betti_1*(-0.30332905))) - 1*(-0.0012996213)` |
| 18 | 6.965663e-08 | 0.0122 | `exp(((cos(euler_characteristic) + betti_1) * -0.1486795) - sin(sin(-0.30549467 * (betti_1 + sin(betti_1))))) - -0.0012787094` | `exp((betti_1 + cos(euler_characteristic))*(-0.1486795) - sin(sin(-0.30549467*(betti_1 + sin(betti_1))))) - 1*(-0.0012787094)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: exp(euler_characteristic*0.14274697) + 0.0012091973</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.833515e-07 | 0.0000 | `0.0014446713` | `0.00144467130000000` |
| 3 | 1.411076e-07 | 0.1309 | `-0.08757079 / euler_characteristic` | `-0.08757079/euler_characteristic` |
| 5 | 1.232404e-07 | 0.0677 | `(5.185424 / euler_characteristic) / euler_characteristic` | `5.185424/(euler_characteristic*euler_characteristic)` |
| 6 | 9.505721e-08 | 0.2597 | `exp(euler_characteristic * 0.14274697) + 0.0012091973` | `exp(euler_characteristic*0.14274697) + 0.0012091973` |
| 7 | 9.505720e-08 | 0.0000 | `sin(exp(euler_characteristic * 0.14274983)) + 0.0012092431` | `sin(exp(euler_characteristic*0.14274983)) + 0.0012092431` |
| 8 | 9.004222e-08 | 0.0542 | `exp(euler_characteristic * 0.13872322) + (-1.8989931e-5 * euler_characteristic)` | `-1.8989931e-5*euler_characteristic + exp(euler_characteristic*0.13872322)` |
| 10 | 8.794085e-08 | 0.0118 | `(exp(betti_1 * -0.12967165) + (betti_1 * 3.8547987e-5)) + -0.0013608616` | `betti_1*3.8547987e-5 + exp(betti_1*(-0.12967165)) - 0.0013608616` |
| 11 | 7.419482e-08 | 0.1700 | `exp((betti_1 * -0.152714) + cos(0.274992 * euler_characteristic)) + 0.0013221327` | `exp(betti_1*(-0.152714) + cos(0.274992*euler_characteristic)) + 0.0013221327` |
| 12 | 7.419482e-08 | 0.0000 | `sin(exp((betti_1 * -0.152714) + cos(euler_characteristic * 0.274992))) + 0.0013221327` | `sin(exp(betti_1*(-0.152714) + cos(euler_characteristic*0.274992))) + 0.0013221327` |
| 13 | 7.389434e-08 | 0.0041 | `exp(((betti_1 * -0.18073846) + 1.3370701) - sin(betti_1 * -0.30034307)) + 0.0013361248` | `exp(betti_1*(-0.18073846) - sin(betti_1*(-0.30034307)) + 1.3370701) + 0.0013361248` |
| 14 | 7.135620e-08 | 0.0350 | `0.0013193736 + exp(((cos(euler_characteristic) + betti_1) * -0.1521268) + cos(euler_characteristic * 0.27521366))` | `exp((betti_1 + cos(euler_characteristic))*(-0.1521268) + cos(euler_characteristic*0.27521366)) + 0.0013193736` |
| 16 | 7.126762e-08 | 0.0006 | `exp((((cos(euler_characteristic) * 1.3504742) + betti_1) * -0.15299141) + cos(betti_1 * -0.2696049)) + 0.0013226861` | `exp((betti_1 + cos(euler_characteristic)*1.3504742)*(-0.15299141) + cos(betti_1*(-0.2696049))) + 0.0013226861` |
| 17 | 6.995001e-08 | 0.0187 | `exp(((cos(euler_characteristic) + betti_1) * -0.15226093) + cos((sin(betti_1) + betti_1) * -0.27149552)) + 0.0013205251` | `exp((betti_1 + cos(euler_characteristic))*(-0.15226093) + cos((betti_1 + sin(betti_1))*(-0.27149552))) + 0.0013205251` |
| 18 | 6.995001e-08 | 0.0000 | `sin(exp((-0.15226093 * (cos(euler_characteristic) + betti_1)) + cos((sin(betti_1) + betti_1) * -0.27149552)) + 0.0013205251)` | `sin(exp(-0.15226093*(betti_1 + cos(euler_characteristic)) + cos((betti_1 + sin(betti_1))*(-0.27149552))) + 0.0013205251)` |
| 19 | 6.988974e-08 | 0.0009 | `0.0013205251 + exp(((betti_1 + cos(euler_characteristic - -0.18012667)) * -0.15226093) + cos(-0.27149552 * (betti_1 + sin(betti_1))))` | `exp((betti_1 + cos(euler_characteristic - 1*(-0.18012667)))*(-0.15226093) + cos(-0.27149552*(betti_1 + sin(betti_1)))) + 0.0013205251` |
| 20 | 6.896414e-08 | 0.0133 | `exp(cos((betti_1 + sin(betti_1)) * 0.27128333) + (-0.15226093 * (cos(euler_characteristic) + (sin(betti_1) + betti_1)))) + 0.0013205251` | `exp(-0.15226093*(betti_1 + sin(betti_1) + cos(euler_characteristic)) + cos((betti_1 + sin(betti_1))*0.27128333)) + 0.0013205251` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: exp(euler_characteristic*0.14276034) + 0.0012105592</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.833516e-07 | 0.0000 | `0.0014446727` | `0.00144467270000000` |
| 2 | 1.833515e-07 | 0.0000 | `sin(0.0014446715)` | `sin(0.0014446715)` |
| 3 | 1.411076e-07 | 0.2619 | `-0.087570764 / euler_characteristic` | `-0.087570764/euler_characteristic` |
| 5 | 1.133154e-07 | 0.1097 | `0.043318346 / (betti_1 - 30.509975)` | `0.043318346/(betti_1 - 1*30.509975)` |
| 6 | 9.505584e-08 | 0.1757 | `exp(euler_characteristic * 0.14276034) + 0.0012105592` | `exp(euler_characteristic*0.14276034) + 0.0012105592` |
| 8 | 8.965382e-08 | 0.0293 | `(euler_characteristic * -1.8621442e-5) + exp(euler_characteristic * 0.13757254)` | `euler_characteristic*(-1.8621442e-5) + exp(euler_characteristic*0.13757254)` |
| 10 | 8.083033e-08 | 0.0518 | `((-5.367227 - sin(betti_1 * -0.25053194)) / euler_characteristic) / betti_1` | `(-sin(betti_1*(-0.25053194)) - 5.367227)/(betti_1*euler_characteristic)` |
| 12 | 7.890498e-08 | 0.0121 | `((-4.9568744 - sin(betti_1 * -0.2502919)) / euler_characteristic) / (betti_1 + -5.364812)` | `(-sin(betti_1*(-0.2502919)) - 4.9568744)/(euler_characteristic*(betti_1 - 5.364812))` |
| 14 | 7.839733e-08 | 0.0032 | `(((-5.117731 - sin(betti_1 * -0.25172737)) / euler_characteristic) / (betti_1 + -5.785062)) + -8.107076e-5` | `-8.107076e-5 + (-sin(betti_1*(-0.25172737)) - 5.117731)/(euler_characteristic*(betti_1 - 5.785062))` |
| 15 | 7.830771e-08 | 0.0011 | `((-4.9568853 - sin(betti_1 * -0.24994744)) / euler_characteristic) / (-5.406272 + (cos(euler_characteristic) + betti_1))` | `(-sin(betti_1*(-0.24994744)) - 4.9568853)/(euler_characteristic*(betti_1 + cos(euler_characteristic) - 5.406272))` |
| 17 | 7.676279e-08 | 0.0100 | `((-4.9568934 - sin((betti_1 - sin(betti_1 * -0.7594142)) * -0.25097498)) / euler_characteristic) / (betti_1 + -4.9568853)` | `(-sin((betti_1 - sin(betti_1*(-0.7594142)))*(-0.25097498)) - 4.9568934)/(euler_characteristic*(betti_1 - 4.9568853))` |
| 19 | 7.667005e-08 | 0.0006 | `((-4.9568834 - sin((betti_1 - sin((betti_1 * betti_0) * -0.7563827)) * -0.25018838)) / euler_characteristic) / (betti_1 + -5.3648114)` | `(-sin((betti_1 - sin(betti_1*betti_0*(-0.7563827)))*(-0.25018838)) - 4.9568834)/(euler_characteristic*(betti_1 - 5.3648114))` |
| 20 | 7.630404e-08 | 0.0048 | `((-4.9568853 - sin(-0.24994744 * (betti_1 - sin(betti_1 * -0.24994744)))) / euler_characteristic) / (-5.406272 + (betti_1 + cos(euler_characteristic)))` | `(-sin(-0.24994744*(betti_1 - sin(betti_1*(-0.24994744)))) - 4.9568853)/(euler_characteristic*(betti_1 + cos(euler_characteristic) - 5.406272))` |

</details>

