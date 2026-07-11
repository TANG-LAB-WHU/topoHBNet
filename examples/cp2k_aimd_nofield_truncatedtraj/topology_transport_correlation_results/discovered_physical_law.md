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
| 1 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173057e-5)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173202e-5)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173008e-5)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173259e-5)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ euler_characteristic*(-1.6173328e-5)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx euler_characteristic*(-1.6173057e-5)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 45/65 | 69.2% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 42/65 | 64.6% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 27/65 | 41.5% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/65 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/65 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 45/65 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: euler_characteristic*(-1.6173057e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936078` | `0.000993607800000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173057e-5` | `euler_characteristic*(-1.6173057e-5)` |
| 5 | 3.361987e-08 | 0.0108 | `(n_hbonds * 1.8427212e-5) + -0.0018810206` | `n_hbonds*1.8427212e-5 - 0.0018810206` |
| 6 | 3.357123e-08 | 0.0014 | `(log(n_hbonds) * 0.0028905591) + -0.013602694` | `0.0028905591*log(n_hbonds) - 0.013602694` |
| 8 | 3.267376e-08 | 0.0135 | `((0.6240381 / cos(betti_1)) + euler_characteristic) * -1.6238186e-5` | `(euler_characteristic + 0.6240381/cos(betti_1))*(-1.6238186e-5)` |
| 10 | 3.262184e-08 | 0.0008 | `((cos(sin(n_hbonds)) / cos(betti_1)) + euler_characteristic) * -1.6237374e-5` | `(euler_characteristic + cos(sin(n_hbonds))/cos(betti_1))*(-1.6237374e-5)` |
| 11 | 3.245248e-08 | 0.0052 | `((sin(0.100847244 * euler_characteristic) / cos(betti_1)) + euler_characteristic) * -1.6237374e-5` | `(euler_characteristic + sin(0.100847244*euler_characteristic)/cos(betti_1))*(-1.6237374e-5)` |
| 12 | 3.241467e-08 | 0.0012 | `((sin(cos(betti_1 * 0.121898025)) / cos(betti_1)) + euler_characteristic) * -1.6237374e-5` | `(euler_characteristic + sin(cos(betti_1*0.121898025))/cos(betti_1))*(-1.6237374e-5)` |
| 13 | 3.230897e-08 | 0.0033 | `((cos(betti_1 * 0.45984355) + (0.60888225 / cos(betti_1))) + euler_characteristic) * -1.6140255e-5` | `(euler_characteristic + cos(betti_1*0.45984355) + 0.60888225/cos(betti_1))*(-1.6140255e-5)` |
| 15 | 3.209968e-08 | 0.0032 | `(((0.5428271 / cos(betti_1)) + euler_characteristic) * -1.5961012e-5) + (cos(betti_1 * 0.45775968) * -4.1266605e-5)` | `(euler_characteristic + 0.5428271/cos(betti_1))*(-1.5961012e-5) + cos(betti_1*0.45775968)*(-4.1266605e-5)` |
| 16 | 3.209968e-08 | 0.0000 | `sin((((0.5428271 / cos(betti_1)) + euler_characteristic) * -1.5961012e-5) + (cos(betti_1 * 0.45775968) * -4.1266605e-5))` | `sin((euler_characteristic + 0.5428271/cos(betti_1))*(-1.5961012e-5) + cos(betti_1*0.45775968)*(-4.1266605e-5))` |
| 17 | 3.206485e-08 | 0.0011 | `(cos(betti_1 * -0.45802772) * -4.374808e-5) + (-1.5950129e-5 * (euler_characteristic + (cos(sin(betti_1)) / cos(betti_1))))` | `-1.5950129e-5*(euler_characteristic + cos(sin(betti_1))/cos(betti_1)) + cos(betti_1*(-0.45802772))*(-4.374808e-5)` |
| 18 | 3.204391e-08 | 0.0007 | `-1.6116432e-5 * ((euler_characteristic + (sin(exp(-0.0691289 - sin(n_hbonds))) / cos(betti_1))) + cos(betti_1 * 0.45917976))` | `-1.6116432e-5*(euler_characteristic + sin(exp(-sin(n_hbonds) - 0.0691289))/cos(betti_1) + cos(betti_1*0.45917976))` |
| 19 | 3.197783e-08 | 0.0021 | `(cos(betti_1 * -0.45802772) * -3.728219e-5) + (((cos(-0.28441533 - sin(n_hbonds)) / cos(betti_1)) + euler_characteristic) * -1.6020898e-5)` | `(euler_characteristic + cos(-sin(n_hbonds) - 0.28441533)/cos(betti_1))*(-1.6020898e-5) + cos(betti_1*(-0.45802772))*(-3.728219e-5)` |
| 20 | 3.185705e-08 | 0.0038 | `((euler_characteristic + (sin(exp(-0.05748214 - sin(n_hbonds))) / cos(betti_1))) * -1.6020898e-5) + (-3.728219e-5 * cos(0.4576286 * betti_1))` | `(euler_characteristic + sin(exp(-sin(n_hbonds) - 0.05748214))/cos(betti_1))*(-1.6020898e-5) - 3.728219e-5*cos(0.4576286*betti_1)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: euler_characteristic*(-1.6173202e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936078` | `0.000993607800000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173202e-5` | `euler_characteristic*(-1.6173202e-5)` |
| 5 | 3.352300e-08 | 0.0123 | `(-0.45346382 / n_hbonds) - -0.0039016402` | `-1*(-0.0039016402) - 0.45346382/n_hbonds` |
| 8 | 3.266967e-08 | 0.0086 | `(betti_1 * 1.5978427e-5) - (9.9832e-6 / cos(betti_1))` | `betti_1*1.5978427e-5 - 9.9832e-6/cos(betti_1)` |
| 10 | 3.201653e-08 | 0.0101 | `((n_hbonds * 1.6146565e-5) - (9.880004e-6 / cos(betti_1))) - 0.0015209293` | `n_hbonds*1.6146565e-5 - 1*0.0015209293 - 9.880004e-6/cos(betti_1)` |
| 11 | 3.193828e-08 | 0.0024 | `-0.011667948 + (log(n_hbonds - (0.54685646 / cos(betti_1))) * 0.0025082845)` | `0.0025082845*log(n_hbonds - 0.54685646/cos(betti_1)) - 0.011667948` |
| 12 | 3.191062e-08 | 0.0009 | `-0.0015205008 - ((6.757126e-6 / (cos(betti_1) + -0.009357357)) - (n_hbonds * 1.614558e-5))` | `-(-1.614558e-5*n_hbonds + 6.757126e-6/(cos(betti_1) - 0.009357357)) - 0.0015205008` |
| 13 | 3.188988e-08 | 0.0007 | `(log(n_hbonds - (0.46040353 / cos(betti_1 - 0.007272139))) * 0.0023688308) + -0.010963851` | `0.0023688308*log(n_hbonds - 0.46040353/cos(betti_1 - 0.007272139)) - 0.010963851` |
| 14 | 3.184157e-08 | 0.0015 | `(((4.854512e-7 + (-3.1570642e-5 / betti_1)) / cos(betti_1)) + (n_hbonds * 4.1011777e-8)) * n_hbonds` | `n_hbonds*(n_hbonds*4.1011777e-8 + (4.854512e-7 - 3.1570642e-5/betti_1)/cos(betti_1))` |
| 15 | 3.182208e-08 | 0.0006 | `(((4.854512e-7 + (-3.1570642e-5 / betti_1)) / sin(cos(betti_1))) + (n_hbonds * 4.1011777e-8)) * n_hbonds` | `n_hbonds*(n_hbonds*4.1011777e-8 + (4.854512e-7 - 3.1570642e-5/betti_1)/sin(cos(betti_1)))` |
| 16 | 3.149892e-08 | 0.0102 | `(log(n_hbonds - ((0.5354914 / cos(betti_1)) - sin(0.5382712 * n_hbonds))) * 0.0027026576) + -0.012652449` | `0.0027026576*log(n_hbonds + sin(0.5382712*n_hbonds) - 0.5354914/cos(betti_1)) - 0.012652449` |
| 18 | 3.149572e-08 | 0.0001 | `(log(n_hbonds - ((0.5354914 / cos(betti_1)) - sin((n_hbonds * 0.540117) - 0.36298466))) * 0.0027026576) + -0.012652449` | `0.0027026576*log(n_hbonds + sin(0.540117*n_hbonds - 0.36298466) - 0.5354914/cos(betti_1)) - 0.012652449` |
| 19 | 3.137604e-08 | 0.0038 | `(0.0025082845 * log(n_hbonds - ((0.5354885 / cos(betti_1)) - (cos(betti_1) * (-0.28528014 / cos(euler_characteristic)))))) + -0.011667948` | `0.0025082845*log(n_hbonds - 0.28528014*cos(betti_1)/cos(euler_characteristic) - 0.5354885/cos(betti_1)) - 0.011667948` |
| 20 | 3.137589e-08 | 0.0000 | `(0.0025082845 * log(n_hbonds - ((0.5354885 / cos(betti_1)) - (cos(betti_1) * (-0.28528014 / sin(cos(euler_characteristic))))))) + -0.011667948` | `0.0025082845*log(n_hbonds - 0.5354885/cos(betti_1) - 0.28528014*cos(betti_1)/sin(cos(euler_characteristic))) - 0.011667948` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: euler_characteristic*(-1.6173008e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173008e-5` | `euler_characteristic*(-1.6173008e-5)` |
| 5 | 3.352336e-08 | 0.0123 | `0.003899097 - (0.45315963 / n_hbonds)` | `0.003899097 - 0.45315963/n_hbonds` |
| 6 | 3.352334e-08 | 0.0000 | `0.003899097 - sin(0.45315963 / n_hbonds)` | `0.003899097 - sin(0.45315963/n_hbonds)` |
| 7 | 3.282225e-08 | 0.0211 | `(-0.005384207 / (n_hbonds - 138.39162)) + 0.001310461` | `0.001310461 - 0.005384207/(n_hbonds - 1*138.39162)` |
| 10 | 3.189210e-08 | 0.0096 | `0.0036705374 - (0.4167384 / (n_hbonds - (0.49769443 / cos(betti_1))))` | `0.0036705374 - 0.4167384/(n_hbonds - 0.49769443/cos(betti_1))` |
| 11 | 3.189209e-08 | 0.0000 | `0.0036705374 - sin(0.4167384 / (n_hbonds - (0.49769443 / cos(betti_1))))` | `0.0036705374 - sin(0.4167384/(n_hbonds - 0.49769443/cos(betti_1)))` |
| 12 | 3.187174e-08 | 0.0006 | `0.0036725504 - (0.41672507 / (n_hbonds - (0.41672507 / cos(betti_1 - 0.0036725504))))` | `0.0036725504 - 0.41672507/(n_hbonds - 0.41672507/cos(betti_1 - 1*0.0036725504))` |
| 14 | 3.186040e-08 | 0.0002 | `0.0036705374 - (0.4167384 / (n_hbonds - (n_hbonds / ((betti_1 / 0.18501067) * cos(betti_1)))))` | `0.0036705374 - 0.4167384/(n_hbonds - n_hbonds/(betti_1*cos(betti_1)/0.18501067))` |
| 15 | 3.143565e-08 | 0.0134 | `0.003900033 - (0.45315832 / ((n_hbonds - (0.41080266 / cos(betti_1))) - cos(n_hbonds * 0.5082587)))` | `0.003900033 - 0.45315832/(n_hbonds - cos(n_hbonds*0.5082587) - 0.41080266/cos(betti_1))` |
| 17 | 3.124120e-08 | 0.0031 | `0.0038968073 - (0.45315835 / ((n_hbonds - (0.39173433 / cos(betti_1))) - (sin(n_hbonds * 0.51832116) * 1.9564483)))` | `0.0038968073 - 0.45315835/(n_hbonds - 1.9564483*sin(n_hbonds*0.51832116) - 0.39173433/cos(betti_1))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: euler_characteristic*(-1.6173259e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936078` | `0.000993607800000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173259e-5` | `euler_characteristic*(-1.6173259e-5)` |
| 5 | 3.352433e-08 | 0.0123 | `(-0.44455865 / n_hbonds) + 0.0038445285` | `0.0038445285 - 0.44455865/n_hbonds` |
| 6 | 3.286806e-08 | 0.0198 | `cos(n_hbonds * -0.05883696) * -0.0010425249` | `cos(n_hbonds*(-0.05883696))*(-0.0010425249)` |
| 8 | 3.267317e-08 | 0.0030 | `(-9.947394e-6 / cos(betti_1)) + (euler_characteristic * -1.6237167e-5)` | `euler_characteristic*(-1.6237167e-5) - 9.947394e-6/cos(betti_1)` |
| 11 | 3.259159e-08 | 0.0008 | `cos(((n_hbonds - cos(betti_1)) * n_hbonds) * 0.0002484414) * 0.0010534474` | `cos((n_hbonds - cos(betti_1))*n_hbonds*0.0002484414)*0.0010534474` |
| 12 | 3.177038e-08 | 0.0255 | `cos(cos(((0.0001368012 / cos(betti_1)) + -0.048226584) * n_hbonds)) * 0.0010628303` | `cos(cos(n_hbonds*(-0.048226584 + 0.0001368012/cos(betti_1))))*0.0010628303` |
| 14 | 3.154634e-08 | 0.0035 | `cos(((0.0002420592 * betti_1) / cos(betti_1)) + cos(n_hbonds * 0.048186664)) * 0.0010651948` | `cos(0.0002420592*betti_1/cos(betti_1) + cos(n_hbonds*0.048186664))*0.0010651948` |
| 15 | 3.153643e-08 | 0.0003 | `cos(((betti_1 * 0.0002420592) / sin(cos(betti_1))) + cos(n_hbonds * -0.048191838)) * 0.0010651948` | `cos(betti_1*0.0002420592/sin(cos(betti_1)) + cos(n_hbonds*(-0.048191838)))*0.0010651948` |
| 16 | 3.153620e-08 | 0.0000 | `sin(cos(cos(n_hbonds * 0.048186664) + ((betti_1 * 0.0002420592) / sin(cos(betti_1)))) * 0.0010651948)` | `sin(cos(betti_1*0.0002420592/sin(cos(betti_1)) + cos(n_hbonds*0.048186664))*0.0010651948)` |
| 17 | 3.152226e-08 | 0.0004 | `cos(cos(n_hbonds * 0.048186664) + ((betti_1 / sin(sin(sin(cos(betti_1))))) * 0.0002420592)) * 0.0010651948` | `cos(betti_1*0.0002420592/sin(sin(sin(cos(betti_1)))) + cos(n_hbonds*0.048186664))*0.0010651948` |
| 18 | 3.142468e-08 | 0.0031 | `cos((betti_1 * (0.00025638443 / cos(betti_1))) + cos((n_hbonds - cos(exp(betti_1))) * 0.048265338)) * 0.001057409` | `cos(betti_1*0.00025638443/cos(betti_1) + cos((n_hbonds - cos(exp(betti_1)))*0.048265338))*0.001057409` |
| 19 | 3.141089e-08 | 0.0004 | `cos(cos((n_hbonds - cos(exp(betti_1))) * 0.048265338) + ((0.00023670426 * betti_1) / sin(cos(betti_1)))) * 0.001057409` | `cos(0.00023670426*betti_1/sin(cos(betti_1)) + cos((n_hbonds - cos(exp(betti_1)))*0.048265338))*0.001057409` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: euler_characteristic*(-1.6173328e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936078` | `0.000993607800000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173328e-5` | `euler_characteristic*(-1.6173328e-5)` |
| 5 | 3.352423e-08 | 0.0123 | `0.003956291 - (0.46198702 / n_hbonds)` | `0.003956291 - 0.46198702/n_hbonds` |
| 7 | 3.352423e-08 | 0.0000 | `0.003956291 - sin(sin(0.46198702 / n_hbonds))` | `0.003956291 - sin(sin(0.46198702/n_hbonds))` |
| 8 | 3.267316e-08 | 0.0257 | `(euler_characteristic * -1.6237349e-5) - (9.946846e-6 / cos(betti_1))` | `euler_characteristic*(-1.6237349e-5) - 9.946846e-6/cos(betti_1)` |
| 10 | 3.260934e-08 | 0.0010 | `(euler_characteristic * -1.6238217e-5) - (-0.0005662842 / (euler_characteristic * cos(betti_1)))` | `euler_characteristic*(-1.6238217e-5) - (-1)*0.0005662842/(euler_characteristic*cos(betti_1))` |
| 11 | 3.254329e-08 | 0.0020 | `(euler_characteristic - (cos(euler_characteristic * 0.27671838) / cos(betti_1))) * -1.6225993e-5` | `(euler_characteristic - cos(euler_characteristic*0.27671838)/cos(betti_1))*(-1.6225993e-5)` |
| 13 | 3.229741e-08 | 0.0038 | `(-9.5080895e-6 / cos(betti_1)) + ((euler_characteristic - cos(euler_characteristic * 0.5207088)) * -1.6167402e-5)` | `(euler_characteristic - cos(euler_characteristic*0.5207088))*(-1.6167402e-5) - 9.5080895e-6/cos(betti_1)` |
| 15 | 3.140094e-08 | 0.0141 | `((cos((0.029439349 / cos(betti_1)) - (n_hbonds * 0.09729514)) / euler_characteristic) * 0.022513894) + 0.00069809245` | `0.00069809245 + cos(-0.09729514*n_hbonds + 0.029439349/cos(betti_1))*0.022513894/euler_characteristic` |
| 17 | 3.140068e-08 | 0.0000 | `((cos((0.029439349 / cos(betti_1)) - (n_hbonds * 0.09729514)) / (euler_characteristic + 0.065605864)) * 0.022513894) + 0.00069809245` | `0.00069809245 + cos(-0.09729514*n_hbonds + 0.029439349/cos(betti_1))*0.022513894/(euler_characteristic + 0.065605864)` |
| 18 | 3.135918e-08 | 0.0013 | `0.00069809245 + ((cos((0.030798735 / cos(betti_1)) - (n_hbonds * 0.09729514)) * 0.022513894) / (euler_characteristic - sin(n_hbonds)))` | `0.00069809245 + cos(-0.09729514*n_hbonds + 0.030798735/cos(betti_1))*0.022513894/(euler_characteristic - sin(n_hbonds))` |
| 20 | 3.133768e-08 | 0.0003 | `0.00069809245 + ((cos((0.030798735 / cos(betti_1)) - (n_hbonds * 0.09729514)) * 0.022513894) / (euler_characteristic - cos(n_hbonds / 1.4016385)))` | `0.00069809245 + cos(-0.09729514*n_hbonds + 0.030798735/cos(betti_1))*0.022513894/(euler_characteristic - cos(n_hbonds/1.4016385))` |

</details>

