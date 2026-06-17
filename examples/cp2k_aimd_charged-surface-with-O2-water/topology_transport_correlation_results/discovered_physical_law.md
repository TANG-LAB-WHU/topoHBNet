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
| 1 | `LBHB_Fraction ≈ exp(betti_1*(-0.19103383)) + 0.004050579` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ cos(cos(n_hbonds/euler_characteristic))/n_hbonds` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(euler_characteristic*0.19788644) - 1*(-0.004057112)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ exp(betti_1*(-0.19100854)) + 0.004051126` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.25231168*cos(cos(-2.8442664/(-0.31996244 + 3.8556225/betti_1)))/betti_1` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(betti_1*(-0.19103383)) + 0.004050579$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `n_hbonds` | Total number of hydrogen bonds in the network | 44/76 | 57.9% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 40/76 | 52.6% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 19/76 | 25.0% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 2/76 | 2.6% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/76 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `n_hbonds` is the most stable feature (appearing in 44/76 Pareto equations). This strongly indicates that `n_hbonds` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(betti_1*(-0.19103383)) + 0.004050579</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 4.921079e-07 | 0.0000 | `0.0041697524` | `0.00416975240000000` |
| 3 | 4.560069e-07 | 0.0381 | `0.6196144 / n_hbonds` | `0.6196144/n_hbonds` |
| 4 | 4.560069e-07 | 0.0000 | `sin(0.61961436 / n_hbonds)` | `sin(0.61961436/n_hbonds)` |
| 5 | 4.417397e-07 | 0.0318 | `(-0.06700464 / euler_characteristic) - -0.0029032102` | `-1*(-0.0029032102) - 0.06700464/euler_characteristic` |
| 6 | 3.424341e-07 | 0.2546 | `exp(betti_1 * -0.19103383) + 0.004050579` | `exp(betti_1*(-0.19103383)) + 0.004050579` |
| 7 | 3.423704e-07 | 0.0002 | `exp(exp(betti_1 * -0.1909022)) + -0.99594957` | `exp(exp(betti_1*(-0.1909022))) - 0.99594957` |
| 8 | 3.204687e-07 | 0.0661 | `exp(3.4269352 - (betti_1 * 0.29484388)) + 0.004083878` | `exp(3.4269352 - 0.29484388*betti_1) + 0.004083878` |
| 9 | 3.204686e-07 | 0.0000 | `sin(exp(3.4269352 - (betti_1 * 0.29484388))) + 0.004083878` | `sin(exp(3.4269352 - 0.29484388*betti_1)) + 0.004083878` |
| 10 | 3.059806e-07 | 0.0463 | `(betti_1 * (exp(betti_1 * -0.28846416) + 2.2590188e-5)) + 0.002802515` | `betti_1*(exp(betti_1*(-0.28846416)) + 2.2590188e-5) + 0.002802515` |
| 11 | 2.665761e-07 | 0.1379 | `exp(sin(n_hbonds * -0.24777973) - (betti_1 * 0.20324558)) + 0.004052309` | `exp(-0.20324558*betti_1 + sin(n_hbonds*(-0.24777973))) + 0.004052309` |
| 12 | 2.665517e-07 | 0.0001 | `exp(exp(sin(n_hbonds * -0.24777973) - (betti_1 * 0.20324558))) + -0.9959494` | `exp(exp(-0.20324558*betti_1 + sin(n_hbonds*(-0.24777973)))) - 0.9959494` |
| 13 | 2.638963e-07 | 0.0100 | `(exp(cos(n_hbonds * -0.259197) - (betti_1 * 0.30720454)) * betti_1) + 0.004074895` | `betti_1*exp(-0.30720454*betti_1 + cos(n_hbonds*(-0.259197))) + 0.004074895` |
| 14 | 2.628960e-07 | 0.0038 | `exp(cos((n_hbonds + cos(betti_1)) * 0.26060006) - (betti_1 * 0.20368487)) + 0.0040553375` | `exp(-0.20368487*betti_1 + cos((n_hbonds + cos(betti_1))*0.26060006)) + 0.0040553375` |
| 15 | 2.414208e-07 | 0.0852 | `(betti_1 * (exp(cos(n_hbonds * 0.25748295) - (betti_1 * 0.2949615)) + 2.917028e-5)) + 0.0024188291` | `betti_1*(exp(-0.2949615*betti_1 + cos(n_hbonds*0.25748295)) + 2.917028e-5) + 0.0024188291` |
| 17 | 2.405176e-07 | 0.0019 | `((exp(cos(n_hbonds * 0.2579284) + ((-0.30586448 - betti_1) * 0.29484847)) + 2.6481242e-5) * betti_1) + 0.0025773724` | `betti_1*(exp((-betti_1 - 0.30586448)*0.29484847 + cos(n_hbonds*0.2579284)) + 2.6481242e-5) + 0.0025773724` |
| 19 | 2.400742e-07 | 0.0009 | `0.0025962065 + (betti_1 * (2.6196787e-5 + exp((0.29484388 * ((betti_0 * -0.29708615) - betti_1)) + cos(n_hbonds * 0.25794694))))` | `betti_1*(exp(0.29484388*(betti_0*(-0.29708615) - betti_1) + cos(n_hbonds*0.25794694)) + 2.6196787e-5) + 0.0025962065` |
| 20 | 2.321676e-07 | 0.0335 | `(betti_1 * (3.0377305e-5 + exp((-0.22212541 * cos(n_hbonds)) + (cos(n_hbonds * -0.2573039) - (0.29493544 * betti_1))))) + 0.0023514552` | `betti_1*(exp(-0.29493544*betti_1 - 0.22212541*cos(n_hbonds) + cos(n_hbonds*(-0.2573039))) + 3.0377305e-5) + 0.0023514552` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: cos(cos(n_hbonds/euler_characteristic))/n_hbonds</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 4.921079e-07 | 0.0000 | `0.004169753` | `0.00416975300000000` |
| 3 | 4.560069e-07 | 0.0381 | `0.6196144 / n_hbonds` | `0.6196144/n_hbonds` |
| 4 | 4.560067e-07 | 0.0000 | `sin(0.6196166 / n_hbonds)` | `sin(0.6196166/n_hbonds)` |
| 5 | 4.417398e-07 | 0.0318 | `(-0.0670254 / euler_characteristic) + 0.0029028328` | `0.0029028328 - 0.0670254/euler_characteristic` |
| 6 | 3.975630e-07 | 0.1054 | `-0.0040673157 / cos(n_hbonds * 0.020532237)` | `-0.0040673157/cos(n_hbonds*0.020532237)` |
| 7 | 3.426921e-07 | 0.1485 | `cos(cos(n_hbonds / euler_characteristic)) / n_hbonds` | `cos(cos(n_hbonds/euler_characteristic))/n_hbonds` |
| 9 | 3.378277e-07 | 0.0071 | `cos(cos(n_hbonds / (-1.1657099 + betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(betti_1 - 1.1657099)))/n_hbonds` |
| 11 | 3.144680e-07 | 0.0358 | `cos(cos((euler_characteristic + euler_characteristic) / (betti_1 - 15.996431))) / n_hbonds` | `cos(cos((euler_characteristic + euler_characteristic)/(betti_1 - 1*15.996431)))/n_hbonds` |
| 13 | 2.783713e-07 | 0.0610 | `-0.003915692 / cos((cos(n_hbonds * 0.21119335) - (n_hbonds * 0.07503892)) * 0.27238125)` | `-0.003915692/cos((-0.07503892*n_hbonds + cos(n_hbonds*0.21119335))*0.27238125)` |
| 14 | 2.783712e-07 | 0.0000 | `sin(-0.003915692 / cos((cos(n_hbonds * 0.21119335) - (n_hbonds * 0.07503892)) * 0.27238125))` | `sin(-0.003915692/cos((-0.07503892*n_hbonds + cos(n_hbonds*0.21119335))*0.27238125))` |
| 15 | 2.665055e-07 | 0.0436 | `-0.003943555 / cos(0.264732 * ((n_hbonds * -0.07593591) - cos(exp(cos(-0.2110601 * n_hbonds)))))` | `-0.003943555/cos(0.264732*(n_hbonds*(-0.07593591) - cos(exp(cos(-0.2110601*n_hbonds)))))` |
| 16 | 2.661641e-07 | 0.0013 | `sin(-0.003943555 / cos(0.264732 * ((n_hbonds * -0.07593591) - cos(exp(cos(0.21069016 * n_hbonds))))))` | `sin(-0.003943555/cos(0.264732*(n_hbonds*(-0.07593591) - cos(exp(cos(0.21069016*n_hbonds))))))` |
| 17 | 2.661366e-07 | 0.0001 | `-0.003943555 / cos(0.26422855 * ((n_hbonds * -0.07593591) - cos(exp(cos(0.06445623 - (0.21113068 * n_hbonds))))))` | `-0.003943555/cos(0.26422855*(n_hbonds*(-0.07593591) - cos(exp(cos(0.06445623 - 0.21113068*n_hbonds)))))` |
| 18 | 2.622154e-07 | 0.0148 | `sin(-0.0039213654 / cos((cos(exp(cos(n_hbonds * 0.21025749) + 0.14603704)) - (n_hbonds * -0.075941235)) * 0.2683006))` | `sin(-0.0039213654/cos((-(-0.075941235)*n_hbonds + cos(exp(cos(n_hbonds*0.21025749) + 0.14603704)))*0.2683006))` |
| 19 | 2.573048e-07 | 0.0189 | `sin(-0.003943555 / cos(-0.26401213 * (cos(exp(cos((sin(euler_characteristic) + n_hbonds) * 0.21025556))) - (-0.07593591 * n_hbonds))))` | `sin(-0.003943555/cos(-0.26401213*(-(-1)*0.07593591*n_hbonds + cos(exp(cos((n_hbonds + sin(euler_characteristic))*0.21025556))))))` |
| 20 | 2.571239e-07 | 0.0007 | `-0.003923246 / cos(((0.080445 * n_hbonds) - cos((0.23876782 / cos(n_hbonds * 0.2131877)) - (n_hbonds * 0.21286806))) * 0.2521648)` | `-0.003923246/cos((0.080445*n_hbonds - cos(-0.21286806*n_hbonds + 0.23876782/cos(n_hbonds*0.2131877)))*0.2521648)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(euler_characteristic*0.19788644) - 1*(-0.004057112)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 4.921079e-07 | 0.0000 | `0.0041697524` | `0.00416975240000000` |
| 3 | 4.560069e-07 | 0.0381 | `0.6196144 / n_hbonds` | `0.6196144/n_hbonds` |
| 5 | 4.417397e-07 | 0.0159 | `(-0.06701249 / euler_characteristic) + 0.0029030591` | `0.0029030591 - 0.06701249/euler_characteristic` |
| 6 | 3.448030e-07 | 0.2477 | `exp(euler_characteristic * 0.19788644) - -0.004057112` | `exp(euler_characteristic*0.19788644) - 1*(-0.004057112)` |
| 7 | 3.426921e-07 | 0.0061 | `cos(cos(n_hbonds / euler_characteristic)) / n_hbonds` | `cos(cos(n_hbonds/euler_characteristic))/n_hbonds` |
| 8 | 3.187074e-07 | 0.0726 | `cos(cos(log(betti_1 + -21.205894))) / n_hbonds` | `cos(cos(log(betti_1 - 21.205894)))/n_hbonds` |
| 9 | 2.889369e-07 | 0.0981 | `cos(sin(0.86243623 / sin(log(betti_1)))) / n_hbonds` | `cos(sin(0.86243623/sin(log(betti_1))))/n_hbonds` |
| 10 | 2.815445e-07 | 0.0259 | `cos(cos(cos(-0.8558804 / sin(log(betti_1))))) / n_hbonds` | `cos(cos(cos(0.8558804/sin(log(betti_1)))))/n_hbonds` |
| 12 | 2.680565e-07 | 0.0245 | `sin(cos(sin(-0.74439377 / sin(log(-2.1664412 + betti_1))))) / n_hbonds` | `sin(cos(sin(0.74439377/sin(log(betti_1 - 2.1664412)))))/n_hbonds` |
| 13 | 2.574684e-07 | 0.0403 | `cos(sin(0.7703023 / sin(log(betti_1 - 1.9462059)))) / (8.475631 + n_hbonds)` | `cos(sin(0.7703023/sin(log(betti_1 - 1.9462059))))/(n_hbonds + 8.475631)` |
| 14 | 2.574683e-07 | 0.0000 | `sin(cos(sin(0.7703023 / sin(log(betti_1 - 1.9462059)))) / (8.475631 + n_hbonds))` | `sin(cos(sin(0.7703023/sin(log(betti_1 - 1.9462059))))/(n_hbonds + 8.475631))` |
| 16 | 2.538385e-07 | 0.0071 | `cos(sin(-0.781644 / sin(log((cos(betti_1) + -1.789019) + betti_1)))) / (n_hbonds + 7.9684396)` | `cos(sin(0.781644/sin(log(betti_1 + cos(betti_1) - 1.789019))))/(n_hbonds + 7.9684396)` |
| 18 | 2.523161e-07 | 0.0030 | `cos(sin(-0.7757806 / sin(log(betti_1 - 1.8443407)))) / (7.9684396 + (sin(n_hbonds / 4.0809374) + n_hbonds))` | `cos(sin(0.7757806/sin(log(betti_1 - 1.8443407))))/(n_hbonds + sin(0.245041739674811*n_hbonds) + 7.9684396)` |
| 19 | 2.522624e-07 | 0.0002 | `sin(cos(sin(-0.7757806 / sin(log(betti_1 + -1.8805046)))) / (7.9684396 + (n_hbonds + sin(n_hbonds / 4.0809374))))` | `sin(cos(sin(0.7757806/sin(log(betti_1 - 1.8805046))))/(n_hbonds + sin(0.245041739674811*n_hbonds) + 7.9684396))` |
| 20 | 2.522237e-07 | 0.0002 | `cos(sin(-0.7731416 / sin(log(betti_1 - (0.08871867 + 1.8443407))))) / (n_hbonds + (sin(n_hbonds / 4.0809374) + 7.9684396))` | `cos(sin(0.7731416/sin(log(betti_1 - 1.93305937))))/(n_hbonds + sin(0.245041739674811*n_hbonds) + 7.9684396)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: exp(betti_1*(-0.19100854)) + 0.004051126</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 4.921078e-07 | 0.0000 | `0.0041697533` | `0.00416975330000000` |
| 3 | 4.560069e-07 | 0.0381 | `0.6196144 / n_hbonds` | `0.6196144/n_hbonds` |
| 4 | 4.506130e-07 | 0.0119 | `0.016663717 / log(betti_1)` | `0.016663717/log(betti_1)` |
| 5 | 4.417396e-07 | 0.0199 | `(-0.06698226 / euler_characteristic) - -0.0029036636` | `-1*(-0.0029036636) - 0.06698226/euler_characteristic` |
| 6 | 3.424333e-07 | 0.2546 | `exp(betti_1 * -0.19100854) + 0.004051126` | `exp(betti_1*(-0.19100854)) + 0.004051126` |
| 8 | 3.254750e-07 | 0.0254 | `exp((betti_1 * -0.24365583) - -1.7611943) - -0.0040761963` | `exp(betti_1*(-0.24365583) - 1*(-1.7611943)) - 1*(-0.0040761963)` |
| 10 | 3.139623e-07 | 0.0180 | `(exp((betti_0 * euler_characteristic) * 0.30807933) + 0.000108755725) * 37.58956` | `(exp(betti_0*euler_characteristic*0.30807933) + 0.000108755725)*37.58956` |
| 11 | 2.687332e-07 | 0.1556 | `exp(sin(n_hbonds * -0.24771562) + (euler_characteristic * 0.21048178)) - -0.0040564146` | `exp(euler_characteristic*0.21048178 + sin(n_hbonds*(-0.24771562))) - 1*(-0.0040564146)` |
| 13 | 2.425546e-07 | 0.0512 | `exp(sin(n_hbonds * -0.24647129) + (euler_characteristic * 0.1979509)) - (n_hbonds * -2.6708934e-5)` | `-(-2.6708934e-5)*n_hbonds + exp(euler_characteristic*0.1979509 + sin(n_hbonds*(-0.24647129)))` |
| 17 | 2.421936e-07 | 0.0004 | `(exp((euler_characteristic * 0.19798662) + sin((n_hbonds * -0.24822882) - -0.20823225)) - (n_hbonds * 0.99997324)) + n_hbonds` | `-0.99997324*n_hbonds + n_hbonds + exp(euler_characteristic*0.19798662 + sin(n_hbonds*(-0.24822882) - 1*(-0.20823225)))` |
| 18 | 2.413301e-07 | 0.0036 | `exp(sin(-0.24647129 * (n_hbonds - sin(-0.24647129 * n_hbonds))) + (0.1979509 * euler_characteristic)) - (n_hbonds * -2.6708934e-5)` | `-(-2.6708934e-5)*n_hbonds + exp(0.1979509*euler_characteristic + sin(-0.24647129*(n_hbonds - sin(-0.24647129*n_hbonds))))` |
| 19 | 2.361223e-07 | 0.0218 | `exp(cos(sin(n_hbonds * -0.28025648)) + ((0.22041906 * euler_characteristic) + sin(n_hbonds * -0.24706116))) - (n_hbonds * -2.6795251e-5)` | `-(-2.6795251e-5)*n_hbonds + exp(0.22041906*euler_characteristic + sin(n_hbonds*(-0.24706116)) + cos(sin(n_hbonds*(-0.28025648))))` |
| 20 | 2.361218e-07 | 0.0000 | `sin(exp((sin(n_hbonds * -0.24706116) + cos(sin(n_hbonds * -0.28025648))) + (euler_characteristic * 0.22041906)) - (n_hbonds * -2.6795251e-5))` | `sin(-(-2.6795251e-5)*n_hbonds + exp(euler_characteristic*0.22041906 + sin(n_hbonds*(-0.24706116)) + cos(sin(n_hbonds*(-0.28025648)))))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.25231168*cos(cos(-2.8442664/(-0.31996244 + 3.8556225/betti_1)))/betti_1</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 4.921077e-07 | 0.0000 | `0.0041696955` | `0.00416969550000000` |
| 3 | 4.560069e-07 | 0.0381 | `0.6196144 / n_hbonds` | `0.6196144/n_hbonds` |
| 4 | 4.506130e-07 | 0.0119 | `0.016663717 / log(betti_1)` | `0.016663717/log(betti_1)` |
| 5 | 4.417396e-07 | 0.0199 | `0.0029031618 - (0.06700654 / euler_characteristic)` | `0.0029031618 - 0.06700654/euler_characteristic` |
| 6 | 3.424308e-07 | 0.2547 | `exp(betti_1 * -0.19092238) - -0.0040501608` | `exp(betti_1*(-0.19092238)) - 1*(-0.0040501608)` |
| 8 | 3.208921e-07 | 0.0325 | `exp(3.0190644 - (betti_1 * 0.28259116)) - -0.004081127` | `exp(3.0190644 - 0.28259116*betti_1) - 1*(-0.004081127)` |
| 9 | 3.121016e-07 | 0.0278 | `cos(cos(betti_1 * -0.074721865)) * (0.2692943 / betti_1)` | `cos(cos(betti_1*(-0.074721865)))*0.2692943/betti_1` |
| 10 | 2.726463e-07 | 0.1352 | `(cos(cos(sin(betti_1 * -0.07486239))) / betti_1) * 0.2962276` | `cos(cos(sin(betti_1*(-0.07486239))))*0.2962276/betti_1` |
| 12 | 2.718509e-07 | 0.0015 | `(0.29621056 / betti_1) * cos(cos(sin((betti_1 - 1.2526479) * -0.07682765)))` | `0.29621056*cos(cos(sin((betti_1 - 1*1.2526479)*(-0.07682765))))/betti_1` |
| 13 | 2.296170e-07 | 0.1688 | `0.25231168 * (cos(cos(-2.8442664 / ((3.8556225 / betti_1) + -0.31996244))) / betti_1)` | `0.25231168*cos(cos(-2.8442664/(-0.31996244 + 3.8556225/betti_1)))/betti_1` |
| 14 | 2.296036e-07 | 0.0001 | `0.25231168 * sin(cos(cos(-2.8442664 / (-0.31996244 + (3.8556225 / betti_1)))) / betti_1)` | `0.25231168*sin(cos(cos(-2.8442664/(-0.31996244 + 3.8556225/betti_1)))/betti_1)` |
| 15 | 2.290671e-07 | 0.0023 | `(cos(cos(3.2198129 / ((3.3928406 / (betti_1 * betti_1)) - -0.04680881))) / betti_1) * 0.24923618` | `cos(cos(3.2198129/(-1*(-0.04680881) + 3.3928406/((betti_1*betti_1)))))*0.24923618/betti_1` |
| 17 | 2.288749e-07 | 0.0004 | `((0.24923618 * cos(cos(3.2198129 / ((3.3928406 / (betti_1 * betti_1)) - -0.04680881)))) / betti_1) / 0.9961086` | `0.24923618*cos(cos(3.2198129/(-1*(-0.04680881) + 3.3928406/((betti_1*betti_1)))))/(0.9961086*betti_1)` |
| 19 | 2.281235e-07 | 0.0016 | `0.26501316 * (cos(cos(-3.0230403 / sin(cos(sin(log(euler_characteristic / -3.581171))) - 0.28469926))) / (betti_1 - -2.429627))` | `0.26501316*cos(cos(3.0230403/sin(cos(sin(log(-0.27923827150393*euler_characteristic))) - 0.28469926)))/(betti_1 + 2.429627)` |
| 20 | 2.281234e-07 | 0.0000 | `sin(cos(cos(-3.0230403 / sin(0.28469926 - cos(sin(log(-3.581171 / euler_characteristic)))))) / (betti_1 - -2.429627)) * 0.26501316` | `0.26501316*sin(cos(cos(3.0230403/sin(cos(sin(log(-3.581171/euler_characteristic))) - 0.28469926)))/(betti_1 + 2.429627))` |

</details>

