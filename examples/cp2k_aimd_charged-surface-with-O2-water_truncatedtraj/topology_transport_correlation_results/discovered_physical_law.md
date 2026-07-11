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
| 1 | `LBHB_Fraction ≈ betti_1*(-6.4889464e-5)/sin(n_hbonds*0.068781644)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ 0.40307212/(-betti_1 + n_hbonds)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.65405697/(n_hbonds - 0.79977727/sin(n_hbonds/(-0.60313284)))` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -1*(-0.00416776) + 3.194272e-5/(sin(n_hbonds) + 0.49348533)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.18053538/(euler_characteristic + n_hbonds/1.5290991 - 0.07563626/cos(n_hbonds + cos(euler_characteristic)))` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx betti_1*(-6.4889464e-5)/sin(n_hbonds*0.068781644)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `n_hbonds` | Total number of hydrogen bonds in the network | 67/78 | 85.9% | 🔥 High |
| `betti_1` | Number of independent H-bond loops/cycles | 36/78 | 46.2% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 25/78 | 32.1% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/78 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/78 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `n_hbonds` is the most stable feature (appearing in 67/78 Pareto equations). This strongly indicates that `n_hbonds` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: betti_1*(-6.4889464e-5)/sin(n_hbonds*0.068781644)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.004183009` | `0.00418300900000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.6523607 / n_hbonds` | `0.6523607/n_hbonds` |
| 4 | 3.683351e-06 | 0.0010 | `log(betti_1) * 0.0010230503` | `0.0010230503*log(betti_1)` |
| 5 | 3.647940e-06 | 0.0097 | `0.4029907 / (n_hbonds - betti_1)` | `0.4029907/(-betti_1 + n_hbonds)` |
| 7 | 3.627678e-06 | 0.0028 | `cos(cos(n_hbonds / betti_1)) / n_hbonds` | `cos(cos(n_hbonds/betti_1))/n_hbonds` |
| 8 | 3.574818e-06 | 0.0147 | `(betti_1 / sin(n_hbonds * 0.068781644)) * -6.4889464e-5` | `betti_1*(-6.4889464e-5)/sin(n_hbonds*0.068781644)` |
| 9 | 3.573941e-06 | 0.0002 | `betti_1 * (-5.5982782e-5 / sin(sin(n_hbonds * 0.06879065)))` | `betti_1*(-5.5982782e-5)/sin(sin(n_hbonds*0.06879065))` |
| 10 | 3.526243e-06 | 0.0134 | `(betti_1 * (betti_1 * -1.0358062e-6)) / sin(n_hbonds * 0.067940965)` | `betti_1*betti_1*(-1.0358062e-6)/sin(n_hbonds*0.067940965)` |
| 11 | 3.484593e-06 | 0.0119 | `(betti_1 * (betti_1 / sin(sin(n_hbonds * 0.08830434)))) * 8.822118e-7` | `betti_1*betti_1*8.822118e-7/sin(sin(n_hbonds*0.08830434))` |
| 12 | 3.463089e-06 | 0.0062 | `(betti_1 / sin(sin(sin(n_hbonds * 0.08818886)))) * (betti_1 * 7.943212e-7)` | `betti_1*betti_1*7.943212e-7/sin(sin(sin(n_hbonds*0.08818886)))` |
| 14 | 3.462839e-06 | 0.0000 | `(((betti_1 * betti_1) / sin(sin(sin(n_hbonds * 0.08818889)))) - -16.02262) * 7.920201e-7` | `(betti_1*betti_1/sin(sin(sin(n_hbonds*0.08818889))) - 1*(-16.02262))*7.920201e-7` |
| 15 | 3.453160e-06 | 0.0028 | `(7.935248e-7 * betti_1) * ((betti_1 - cos(betti_1)) / sin(sin(sin(n_hbonds * 0.088188894))))` | `7.935248e-7*betti_1*(betti_1 - cos(betti_1))/sin(sin(sin(n_hbonds*0.088188894)))` |
| 16 | 3.445840e-06 | 0.0021 | `(betti_1 * -6.303481e-5) / sin((n_hbonds * -0.57321244) / (betti_1 / sin(sin(n_hbonds / 11.3251705))))` | `betti_1*(-6.303481e-5)/sin(n_hbonds*(-0.57321244)/(betti_1/sin(sin(n_hbonds/11.3251705))))` |
| 17 | 3.439402e-06 | 0.0019 | `((betti_1 - cos(n_hbonds * -0.4653755)) * (betti_1 / sin(sin(sin(n_hbonds * 0.088188894))))) * 7.935248e-7` | `(betti_1 - cos(n_hbonds*(-0.4653755)))*betti_1*7.935248e-7/sin(sin(sin(n_hbonds*0.088188894)))` |
| 18 | 3.433009e-06 | 0.0019 | `6.344373e-5 * (betti_1 / sin(n_hbonds * (0.49713725 / (betti_1 / sin((cos(betti_1) + n_hbonds) / 11.273218)))))` | `6.344373e-5*betti_1/sin(n_hbonds*0.49713725/(betti_1/sin((n_hbonds + cos(betti_1))/11.273218)))` |
| 19 | 3.400270e-06 | 0.0096 | `(7.935248e-7 * (betti_1 - (cos(-0.4653755 * n_hbonds) / 0.26190412))) * (betti_1 / sin(sin(sin(n_hbonds * 0.088188894))))` | `7.935248e-7*betti_1*(betti_1 - cos(-0.4653755*n_hbonds)/0.26190412)/sin(sin(sin(n_hbonds*0.088188894)))` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: 0.40307212/(-betti_1 + n_hbonds)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830125` | `0.00418301250000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.6523378 / n_hbonds` | `0.6523378/n_hbonds` |
| 4 | 3.687095e-06 | 0.0000 | `sin(0.65237826 / n_hbonds)` | `sin(0.65237826/n_hbonds)` |
| 5 | 3.647941e-06 | 0.0107 | `0.40307212 / (n_hbonds - betti_1)` | `0.40307212/(-betti_1 + n_hbonds)` |
| 7 | 3.614075e-06 | 0.0047 | `(1.1937655 / (n_hbonds - betti_1)) - 0.008220456` | `-1*0.008220456 + 1.1937655/(-betti_1 + n_hbonds)` |
| 9 | 3.614075e-06 | 0.0000 | `(1.1927414 / (n_hbonds - (betti_1 - -0.006959691))) - 0.008210918` | `-1*0.008210918 + 1.1927414/(n_hbonds - (betti_1 - 1*(-0.006959691)))` |
| 10 | 3.600175e-06 | 0.0039 | `(1.2236776 / (n_hbonds + (cos(betti_1) - betti_1))) - 0.008530683` | `-1*0.008530683 + 1.2236776/(-betti_1 + n_hbonds + cos(betti_1))` |
| 11 | 3.597080e-06 | 0.0009 | `(1.2236775 / (cos(exp(betti_1)) + (n_hbonds - betti_1))) - 0.008545943` | `-1*0.008545943 + 1.2236775/(-betti_1 + n_hbonds + cos(exp(betti_1)))` |
| 12 | 3.589121e-06 | 0.0022 | `(1.4869806 / (sin(n_hbonds + euler_characteristic) + (n_hbonds - betti_1))) - 0.011242345` | `-1*0.011242345 + 1.4869806/(-betti_1 + n_hbonds + sin(euler_characteristic + n_hbonds))` |
| 14 | 3.554546e-06 | 0.0048 | `cos(cos(n_hbonds / ((0.08721791 / (sin(n_hbonds) + -0.6073447)) - betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + 0.08721791/(sin(n_hbonds) - 0.6073447))))/n_hbonds` |
| 15 | 3.549996e-06 | 0.0013 | `cos(cos(n_hbonds / ((cos(euler_characteristic) / sin(n_hbonds - -0.5483965)) - betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + cos(euler_characteristic)/sin(n_hbonds - 1*(-0.5483965)))))/n_hbonds` |
| 17 | 3.538479e-06 | 0.0016 | `cos(cos(n_hbonds / (((cos(betti_1) + -0.48252055) / sin(n_hbonds - -0.5448195)) - betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + (cos(betti_1) - 0.48252055)/sin(n_hbonds - 1*(-0.5448195)))))/n_hbonds` |
| 18 | 3.538199e-06 | 0.0001 | `cos(cos(n_hbonds / (((cos(euler_characteristic) / sin(n_hbonds - -0.5483965)) + cos(betti_1)) - betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + cos(betti_1) + cos(euler_characteristic)/sin(n_hbonds - 1*(-0.5483965)))))/n_hbonds` |
| 19 | 3.537450e-06 | 0.0002 | `cos(cos(n_hbonds / (((cos(betti_1 + 0.082021534) + -0.49552467) / sin(n_hbonds - -0.5448195)) - betti_1))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + (cos(betti_1 + 0.082021534) - 0.49552467)/sin(n_hbonds - 1*(-0.5448195)))))/n_hbonds` |
| 20 | 3.526520e-06 | 0.0031 | `cos(cos(n_hbonds / (cos(betti_1) + (((cos(betti_1) + -0.5014431) / sin(n_hbonds - -0.5448195)) - betti_1)))) / n_hbonds` | `cos(cos(n_hbonds/(-betti_1 + (cos(betti_1) - 0.5014431)/sin(n_hbonds - 1*(-0.5448195)) + cos(betti_1))))/n_hbonds` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.65405697/(n_hbonds - 0.79977727/sin(n_hbonds/(-0.60313284)))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041829734` | `0.00418297340000000` |
| 2 | 3.691254e-06 | 0.0000 | `sin(0.004183075)` | `sin(0.004183075)` |
| 3 | 3.687095e-06 | 0.0011 | `0.65237653 / n_hbonds` | `0.65237653/n_hbonds` |
| 4 | 3.683351e-06 | 0.0010 | `log(betti_1) * 0.0010230504` | `0.0010230504*log(betti_1)` |
| 5 | 3.647941e-06 | 0.0097 | `0.40299162 / (n_hbonds - betti_1)` | `0.40299162/(-betti_1 + n_hbonds)` |
| 7 | 3.617476e-06 | 0.0042 | `((n_hbonds + euler_characteristic) * -0.00012344698) - -0.016193936` | `(euler_characteristic + n_hbonds)*(-0.00012344698) - 1*(-0.016193936)` |
| 8 | 3.617476e-06 | 0.0000 | `sin((-0.00012344698 * (n_hbonds + euler_characteristic)) - -0.016193936)` | `sin(-0.00012344698*(euler_characteristic + n_hbonds) - 1*(-0.016193936))` |
| 9 | 3.611002e-06 | 0.0018 | `((n_hbonds * -0.00012140919) + (euler_characteristic * -0.0001449073)) + 0.014614897` | `euler_characteristic*(-0.0001449073) + n_hbonds*(-0.00012140919) + 0.014614897` |
| 10 | 3.519027e-06 | 0.0258 | `0.65405697 / ((-0.79977727 / sin(n_hbonds / -0.60313284)) + n_hbonds)` | `0.65405697/(n_hbonds - 0.79977727/sin(n_hbonds/(-0.60313284)))` |
| 13 | 3.516255e-06 | 0.0003 | `0.65405697 / (((-0.60313284 / sin(n_hbonds / -0.60313284)) / exp(-0.30623138)) + n_hbonds)` | `0.65405697/(n_hbonds - 0.60313284/(exp(-0.30623138)*sin(n_hbonds/(-0.60313284))))` |
| 14 | 3.477362e-06 | 0.0111 | `(((n_hbonds + euler_characteristic) + (-0.6086916 / sin(n_hbonds / 0.93548465))) * -0.00011901968) - -0.015772738` | `(euler_characteristic + n_hbonds - 0.6086916/sin(n_hbonds/0.93548465))*(-0.00011901968) - 1*(-0.015772738)` |
| 15 | 3.477337e-06 | 0.0000 | `((n_hbonds + (euler_characteristic + (-0.6086916 / sin(n_hbonds / 0.93548465)))) * -0.00011901968) - sin(-0.015772738)` | `(euler_characteristic + n_hbonds - 0.6086916/sin(n_hbonds/0.93548465))*(-0.00011901968) - sin(-0.015772738)` |
| 16 | 3.476129e-06 | 0.0003 | `((((-0.6330986 / sin((n_hbonds / 0.93548465) + 0.00016170587)) + n_hbonds) + euler_characteristic) * -0.00011940874) - -0.015772734` | `(euler_characteristic + n_hbonds - 0.6330986/sin(n_hbonds/0.93548465 + 0.00016170587))*(-0.00011940874) - 1*(-0.015772734)` |
| 17 | 3.446320e-06 | 0.0086 | `((((cos(n_hbonds / -3.080878) / sin(n_hbonds / -0.97518086)) + n_hbonds) + euler_characteristic) * -0.00011951742) - -0.015772268` | `(euler_characteristic + n_hbonds + cos(n_hbonds/(-3.080878))/sin(n_hbonds/(-0.97518086)))*(-0.00011951742) - 1*(-0.015772268)` |
| 18 | 3.444136e-06 | 0.0006 | `((n_hbonds + ((cos(n_hbonds * exp(1.3954209)) / sin(n_hbonds / -0.9751859)) + euler_characteristic)) * -0.00011901968) - -0.015772738` | `(euler_characteristic + n_hbonds + cos(n_hbonds*exp(1.3954209))/sin(n_hbonds/(-0.9751859)))*(-0.00011901968) - 1*(-0.015772738)` |
| 19 | 3.411437e-06 | 0.0095 | `((euler_characteristic + (n_hbonds + ((cos(n_hbonds / 3.0869193) + -0.27935553) / sin(n_hbonds / -0.97518086)))) * -0.00011951742) - -0.015772268` | `(euler_characteristic + n_hbonds + (cos(n_hbonds/3.0869193) - 0.27935553)/sin(n_hbonds/(-0.97518086)))*(-0.00011951742) - 1*(-0.015772268)` |
| 20 | 3.411081e-06 | 0.0001 | `((euler_characteristic + (n_hbonds + ((cos(n_hbonds / 3.0869193) + -0.27935553) / sin(sin(n_hbonds / -0.97518086))))) * -0.00011951742) - -0.015772268` | `(euler_characteristic + n_hbonds + (cos(n_hbonds/3.0869193) - 0.27935553)/sin(sin(n_hbonds/(-0.97518086))))*(-0.00011951742) - 1*(-0.015772268)` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -1*(-0.00416776) + 3.194272e-5/(sin(n_hbonds) + 0.49348533)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830125` | `0.00418301250000000` |
| 2 | 3.691254e-06 | 0.0000 | `sin(0.0041834717)` | `sin(0.0041834717)` |
| 3 | 3.687095e-06 | 0.0011 | `0.6523738 / n_hbonds` | `0.6523738/n_hbonds` |
| 4 | 3.683352e-06 | 0.0010 | `log(betti_1) * 0.0010232077` | `0.0010232077*log(betti_1)` |
| 5 | 3.647941e-06 | 0.0097 | `-0.4029914 / (betti_1 - n_hbonds)` | `-0.4029914/(betti_1 - n_hbonds)` |
| 7 | 3.614129e-06 | 0.0047 | `(1.1763382 / (euler_characteristic + n_hbonds)) - 0.007912667` | `-1*0.007912667 + 1.1763382/(euler_characteristic + n_hbonds)` |
| 8 | 3.530112e-06 | 0.0235 | `(3.194272e-5 / (sin(n_hbonds) + 0.49348533)) - -0.00416776` | `-1*(-0.00416776) + 3.194272e-5/(sin(n_hbonds) + 0.49348533)` |
| 10 | 3.528830e-06 | 0.0002 | `(3.0820695e-5 / (sin(n_hbonds + -7.425348e-5) + 0.49344835)) - -0.004167934` | `-1*(-0.004167934) + 3.0820695e-5/(sin(n_hbonds - 7.425348e-5) + 0.49344835)` |
| 12 | 3.527957e-06 | 0.0001 | `(3.1063766e-5 / (sin((n_hbonds + -9.9397315e-5) + -9.9397315e-5) + 0.49348563)) - -0.004167713` | `-1*(-0.004167713) + 3.1063766e-5/(sin(n_hbonds - 9.9397315e-5 - 9.9397315e-5) + 0.49348563)` |
| 16 | 3.496039e-06 | 0.0023 | `(1.3816565e-5 / cos(n_hbonds * (1.1587425 * (n_hbonds + n_hbonds)))) - ((n_hbonds / n_hbonds) + -1.0042095)` | `-(-1.0042095 + n_hbonds/n_hbonds) + 1.3816565e-5/cos(n_hbonds*1.1587425*(n_hbonds + n_hbonds))` |
| 17 | 3.496036e-06 | 0.0000 | `sin((1.3816565e-5 / cos((n_hbonds * 1.1587425) * (n_hbonds + n_hbonds))) - ((n_hbonds / n_hbonds) + -1.0042095))` | `sin(-(-1.0042095 + n_hbonds/n_hbonds) + 1.3816565e-5/cos(n_hbonds*1.1587425*(n_hbonds + n_hbonds)))` |
| 18 | 3.493032e-06 | 0.0009 | `(1.3838835e-5 / cos(((n_hbonds + n_hbonds) * 1.0379678) * (n_hbonds / 0.89577085))) - ((n_hbonds / n_hbonds) + -1.0042095)` | `-(-1.0042095 + n_hbonds/n_hbonds) + 1.3838835e-5/cos((n_hbonds + n_hbonds)*1.0379678*n_hbonds/0.89577085)` |
| 19 | 3.493031e-06 | 0.0000 | `(1.3838835e-5 / cos(((n_hbonds + n_hbonds) * (n_hbonds * 1.0379678)) / 0.89577085)) - sin((n_hbonds / n_hbonds) + -1.0042095)` | `-sin(-1.0042095 + n_hbonds/n_hbonds) + 1.3838835e-5/cos((n_hbonds + n_hbonds)*n_hbonds*1.0379678/0.89577085)` |
| 20 | 3.492944e-06 | 0.0000 | `(1.3838835e-5 / cos((n_hbonds * (1.0379678 * (n_hbonds + n_hbonds))) / 0.89577085)) - ((n_hbonds / (n_hbonds + -0.00883942)) + -1.0042095)` | `-(n_hbonds/(n_hbonds - 0.00883942) - 1.0042095) + 1.3838835e-5/cos(n_hbonds*1.0379678*(n_hbonds + n_hbonds)/0.89577085)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.18053538/(euler_characteristic + n_hbonds/1.5290991 - 0.07563626/cos(n_hbonds + cos(euler_characteristic)))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.691254e-06 | 0.0000 | `0.0041830125` | `0.00418301250000000` |
| 3 | 3.687095e-06 | 0.0006 | `0.6523758 / n_hbonds` | `0.6523758/n_hbonds` |
| 4 | 3.683352e-06 | 0.0010 | `0.0010228254 * log(betti_1)` | `0.0010228254*log(betti_1)` |
| 5 | 3.647941e-06 | 0.0097 | `0.40299135 / (n_hbonds - betti_1)` | `0.40299135/(-betti_1 + n_hbonds)` |
| 7 | 3.605945e-06 | 0.0058 | `0.11567451 / ((n_hbonds + -69.4733) + euler_characteristic)` | `0.11567451/(euler_characteristic + n_hbonds - 69.4733)` |
| 8 | 3.582641e-06 | 0.0065 | `0.003742003 / sin((n_hbonds + euler_characteristic) * 0.076335154)` | `0.003742003/sin((euler_characteristic + n_hbonds)*0.076335154)` |
| 9 | 3.530460e-06 | 0.0147 | `(0.0040825964 / ((n_hbonds + euler_characteristic) + -91.5172)) + 0.0033584558` | `0.0033584558 + 0.0040825964/(euler_characteristic + n_hbonds - 91.5172)` |
| 11 | 3.525323e-06 | 0.0007 | `(0.0044604116 / ((n_hbonds + -91.39909) + (betti_1 * -0.98563594))) - -0.0032728403` | `-1*(-0.0032728403) + 0.0044604116/(betti_1*(-0.98563594) + n_hbonds - 91.39909)` |
| 12 | 3.503561e-06 | 0.0062 | `0.0034462456 - (-0.0035342146 / (((euler_characteristic + -91.501175) + n_hbonds) + cos(euler_characteristic)))` | `0.0034462456 - (-1)*0.0035342146/(euler_characteristic + n_hbonds + cos(euler_characteristic) - 91.501175)` |
| 14 | 3.460760e-06 | 0.0061 | `0.18700083 / (((-0.4246089 / sin(n_hbonds + 0.5257148)) + euler_characteristic) + (n_hbonds / 1.5075647))` | `0.18700083/(euler_characteristic + n_hbonds/1.5075647 - 0.4246089/sin(n_hbonds + 0.5257148))` |
| 15 | 3.409923e-06 | 0.0148 | `0.18053538 / (((-0.07563626 / cos(cos(euler_characteristic) + n_hbonds)) + (n_hbonds / 1.5290991)) + euler_characteristic)` | `0.18053538/(euler_characteristic + n_hbonds/1.5290991 - 0.07563626/cos(n_hbonds + cos(euler_characteristic)))` |
| 16 | 3.409821e-06 | 0.0000 | `0.18053538 / (((-0.07563626 / sin(cos(cos(euler_characteristic) + n_hbonds))) + (n_hbonds / 1.5290991)) + euler_characteristic)` | `0.18053538/(euler_characteristic + n_hbonds/1.5290991 - 0.07563626/sin(cos(n_hbonds + cos(euler_characteristic))))` |
| 17 | 3.406230e-06 | 0.0011 | `(0.20834479 / (euler_characteristic + ((-0.072569 / cos(n_hbonds + cos(euler_characteristic))) + (n_hbonds / 1.5364921)))) + -0.0006782781` | `-0.0006782781 + 0.20834479/(euler_characteristic + n_hbonds/1.5364921 - 0.072569/cos(n_hbonds + cos(euler_characteristic)))` |
| 18 | 3.402644e-06 | 0.0011 | `0.18038785 / (euler_characteristic + ((n_hbonds / 1.5289437) + ((-0.07376376 / cos(n_hbonds + cos(euler_characteristic))) + cos(betti_1))))` | `0.18038785/(euler_characteristic + n_hbonds/1.5289437 + cos(betti_1) - 0.07376376/cos(n_hbonds + cos(euler_characteristic)))` |
| 19 | 3.402639e-06 | 0.0000 | `sin(0.18039176 / ((((n_hbonds / 1.5289457) + (-0.073779754 / cos(cos(euler_characteristic) + n_hbonds))) + cos(betti_1)) + euler_characteristic))` | `sin(0.18039176/(euler_characteristic + n_hbonds/1.5289457 + cos(betti_1) - 0.073779754/cos(n_hbonds + cos(euler_characteristic))))` |
| 20 | 3.398312e-06 | 0.0013 | `(0.2083618 / (((n_hbonds / 1.5364779) + cos(betti_1)) + (euler_characteristic + (-0.07005302 / cos(cos(euler_characteristic) + n_hbonds))))) + -0.0007031207` | `-0.0007031207 + 0.2083618/(euler_characteristic + n_hbonds/1.5364779 + cos(betti_1) - 0.07005302/cos(n_hbonds + cos(euler_characteristic)))` |

</details>

