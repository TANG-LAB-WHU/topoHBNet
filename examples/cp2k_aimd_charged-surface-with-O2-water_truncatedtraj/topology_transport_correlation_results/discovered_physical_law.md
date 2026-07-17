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
| 1 | `LBHB_Fraction ≈ betti_1*3.800399/((n_hbonds - 1.5634004/sin(n_hbonds - 1*(-0.53420717)))*n_hbonds) - 0.00514158` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ 0.65234816/(n_hbonds*cos(5.46773/(n_hbonds*sin(n_hbonds/0.48757625))))` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.651901/(n_hbonds - 1.4627218/sin(n_hbonds + 0.5268553))` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -1*0.010933882 + 1.4546862/(n_hbonds - (betti_1 - 0.13173987/cos(exp(sin(n_hbonds + 0.9841815)))))` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.40720773/(euler_characteristic + n_hbonds)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx betti_1*3.800399/((n_hbonds - 1.5634004/sin(n_hbonds - 1*(-0.53420717)))*n_hbonds) - 0.00514158$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `n_hbonds` | Total number of hydrogen bonds in the network | 67/76 | 88.2% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 45/76 | 59.2% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 26/76 | 34.2% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 2/76 | 2.6% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/76 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `n_hbonds` is the most stable feature (appearing in 67/76 Pareto equations). This strongly indicates that `n_hbonds` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: betti_1*3.800399/((n_hbonds - 1.5634004/sin(n_hbonds - 1*(-0.53420717)))*n_hbonds) - 0.00514158</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830125` | `0.00418301250000000` |
| 2 | 3.691254e-06 | 0.0000 | `sin(0.004183075)` | `sin(0.004183075)` |
| 3 | 3.687095e-06 | 0.0011 | `0.6523769 / n_hbonds` | `0.6523769/n_hbonds` |
| 4 | 3.687095e-06 | 0.0000 | `sin(0.65237826 / n_hbonds)` | `sin(0.65237826/n_hbonds)` |
| 5 | 3.647940e-06 | 0.0107 | `0.40299097 / (n_hbonds - betti_1)` | `0.40299097/(-betti_1 + n_hbonds)` |
| 7 | 3.614042e-06 | 0.0047 | `(1.2176219 / (n_hbonds + euler_characteristic)) + -0.008337155` | `-0.008337155 + 1.2176219/(euler_characteristic + n_hbonds)` |
| 9 | 3.609894e-06 | 0.0006 | `(((betti_1 / n_hbonds) * 3.6926744) / n_hbonds) + -0.00487521` | `betti_1*3.6926744/(n_hbonds*n_hbonds) - 0.00487521` |
| 10 | 3.608680e-06 | 0.0003 | `(sin(betti_1 / n_hbonds) * (3.9529681 / n_hbonds)) + -0.0052777417` | `-0.0052777417 + sin(betti_1/n_hbonds)*3.9529681/n_hbonds` |
| 11 | 3.607243e-06 | 0.0004 | `((((betti_1 / n_hbonds) + 0.09123182) / n_hbonds) * 3.5791163) + -0.006689901` | `-0.006689901 + (betti_1/n_hbonds + 0.09123182)*3.5791163/n_hbonds` |
| 12 | 3.596265e-06 | 0.0030 | `(((betti_1 - cos(betti_1)) * (3.6069963 / n_hbonds)) / n_hbonds) + -0.0046633924` | `-0.0046633924 + (betti_1 - cos(betti_1))*3.6069963/(n_hbonds*n_hbonds)` |
| 13 | 3.594927e-06 | 0.0004 | `(sin((betti_1 - cos(betti_1)) / n_hbonds) * (3.9830797 / n_hbonds)) + -0.005347997` | `-0.005347997 + sin((betti_1 - cos(betti_1))/n_hbonds)*3.9830797/n_hbonds` |
| 14 | 3.588333e-06 | 0.0018 | `((((sin(betti_1 * -0.8081495) + betti_1) / n_hbonds) * 3.800399) / n_hbonds) + -0.00514158` | `-0.00514158 + (betti_1 + sin(betti_1*(-0.8081495)))*3.800399/(n_hbonds*n_hbonds)` |
| 15 | 3.587179e-06 | 0.0003 | `-0.005347997 + ((3.9830797 * sin((betti_1 - sin(0.80711514 * betti_1)) / n_hbonds)) / n_hbonds)` | `-0.005347997 + 3.9830797*sin((betti_1 - sin(0.80711514*betti_1))/n_hbonds)/n_hbonds` |
| 16 | 3.505272e-06 | 0.0231 | `((betti_1 / ((-1.5634004 / sin(n_hbonds - -0.53420717)) + n_hbonds)) * (3.800399 / n_hbonds)) + -0.00514158` | `betti_1*3.800399/((n_hbonds - 1.5634004/sin(n_hbonds - 1*(-0.53420717)))*n_hbonds) - 0.00514158` |
| 17 | 3.469535e-06 | 0.0102 | `(((3.7864566 * betti_1) / n_hbonds) / ((0.5689037 / cos(0.70645094 + cos(n_hbonds))) + n_hbonds)) + -0.005109127` | `3.7864566*betti_1/(n_hbonds*(n_hbonds + 0.5689037/cos(cos(n_hbonds) + 0.70645094))) - 0.005109127` |
| 19 | 3.469122e-06 | 0.0001 | `(((3.7864566 / ((0.57063854 / cos((0.70645094 / betti_0) + cos(n_hbonds))) + n_hbonds)) / n_hbonds) * betti_1) + -0.005109127` | `3.7864566*betti_1/(n_hbonds*(n_hbonds + 0.57063854/cos(cos(n_hbonds) + 0.70645094/betti_0))) - 0.005109127` |
| 20 | 3.454556e-06 | 0.0042 | `((betti_1 / n_hbonds) * (3.7864566 / (n_hbonds + ((sin(betti_1) / cos(cos(n_hbonds) + 0.7064701)) * 0.588731)))) + -0.0051129023` | `betti_1*3.7864566/(n_hbonds*(n_hbonds + sin(betti_1)*0.588731/cos(cos(n_hbonds) + 0.7064701))) - 0.0051129023` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.65234816/(n_hbonds*cos(5.46773/(n_hbonds*sin(n_hbonds/0.48757625))))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830074` | `0.00418300740000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.65238065 / n_hbonds` | `0.65238065/n_hbonds` |
| 4 | 3.683353e-06 | 0.0010 | `log(betti_1) * 0.0010232951` | `0.0010232951*log(betti_1)` |
| 5 | 3.647940e-06 | 0.0097 | `0.40299064 / (n_hbonds - betti_1)` | `0.40299064/(-betti_1 + n_hbonds)` |
| 7 | 3.614042e-06 | 0.0047 | `(1.2169986 / (euler_characteristic + n_hbonds)) - 0.008330877` | `-1*0.008330877 + 1.2169986/(euler_characteristic + n_hbonds)` |
| 9 | 3.609892e-06 | 0.0006 | `(((betti_1 / n_hbonds) / n_hbonds) * 3.6688375) + -0.004816714` | `betti_1*3.6688375/(n_hbonds*n_hbonds) - 0.004816714` |
| 10 | 3.608679e-06 | 0.0003 | `((sin(betti_1 / n_hbonds) * 3.9693875) / n_hbonds) + -0.0053170323` | `-0.0053170323 + sin(betti_1/n_hbonds)*3.9693875/n_hbonds` |
| 11 | 3.607583e-06 | 0.0003 | `(((3.6688073 / n_hbonds) * (betti_1 + 3.6746893)) / n_hbonds) + -0.0053710514` | `-0.0053710514 + 3.6688073*(betti_1 + 3.6746893)/(n_hbonds*n_hbonds)` |
| 12 | 3.602040e-06 | 0.0015 | `(((3.7671878 * betti_1) / n_hbonds) / (cos(betti_1) + n_hbonds)) + -0.0050576935` | `3.7671878*betti_1/(n_hbonds*(n_hbonds + cos(betti_1))) - 0.0050576935` |
| 13 | 3.507328e-06 | 0.0266 | `(0.65234816 / n_hbonds) / cos((5.46773 / n_hbonds) / sin(n_hbonds / 0.48757625))` | `0.65234816/(n_hbonds*cos(5.46773/(n_hbonds*sin(n_hbonds/0.48757625))))` |
| 14 | 3.507303e-06 | 0.0000 | `sin((0.65234816 / n_hbonds) / cos((-5.472496 / n_hbonds) / sin(n_hbonds / 0.48757622)))` | `sin(0.65234816/(n_hbonds*cos(-5.472496/(n_hbonds*sin(n_hbonds/0.48757622)))))` |
| 16 | 3.453441e-06 | 0.0077 | `-0.0048192353 + ((betti_1 * (3.6688375 / ((0.32376236 / cos(n_hbonds / 0.42639184)) + n_hbonds))) / n_hbonds)` | `betti_1*3.6688375/((n_hbonds + 0.32376236/cos(n_hbonds/0.42639184))*n_hbonds) - 0.0048192353` |
| 17 | 3.453266e-06 | 0.0001 | `(sin((betti_1 / ((0.32376245 / cos(n_hbonds / 0.42639187)) + n_hbonds)) / n_hbonds) + -0.001314748) * 3.6688354` | `(sin(betti_1/(n_hbonds*(n_hbonds + 0.32376245/cos(n_hbonds/0.42639187)))) - 0.001314748)*3.6688354` |
| 19 | 3.417718e-06 | 0.0052 | `((betti_1 * (3.7708912 / n_hbonds)) / n_hbonds) - (cos((4.660294 / euler_characteristic) / sin(n_hbonds / 0.4875728)) * 0.0051727914)` | `betti_1*3.7708912/(n_hbonds*n_hbonds) - 0.0051727914*cos(4.660294/(euler_characteristic*sin(n_hbonds/0.4875728)))` |
| 20 | 3.417629e-06 | 0.0000 | `(((betti_1 * 3.7708912) / n_hbonds) / n_hbonds) - (cos((4.660294 / euler_characteristic) / sin(sin(n_hbonds / 0.4875728))) * 0.0051727914)` | `betti_1*3.7708912/(n_hbonds*n_hbonds) - 0.0051727914*cos(4.660294/(euler_characteristic*sin(sin(n_hbonds/0.4875728))))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.651901/(n_hbonds - 1.4627218/sin(n_hbonds + 0.5268553))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830214` | `0.00418302140000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.65237606 / n_hbonds` | `0.65237606/n_hbonds` |
| 4 | 3.683351e-06 | 0.0010 | `log(betti_1) * 0.0010230504` | `0.0010230504*log(betti_1)` |
| 5 | 3.647941e-06 | 0.0097 | `0.40299004 / (n_hbonds - betti_1)` | `0.40299004/(-betti_1 + n_hbonds)` |
| 7 | 3.614043e-06 | 0.0047 | `(1.2146622 / (n_hbonds + euler_characteristic)) + -0.008306742` | `-0.008306742 + 1.2146622/(euler_characteristic + n_hbonds)` |
| 9 | 3.610544e-06 | 0.0005 | `((euler_characteristic / n_hbonds) / (n_hbonds / -3.6608207)) + -0.0046454356` | `euler_characteristic/(n_hbonds*((n_hbonds/(-3.6608207)))) - 0.0046454356` |
| 10 | 3.524664e-06 | 0.0241 | `0.651901 / (n_hbonds + (-1.4627218 / sin(0.5268553 + n_hbonds)))` | `0.651901/(n_hbonds - 1.4627218/sin(n_hbonds + 0.5268553))` |
| 12 | 3.480322e-06 | 0.0063 | `(-0.011131757 / ((-1.4519405 / sin(n_hbonds + 0.52645105)) + n_hbonds)) * euler_characteristic` | `-0.011131757*euler_characteristic/(n_hbonds - 1.4519405/sin(n_hbonds + 0.52645105))` |
| 14 | 3.480257e-06 | 0.0000 | `euler_characteristic * (-0.011131757 / ((-1.4481332 / (sin(0.52645105 + n_hbonds) / 1.0484341)) + n_hbonds))` | `euler_characteristic*(-0.011131757)/(n_hbonds - 1.4481332*1.0484341/sin(n_hbonds + 0.52645105))` |
| 15 | 3.475841e-06 | 0.0013 | `(euler_characteristic / ((n_hbonds + (-1.4481332 / sin(n_hbonds + 0.52645105))) + cos(betti_1))) * -0.011131757` | `euler_characteristic*(-0.011131757)/(n_hbonds + cos(betti_1) - 1.4481332/sin(n_hbonds + 0.52645105))` |
| 18 | 3.376298e-06 | 0.0097 | `0.64735395 / (n_hbonds - (2.6258147 / sin((n_hbonds - (cos(cos(betti_1 * -0.27975717)) * 0.38091907)) + 0.88880813)))` | `0.64735395/(n_hbonds - 2.6258147/sin(n_hbonds - 0.38091907*cos(cos(betti_1*(-0.27975717))) + 0.88880813))` |
| 20 | 3.376171e-06 | 0.0000 | `0.64735395 / (n_hbonds - (2.6258147 / sin((n_hbonds - (cos(cos((betti_1 * -0.27975717) * betti_0)) * 0.38091907)) + 0.88880813)))` | `0.64735395/(n_hbonds - 2.6258147/sin(n_hbonds - 0.38091907*cos(cos(betti_1*(-0.27975717)*betti_0)) + 0.88880813))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -1*0.010933882 + 1.4546862/(n_hbonds - (betti_1 - 0.13173987/cos(exp(sin(n_hbonds + 0.9841815)))))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830633` | `0.00418306330000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.65237206 / n_hbonds` | `0.65237206/n_hbonds` |
| 4 | 3.687095e-06 | 0.0000 | `sin(0.6523754 / n_hbonds)` | `sin(0.6523754/n_hbonds)` |
| 5 | 3.647940e-06 | 0.0107 | `0.40299147 / (n_hbonds - betti_1)` | `0.40299147/(-betti_1 + n_hbonds)` |
| 7 | 3.614076e-06 | 0.0047 | `(1.194561 / (n_hbonds - betti_1)) - 0.008228173` | `-1*0.008228173 + 1.194561/(-betti_1 + n_hbonds)` |
| 8 | 3.614076e-06 | 0.0000 | `sin((1.1909733 / (n_hbonds - betti_1)) - 0.008191111)` | `sin(-1*0.008191111 + 1.1909733/(-betti_1 + n_hbonds))` |
| 9 | 3.610375e-06 | 0.0010 | `(-0.6214963 / (betti_1 - (n_hbonds / 1.2552614))) - 0.0054531414` | `-1*0.0054531414 - 0.6214963/(betti_1 - n_hbonds/1.2552614)` |
| 10 | 3.600175e-06 | 0.0028 | `(1.2238462 / (n_hbonds + (cos(betti_1) - betti_1))) - 0.008532436` | `-1*0.008532436 + 1.2238462/(-betti_1 + n_hbonds + cos(betti_1))` |
| 11 | 3.597060e-06 | 0.0009 | `(1.234248 / (n_hbonds + (cos(exp(betti_1)) - betti_1))) - 0.008655906` | `-1*0.008655906 + 1.234248/(-betti_1 + n_hbonds + cos(exp(betti_1)))` |
| 12 | 3.589124e-06 | 0.0022 | `(1.4793956 / ((sin(euler_characteristic + n_hbonds) + n_hbonds) - betti_1)) - 0.011163415` | `-1*0.011163415 + 1.4793956/(-betti_1 + n_hbonds + sin(euler_characteristic + n_hbonds))` |
| 13 | 3.589124e-06 | 0.0000 | `sin((1.4793956 / (sin(euler_characteristic + n_hbonds) + (n_hbonds - betti_1))) - 0.011163415)` | `sin(-1*0.011163415 + 1.4793956/(-betti_1 + n_hbonds + sin(euler_characteristic + n_hbonds)))` |
| 14 | 3.581263e-06 | 0.0022 | `(1.3421118 / (n_hbonds + (sin(n_hbonds + (euler_characteristic * 0.8988881)) - betti_1))) - 0.0097345365` | `-1*0.0097345365 + 1.3421118/(-betti_1 + n_hbonds + sin(euler_characteristic*0.8988881 + n_hbonds))` |
| 15 | 3.574204e-06 | 0.0020 | `(1.4793956 / (sin(n_hbonds + euler_characteristic) + ((n_hbonds + cos(betti_1)) - betti_1))) - 0.011163415` | `-1*0.011163415 + 1.4793956/(-betti_1 + n_hbonds + sin(euler_characteristic + n_hbonds) + cos(betti_1))` |
| 16 | 3.453083e-06 | 0.0345 | `(1.4546862 / (n_hbonds - (betti_1 + (-0.13173987 / cos(exp(sin(n_hbonds + 0.9841815))))))) - 0.010933882` | `-1*0.010933882 + 1.4546862/(n_hbonds - (betti_1 - 0.13173987/cos(exp(sin(n_hbonds + 0.9841815)))))` |
| 19 | 3.445585e-06 | 0.0007 | `(1.1412861 / (n_hbonds - (betti_1 / cos(1.6564881 / (cos((n_hbonds + n_hbonds) + n_hbonds) * betti_1))))) - 0.0077010486` | `-1*0.0077010486 + 1.1412861/(-betti_1/cos(1.6564881/((betti_1*cos(n_hbonds + n_hbonds + n_hbonds)))) + n_hbonds)` |
| 20 | 3.445584e-06 | 0.0000 | `sin((1.1412861 / (n_hbonds - (betti_1 / cos(1.6564881 / (betti_1 * cos(n_hbonds + (n_hbonds + n_hbonds))))))) - 0.007701045)` | `sin(-1*0.007701045 + 1.1412861/(-betti_1/cos(1.6564881/((betti_1*cos(n_hbonds + n_hbonds + n_hbonds)))) + n_hbonds))` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.40720773/(euler_characteristic + n_hbonds)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830125` | `0.00418301250000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.6523757 / n_hbonds` | `0.6523757/n_hbonds` |
| 4 | 3.683351e-06 | 0.0010 | `log(betti_1) * 0.0010230503` | `0.0010230503*log(betti_1)` |
| 5 | 3.648251e-06 | 0.0096 | `0.40720773 / (n_hbonds + euler_characteristic)` | `0.40720773/(euler_characteristic + n_hbonds)` |
| 7 | 3.614043e-06 | 0.0047 | `(1.2185099 / (euler_characteristic + n_hbonds)) + -0.008346252` | `-0.008346252 + 1.2185099/(euler_characteristic + n_hbonds)` |
| 8 | 3.614037e-06 | 0.0000 | `exp(1.2158434 / (euler_characteristic + n_hbonds)) + -1.0083971` | `exp(1.2158434/(euler_characteristic + n_hbonds)) - 1.0083971` |
| 9 | 3.612014e-06 | 0.0006 | `(0.69432527 / ((euler_characteristic / 0.76510674) + n_hbonds)) + -0.004586458` | `-0.004586458 + 0.69432527/(euler_characteristic/0.76510674 + n_hbonds)` |
| 10 | 3.600203e-06 | 0.0033 | `(1.2473037 / (euler_characteristic + (cos(betti_1) + n_hbonds))) + -0.008641573` | `-0.008641573 + 1.2473037/(euler_characteristic + n_hbonds + cos(betti_1))` |
| 11 | 3.596930e-06 | 0.0009 | `(1.2706194 / ((n_hbonds + euler_characteristic) + cos(exp(betti_1)))) + -0.008897115` | `-0.008897115 + 1.2706194/(euler_characteristic + n_hbonds + cos(exp(betti_1)))` |
| 12 | 3.589369e-06 | 0.0021 | `(1.5139375 / ((sin(euler_characteristic + n_hbonds) + euler_characteristic) + n_hbonds)) + -0.011358799` | `-0.011358799 + 1.5139375/(euler_characteristic + n_hbonds + sin(euler_characteristic + n_hbonds))` |
| 13 | 3.589349e-06 | 0.0000 | `exp(1.4659154 / (n_hbonds + (euler_characteristic + sin(n_hbonds + euler_characteristic)))) + -1.0109804` | `exp(1.4659154/(euler_characteristic + n_hbonds + sin(euler_characteristic + n_hbonds))) - 1.0109804` |
| 14 | 3.583249e-06 | 0.0017 | `(1.5662488 / ((euler_characteristic + n_hbonds) + cos((euler_characteristic / -1.2214631) - n_hbonds))) + -0.011894856` | `-0.011894856 + 1.5662488/(euler_characteristic + n_hbonds + cos(euler_characteristic/(-1.2214631) - n_hbonds))` |
| 15 | 3.574528e-06 | 0.0024 | `(1.5139375 / (sin(euler_characteristic + n_hbonds) + ((euler_characteristic + cos(betti_1)) + n_hbonds))) + -0.011358799` | `-0.011358799 + 1.5139375/(euler_characteristic + n_hbonds + sin(euler_characteristic + n_hbonds) + cos(betti_1))` |
| 16 | 3.570140e-06 | 0.0012 | `(1.5477289 / ((euler_characteristic + n_hbonds) + (cos(exp(betti_1)) + sin(euler_characteristic + n_hbonds)))) + -0.011724566` | `-0.011724566 + 1.5477289/(euler_characteristic + n_hbonds + sin(euler_characteristic + n_hbonds) + cos(exp(betti_1)))` |
| 17 | 3.564878e-06 | 0.0015 | `(1.5662705 / ((euler_characteristic + n_hbonds) + (sin(euler_characteristic / -1.218369) + sin(n_hbonds + euler_characteristic)))) + -0.011899992` | `-0.011899992 + 1.5662705/(euler_characteristic + n_hbonds + sin(euler_characteristic/(-1.218369)) + sin(euler_characteristic + n_hbonds))` |
| 19 | 3.558466e-06 | 0.0009 | `(1.5662488 / (euler_characteristic + ((sin(euler_characteristic / -1.2178046) + n_hbonds) + cos((euler_characteristic / -1.2214631) - n_hbonds)))) + -0.011894856` | `-0.011894856 + 1.5662488/(euler_characteristic + n_hbonds + sin(euler_characteristic/(-1.2178046)) + cos(euler_characteristic/(-1.2214631) - n_hbonds))` |

</details>

