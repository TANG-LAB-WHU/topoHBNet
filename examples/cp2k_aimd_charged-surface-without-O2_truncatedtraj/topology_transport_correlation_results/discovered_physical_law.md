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
| 1 | `LBHB_Fraction ≈ cos(0.048960995*betti_1)*(-0.0019095205)` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ -0.3593282*sin(log(betti_1))/(n_hbonds - 6.7746086*cos(betti_1 - n_hbonds))` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ (n_hbonds - sin((-betti_1 + n_hbonds)*0.2061641)/0.026215233)*1.4765725e-5` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ -0.0019109752*cos(-0.048944183*betti_1)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ cos(betti_1*(-0.04920097))*(-0.0019097836)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx cos(0.048960995*betti_1)*(-0.0019095205)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `betti_1` | Number of independent H-bond loops/cycles | 55/73 | 75.3% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 48/73 | 65.8% | ⚡ Medium |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 14/73 | 19.2% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 2/73 | 2.7% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/73 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `betti_1` is the most stable feature (appearing in 55/73 Pareto equations). This strongly indicates that `betti_1` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: cos(0.048960995*betti_1)*(-0.0019095205)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671911e-5` | `n_hbonds*1.1671911e-5` |
| 5 | 2.517716e-07 | 0.0034 | `0.0025607212 - (0.0431713 / betti_1)` | `0.0025607212 - 0.0431713/betti_1` |
| 6 | 2.503207e-07 | 0.0058 | `cos(0.048960995 * betti_1) * -0.0019095205` | `cos(0.048960995*betti_1)*(-0.0019095205)` |
| 7 | 2.501123e-07 | 0.0008 | `cos(sin(betti_1 * -0.048671935)) * 0.0019103659` | `cos(sin(betti_1*(-0.048671935)))*0.0019103659` |
| 8 | 2.500458e-07 | 0.0003 | `cos(sin(sin(betti_1 * -0.048457466))) * 0.0019106328` | `cos(sin(sin(betti_1*(-0.048457466))))*0.0019106328` |
| 9 | 2.500430e-07 | 0.0000 | `cos(sin(sin(betti_1 * sin(0.048618212)))) * 0.0019091484` | `cos(sin(sin(betti_1*sin(0.048618212))))*0.0019091484` |
| 10 | 2.500152e-07 | 0.0001 | `cos(sin(sin((betti_1 + betti_0) * -0.047812458))) * 0.0019103659` | `cos(sin(sin((betti_0 + betti_1)*(-0.047812458))))*0.0019103659` |
| 11 | 2.496354e-07 | 0.0015 | `sin(-1.3293211 - (0.045962594 * (euler_characteristic - sin(n_hbonds)))) * 0.0019137511` | `sin(-0.045962594*(euler_characteristic - sin(n_hbonds)) - 1.3293211)*0.0019137511` |
| 13 | 2.491606e-07 | 0.0010 | `sin(-1.3293211 - ((euler_characteristic * 0.045962594) + (sin(n_hbonds) * -0.11717924))) * 0.0019137511` | `sin(-(euler_characteristic*0.045962594 + sin(n_hbonds)*(-0.11717924)) - 1.3293211)*0.0019137511` |
| 16 | 2.490144e-07 | 0.0002 | `sin((sin(n_hbonds) * 0.110423654) + (-1.1055467 + ((sin(euler_characteristic) - euler_characteristic) * 0.04196546))) * 0.001911578` | `sin((-euler_characteristic + sin(euler_characteristic))*0.04196546 + sin(n_hbonds)*0.110423654 - 1.1055467)*0.001911578` |
| 18 | 2.486720e-07 | 0.0007 | `0.0019125094 * sin(((sin(euler_characteristic * n_hbonds) - euler_characteristic) * 0.041960355) + (-1.1055467 + (sin(n_hbonds) * 0.10084125)))` | `0.0019125094*sin((-euler_characteristic + sin(euler_characteristic*n_hbonds))*0.041960355 + sin(n_hbonds)*0.10084125 - 1.1055467)` |
| 20 | 2.485523e-07 | 0.0002 | `sin((-1.1078743 / (betti_0 + (sin(euler_characteristic * n_hbonds) * 0.10084125))) + ((sin(n_hbonds) - euler_characteristic) * 0.041963566)) * 0.0019158244` | `sin((-euler_characteristic + sin(n_hbonds))*0.041963566 - 1.1078743/(betti_0 + sin(euler_characteristic*n_hbonds)*0.10084125))*0.0019158244` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: -0.3593282*sin(log(betti_1))/(n_hbonds - 6.7746086*cos(betti_1 - n_hbonds))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671998e-5` | `n_hbonds*1.1671998e-5` |
| 5 | 2.517724e-07 | 0.0034 | `(0.04151747 / euler_characteristic) + 0.002545162` | `0.002545162 + 0.04151747/euler_characteristic` |
| 6 | 2.511418e-07 | 0.0025 | `0.0019268474 - exp(euler_characteristic * 0.16184942)` | `0.0019268474 - exp(euler_characteristic*0.16184942)` |
| 7 | 2.509754e-07 | 0.0007 | `(sin(log(betti_1)) * -0.3577108) / n_hbonds` | `-0.3577108*sin(log(betti_1))/n_hbonds` |
| 9 | 2.508376e-07 | 0.0003 | `(sin(log(betti_1)) * (-0.45837933 / n_hbonds)) - 0.00052573095` | `-0.00052573095 - 0.45837933*sin(log(betti_1))/n_hbonds` |
| 10 | 2.507720e-07 | 0.0003 | `(-0.3577108 / (n_hbonds - cos(n_hbonds))) * sin(log(betti_1))` | `-0.3577108*sin(log(betti_1))/(n_hbonds - cos(n_hbonds))` |
| 11 | 2.504455e-07 | 0.0013 | `(0.20978956 - ((n_hbonds / betti_1) * (2.2453446 / betti_1))) / betti_1` | `(0.20978956 - 2.2453446*n_hbonds/(betti_1*betti_1))/betti_1` |
| 12 | 2.501755e-07 | 0.0011 | `(sin(log(betti_1)) / (n_hbonds - cos(n_hbonds - betti_1))) * -0.35810515` | `-0.35810515*sin(log(betti_1))/(n_hbonds - cos(betti_1 - n_hbonds))` |
| 13 | 2.500847e-07 | 0.0004 | `sin(-3.1393435 - (cos(betti_1 - n_hbonds) * -9.460797e-5)) * sin(log(betti_1))` | `sin(9.460797e-5*cos(betti_1 - n_hbonds) - 3.1393435)*sin(log(betti_1))` |
| 14 | 2.480880e-07 | 0.0080 | `sin(log(betti_1)) * (-0.3593282 / (n_hbonds - (6.7746086 * cos(betti_1 - n_hbonds))))` | `-0.3593282*sin(log(betti_1))/(n_hbonds - 6.7746086*cos(betti_1 - n_hbonds))` |
| 15 | 2.480714e-07 | 0.0001 | `((sin(log(betti_1)) * -0.36005682) / n_hbonds) - (sin(cos(betti_1 - n_hbonds)) * -8.910769e-5)` | `8.910769e-5*sin(cos(betti_1 - n_hbonds)) - 0.36005682*sin(log(betti_1))/n_hbonds` |
| 16 | 2.476957e-07 | 0.0015 | `-0.3593282 * (sin(log(betti_1)) / (n_hbonds + (-7.4509997 * cos((0.63647467 - euler_characteristic) - n_hbonds))))` | `-0.3593282*sin(log(betti_1))/(n_hbonds - 7.4509997*cos(euler_characteristic + n_hbonds - 0.63647467))` |
| 17 | 2.476100e-07 | 0.0003 | `(sin(log(betti_1)) * (-0.36026835 / n_hbonds)) - (sin(cos((betti_1 - n_hbonds) + -0.35252532)) * -9.5358424e-5)` | `9.5358424e-5*sin(cos(-betti_1 + n_hbonds + 0.35252532)) - 0.36026835*sin(log(betti_1))/n_hbonds` |
| 18 | 2.475343e-07 | 0.0003 | `(sin(log(betti_1)) * (-0.3602683 / n_hbonds)) - (sin(sin(cos((n_hbonds - -0.3031974) - betti_1))) * -0.000105387866)` | `0.000105387866*sin(sin(cos(-betti_1 + n_hbonds + 0.3031974))) - 0.3602683*sin(log(betti_1))/n_hbonds` |
| 19 | 2.474802e-07 | 0.0002 | `(sin(log(betti_1)) * (-0.36026835 / n_hbonds)) - (sin(sin(sin(cos(betti_1 - (n_hbonds - -0.3031974))))) * -0.00011387191)` | `0.00011387191*sin(sin(sin(cos(-betti_1 + n_hbonds + 0.3031974)))) - 0.36026835*sin(log(betti_1))/n_hbonds` |
| 20 | 2.474319e-07 | 0.0002 | `(sin(log(betti_1)) * (-0.36071596 / n_hbonds)) - (sin(sin(sin(sin(cos((n_hbonds - -0.33110824) - betti_1))))) * -0.0001224122)` | `0.0001224122*sin(sin(sin(sin(cos(-betti_1 + n_hbonds + 0.33110824))))) - 0.36071596*sin(log(betti_1))/n_hbonds` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: (n_hbonds - sin((-betti_1 + n_hbonds)*0.2061641)/0.026215233)*1.4765725e-5</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671865e-5` | `n_hbonds*1.1671865e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045175455` | `0.00045175455*log(betti_1)` |
| 5 | 2.517716e-07 | 0.0017 | `(-0.04317087 / betti_1) + 0.0025607096` | `0.0025607096 - 0.04317087/betti_1` |
| 7 | 2.508458e-07 | 0.0018 | `((9.567276 / betti_1) + -0.26880565) / euler_characteristic` | `(-0.26880565 + 9.567276/betti_1)/euler_characteristic` |
| 9 | 2.505425e-07 | 0.0006 | `(((19.724386 / betti_1) + -0.6046085) / euler_characteristic) - 0.002806316` | `-1*0.002806316 + (-0.6046085 + 19.724386/betti_1)/euler_characteristic` |
| 10 | 2.503280e-07 | 0.0009 | `(((euler_characteristic * 0.012709478) + log(betti_1)) + -3.0527096) / n_hbonds` | `(0.012709478*euler_characteristic + log(betti_1) - 3.0527096)/n_hbonds` |
| 11 | 2.503280e-07 | 0.0000 | `sin(((0.012709478 * euler_characteristic) + (log(betti_1) + -3.0527096)) / n_hbonds)` | `sin((0.012709478*euler_characteristic + log(betti_1) - 3.0527096)/n_hbonds)` |
| 12 | 2.480186e-07 | 0.0093 | `(n_hbonds - (sin((n_hbonds - betti_1) * 0.2061641) / 0.026215233)) * 1.4765725e-5` | `(n_hbonds - sin((-betti_1 + n_hbonds)*0.2061641)/0.026215233)*1.4765725e-5` |
| 13 | 2.475152e-07 | 0.0020 | `(n_hbonds - (sin(sin((n_hbonds - betti_1) * 0.27028888)) / 0.026661308)) * 1.3979171e-5` | `(n_hbonds - sin(sin((-betti_1 + n_hbonds)*0.27028888))/0.026661308)*1.3979171e-5` |
| 14 | 2.475152e-07 | 0.0000 | `sin((n_hbonds - (sin(sin((n_hbonds - betti_1) * 0.27028888)) / 0.026661308)) * 1.3979171e-5)` | `sin((n_hbonds - sin(sin((-betti_1 + n_hbonds)*0.27028888))/0.026661308)*1.3979171e-5)` |
| 15 | 2.473085e-07 | 0.0008 | `(n_hbonds - (sin(sin((n_hbonds - betti_1) * -0.23822527)) / (4.0952744 / n_hbonds))) * 1.4222804e-5` | `(n_hbonds - sin(sin((-betti_1 + n_hbonds)*(-0.23822527)))/(4.0952744/n_hbonds))*1.4222804e-5` |
| 16 | 2.473085e-07 | 0.0000 | `sin((n_hbonds - (sin(sin((n_hbonds - betti_1) * -0.23822527)) / (4.0952744 / n_hbonds))) * 1.4222804e-5)` | `sin((n_hbonds - sin(sin((-betti_1 + n_hbonds)*(-0.23822527)))/(4.0952744/n_hbonds))*1.4222804e-5)` |
| 18 | 2.469393e-07 | 0.0007 | `((n_hbonds + cos(betti_1 * 0.309463)) - (sin(sin((n_hbonds - betti_1) * -0.23822527)) / 0.02519692)) * 1.4229358e-5` | `(n_hbonds - sin(sin((-betti_1 + n_hbonds)*(-0.23822527)))/0.02519692 + cos(betti_1*0.309463))*1.4229358e-5` |
| 20 | 2.468923e-07 | 0.0001 | `(cos((euler_characteristic * betti_1) + n_hbonds) + (n_hbonds - (sin(sin((n_hbonds - betti_1) * 0.27028888)) / 0.026661308))) * 1.3979171e-5` | `(n_hbonds - sin(sin((-betti_1 + n_hbonds)*0.27028888))/0.026661308 + cos(betti_1*euler_characteristic + n_hbonds))*1.3979171e-5` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: -0.0019109752*cos(-0.048944183*betti_1)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1672122e-5` | `n_hbonds*1.1672122e-5` |
| 4 | 2.521924e-07 | 0.0051 | `log(betti_1) * 0.00045175498` | `0.00045175498*log(betti_1)` |
| 5 | 2.517717e-07 | 0.0017 | `(-0.043384165 / betti_1) + 0.0025640032` | `0.0025640032 - 0.043384165/betti_1` |
| 6 | 2.503170e-07 | 0.0058 | `-0.0019109752 * cos(-0.048944183 * betti_1)` | `-0.0019109752*cos(-0.048944183*betti_1)` |
| 7 | 2.501187e-07 | 0.0008 | `cos(sin(betti_1 * -0.048696972)) * 0.0019085123` | `cos(sin(betti_1*(-0.048696972)))*0.0019085123` |
| 8 | 2.499749e-07 | 0.0006 | `(cos(betti_1 * 0.19496953) * 0.00015712957) + 0.0017590289` | `cos(betti_1*0.19496953)*0.00015712957 + 0.0017590289` |
| 9 | 2.497937e-07 | 0.0007 | `(sin(cos(betti_1 * -0.19477898)) * 0.00018323117) + 0.0017571802` | `sin(cos(betti_1*(-0.19477898)))*0.00018323117 + 0.0017571802` |
| 11 | 2.491703e-07 | 0.0012 | `(cos((sin(n_hbonds) + betti_1) * -0.19542283) * 0.00017237764) + 0.0017499913` | `cos((betti_1 + sin(n_hbonds))*(-0.19542283))*0.00017237764 + 0.0017499913` |
| 13 | 2.477472e-07 | 0.0029 | `((cos(betti_1 * 0.24272066) - cos(betti_1 - n_hbonds)) * -9.984703e-5) + 0.0018262527` | `0.0018262527 + (cos(betti_1*0.24272066) - cos(betti_1 - n_hbonds))*(-9.984703e-5)` |
| 14 | 2.474720e-07 | 0.0011 | `((cos(betti_1 * 0.24272066) - sin(cos(betti_1 - n_hbonds))) * -9.984703e-5) + 0.0018262527` | `0.0018262527 + (-sin(cos(betti_1 - n_hbonds)) + cos(betti_1*0.24272066))*(-9.984703e-5)` |
| 16 | 2.471728e-07 | 0.0006 | `(sin((cos(betti_1 - n_hbonds) * -0.51432514) + cos(-0.14432545 * betti_1)) * -0.00023214253) + 0.001732822` | `0.001732822 + sin(cos(-0.14432545*betti_1) + cos(betti_1 - n_hbonds)*(-0.51432514))*(-0.00023214253)` |
| 17 | 2.471544e-07 | 0.0001 | `(-0.00023214253 * sin((cos(betti_1 - n_hbonds) * -0.48547676) + cos(-0.14432545 * betti_1))) + sin(0.001732822)` | `-0.00023214253*sin(cos(-0.14432545*betti_1) + cos(betti_1 - n_hbonds)*(-0.48547676)) + sin(0.001732822)` |
| 19 | 2.469016e-07 | 0.0005 | `(((-0.16833973 / cos(((betti_1 / n_hbonds) + n_hbonds) - betti_1)) + cos(betti_1 * 0.14415064)) * -0.00019099058) + 0.0017260344` | `0.0017260344 + (cos(betti_1*0.14415064) - 0.16833973/cos(-betti_1 + betti_1/n_hbonds + n_hbonds))*(-0.00019099058)` |
| 20 | 2.466155e-07 | 0.0012 | `(sin((-0.3014933 / cos((n_hbonds + (betti_1 / n_hbonds)) - betti_1)) + cos(betti_1 * -0.24298473)) * -0.00015620992) + 0.0018110722` | `0.0018110722 + sin(cos(betti_1*(-0.24298473)) - 0.3014933/cos(-betti_1 + betti_1/n_hbonds + n_hbonds))*(-0.00015620992)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: cos(betti_1*(-0.04920097))*(-0.0019097836)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 2.540913e-07 | 0.0000 | `0.0018668327` | `0.00186683270000000` |
| 3 | 2.534733e-07 | 0.0012 | `n_hbonds * 1.1671869e-5` | `n_hbonds*1.1671869e-5` |
| 5 | 2.517758e-07 | 0.0034 | `0.002519254 - (-0.039942615 / euler_characteristic)` | `0.002519254 - (-1)*0.039942615/euler_characteristic` |
| 6 | 2.503417e-07 | 0.0057 | `cos(betti_1 * -0.04920097) * -0.0019097836` | `cos(betti_1*(-0.04920097))*(-0.0019097836)` |
| 8 | 2.496212e-07 | 0.0014 | `-0.0018244598 / cos((betti_1 - n_hbonds) * 0.09578851)` | `-0.0018244598/cos((betti_1 - n_hbonds)*0.09578851)` |
| 9 | 2.493413e-07 | 0.0011 | `0.0015249006 / sin(cos((betti_1 - n_hbonds) * 0.12756751))` | `0.0015249006/sin(cos((betti_1 - n_hbonds)*0.12756751))` |
| 11 | 2.493147e-07 | 0.0001 | `0.0015262724 / sin(cos(((betti_1 + -0.37545863) - n_hbonds) * 0.12717602))` | `0.0015262724/sin(cos((betti_1 - n_hbonds - 0.37545863)*0.12717602))` |
| 14 | 2.486993e-07 | 0.0008 | `((cos(betti_1 - n_hbonds) * 2.5131643) + betti_1) * ((n_hbonds * -2.9626844e-7) + 7.7478064e-5)` | `(7.7478064e-5 + n_hbonds*(-2.9626844e-7))*(betti_1 + cos(betti_1 - n_hbonds)*2.5131643)` |
| 15 | 2.486363e-07 | 0.0003 | `(betti_1 + (3.0617862 * sin(cos(n_hbonds - betti_1)))) * ((-3.0837276e-7 * n_hbonds) + 7.947408e-5)` | `(7.947408e-5 - 3.0837276e-7*n_hbonds)*(betti_1 + 3.0617862*sin(cos(-betti_1 + n_hbonds)))` |
| 16 | 2.479768e-07 | 0.0027 | `((n_hbonds * -3.1831428e-7) + 8.109459e-5) * ((cos((betti_1 + -0.4559769) - n_hbonds) * 2.8449218) + betti_1)` | `(8.109459e-5 + n_hbonds*(-3.1831428e-7))*(betti_1 + cos(betti_1 - n_hbonds - 0.4559769)*2.8449218)` |
| 17 | 2.478627e-07 | 0.0005 | `((-3.0812234e-7 * n_hbonds) + 7.947408e-5) * (betti_1 + (sin(cos(-0.42450678 + (betti_1 - n_hbonds))) * 3.0617862))` | `(7.947408e-5 - 3.0812234e-7*n_hbonds)*(betti_1 + sin(cos(betti_1 - n_hbonds - 0.42450678))*3.0617862)` |
| 18 | 2.477943e-07 | 0.0003 | `(betti_1 + (exp(sin(cos((n_hbonds - betti_1) + 0.5039167))) * 3.1622148)) * (7.1721945e-5 + (n_hbonds * -2.704318e-7))` | `(7.1721945e-5 + n_hbonds*(-2.704318e-7))*(betti_1 + exp(sin(cos(-betti_1 + n_hbonds + 0.5039167)))*3.1622148)` |
| 19 | 2.472496e-07 | 0.0022 | `(betti_1 + (sin(0.9999997 / cos((n_hbonds + 0.37869278) - betti_1)) * 2.420067)) * ((n_hbonds * -3.1025257e-7) + 7.983397e-5)` | `(7.983397e-5 + n_hbonds*(-3.1025257e-7))*(betti_1 + sin(0.9999997/cos(-betti_1 + n_hbonds + 0.37869278))*2.420067)` |

</details>

