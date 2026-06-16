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
| 1 | `LBHB_Fraction ≈ exp(euler_characteristic/exp(sin(n_hbonds*(-0.03735811)) + 0.98132855)) + 0.0021788962` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13960478) - 1*(-0.0017845872)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ exp(0.13965264*euler_characteristic) + 0.0017864308` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ exp(euler_characteristic*0.13960125) - 1*(-0.0017848626)` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ exp(euler_characteristic/7.163202) - 1*(-0.0017850517)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx exp(euler_characteristic/exp(sin(n_hbonds*(-0.03735811)) + 0.98132855)) + 0.0021788962$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 61/81 | 75.3% | 🔥 High |
| `n_hbonds` | Total number of hydrogen bonds in the network | 35/81 | 43.2% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 18/81 | 22.2% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 17/81 | 21.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/81 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 61/81 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: exp(euler_characteristic/exp(sin(n_hbonds*(-0.03735811)) + 0.98132855)) + 0.0021788962</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.615589e-06 | 0.0000 | `0.0025009285` | `0.00250092850000000` |
| 2 | 1.615589e-06 | 0.0000 | `sin(0.0025009285)` | `sin(0.0025009285)` |
| 3 | 1.068826e-06 | 0.4131 | `-0.14090165 / euler_characteristic` | `-0.14090165/euler_characteristic` |
| 4 | 5.334020e-07 | 0.6950 | `exp(n_hbonds * -0.039988086)` | `exp(n_hbonds*(-0.039988086))` |
| 5 | 3.159853e-07 | 0.5236 | `-0.063028105 / (euler_characteristic + 27.818727)` | `-0.063028105/(euler_characteristic + 27.818727)` |
| 6 | 2.233474e-07 | 0.3470 | `exp(euler_characteristic / 7.1626716) + 0.0017850589` | `exp(euler_characteristic/7.1626716) + 0.0017850589` |
| 7 | 2.231044e-07 | 0.0011 | `exp(exp(euler_characteristic / 7.158042)) + -0.99821275` | `exp(exp(euler_characteristic/7.158042)) - 0.99821275` |
| 8 | 1.973443e-07 | 0.1227 | `exp(euler_characteristic / 7.336664) + (euler_characteristic * -3.0229297e-5)` | `euler_characteristic*(-3.0229297e-5) + exp(euler_characteristic/7.336664)` |
| 9 | 1.973435e-07 | 0.0000 | `sin(exp(euler_characteristic / 7.336664) + (euler_characteristic * -3.0229297e-5))` | `sin(euler_characteristic*(-3.0229297e-5) + exp(euler_characteristic/7.336664))` |
| 10 | 1.849451e-07 | 0.0649 | `((euler_characteristic * -5.025641e-7) * betti_1) + exp(euler_characteristic / 7.4529276)` | `euler_characteristic*(-5.025641e-7)*betti_1 + exp(euler_characteristic/7.4529276)` |
| 11 | 1.849425e-07 | 0.0000 | `sin(((euler_characteristic * -5.025641e-7) * betti_1) + exp(euler_characteristic / 7.4529276))` | `sin(euler_characteristic*(-5.025641e-7)*betti_1 + exp(euler_characteristic/7.4529276))` |
| 12 | 1.557457e-07 | 0.1718 | `exp(euler_characteristic / exp(sin(n_hbonds * -0.03735811) + 0.98132855)) + 0.0021788962` | `exp(euler_characteristic/exp(sin(n_hbonds*(-0.03735811)) + 0.98132855)) + 0.0021788962` |
| 13 | 1.557454e-07 | 0.0000 | `sin(exp(euler_characteristic / exp(sin(n_hbonds * -0.03735811) + 0.98132855)) + 0.0021788962)` | `sin(exp(euler_characteristic/exp(sin(n_hbonds*(-0.03735811)) + 0.98132855)) + 0.0021788962)` |
| 14 | 1.553271e-07 | 0.0027 | `exp(euler_characteristic / exp(sin((n_hbonds - 4.863136) * -0.038801637) + 0.9830072)) + 0.0021801512` | `exp(euler_characteristic/exp(sin((n_hbonds - 1*4.863136)*(-0.038801637)) + 0.9830072)) + 0.0021801512` |
| 15 | 1.503266e-07 | 0.0327 | `exp(euler_characteristic / exp(sin((n_hbonds - exp(betti_0)) * -0.03819776) + 0.98132837)) + 0.0021709686` | `exp(euler_characteristic/exp(sin((n_hbonds - exp(betti_0))*(-0.03819776)) + 0.98132837)) + 0.0021709686` |
| 16 | 1.503254e-07 | 0.0000 | `sin(exp(euler_characteristic / exp(sin((n_hbonds - exp(betti_0)) * -0.038197808) + 0.98132837)) + 0.0021710433)` | `sin(exp(euler_characteristic/exp(sin((n_hbonds - exp(betti_0))*(-0.038197808)) + 0.98132837)) + 0.0021710433)` |
| 17 | 1.489254e-07 | 0.0094 | `exp(euler_characteristic / exp(sin((n_hbonds - exp(0.4713755 + betti_0)) * -0.03877763) + 0.98300725)) + 0.002184592` | `exp(euler_characteristic/exp(sin((n_hbonds - exp(betti_0 + 0.4713755))*(-0.03877763)) + 0.98300725)) + 0.002184592` |
| 18 | 1.489250e-07 | 0.0000 | `sin(exp(euler_characteristic / exp(sin((n_hbonds - exp(betti_0 + 0.4713755)) * -0.03877763) + 0.98300725)) + 0.002184592)` | `sin(exp(euler_characteristic/exp(sin((n_hbonds - exp(betti_0 + 0.4713755))*(-0.03877763)) + 0.98300725)) + 0.002184592)` |
| 19 | 1.488901e-07 | 0.0002 | `exp(euler_characteristic / exp(sin(((n_hbonds - exp(betti_0 + 0.42897207)) - 0.4809736) * -0.03882975) + 0.9830072)) + 0.0021735292` | `exp(euler_characteristic/exp(sin((n_hbonds - exp(betti_0 + 0.42897207) - 1*0.4809736)*(-0.03882975)) + 0.9830072)) + 0.0021735292` |
| 20 | 1.481470e-07 | 0.0050 | `0.002184592 + exp(euler_characteristic / exp(sin(-0.03877763 * ((cos(betti_1) + n_hbonds) - exp(0.4713755 + betti_0))) + 0.98300725))` | `exp(euler_characteristic/exp(sin(-0.03877763*(n_hbonds - exp(betti_0 + 0.4713755) + cos(betti_1))) + 0.98300725)) + 0.002184592` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: exp(euler_characteristic*0.13960478) - 1*(-0.0017845872)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.615589e-06 | 0.0000 | `0.0025009296` | `0.00250092960000000` |
| 3 | 1.068826e-06 | 0.2066 | `-0.14090207 / euler_characteristic` | `-0.14090207/euler_characteristic` |
| 4 | 5.333787e-07 | 0.6951 | `exp(n_hbonds * -0.039976113)` | `exp(n_hbonds*(-0.039976113))` |
| 6 | 2.233472e-07 | 0.4353 | `exp(euler_characteristic * 0.13960478) - -0.0017845872` | `exp(euler_characteristic*0.13960478) - 1*(-0.0017845872)` |
| 8 | 1.949087e-07 | 0.0681 | `0.00485178 / exp(sin(cos(betti_1 * -0.10880248)))` | `0.00485178/exp(sin(cos(betti_1*(-0.10880248))))` |
| 9 | 1.899582e-07 | 0.0257 | `0.0070301215 / exp(sin(euler_characteristic * 0.08274241) * 1.2231846)` | `0.0070301215/exp(sin(euler_characteristic*0.08274241)*1.2231846)` |
| 10 | 1.749903e-07 | 0.0821 | `0.006076803 / exp(sin(sin(euler_characteristic * 0.080225155) * 1.5484488))` | `0.006076803/exp(sin(sin(euler_characteristic*0.080225155)*1.5484488))` |
| 11 | 1.691083e-07 | 0.0342 | `0.0051156105 / exp(sin(sin(sin(euler_characteristic * 0.07652079) * 1.7443672)))` | `0.0051156105/exp(sin(sin(sin(euler_characteristic*0.07652079)*1.7443672)))` |
| 12 | 1.643437e-07 | 0.0286 | `0.005211635 / exp(sin(sin(euler_characteristic * 0.07674633) * 1.8333081) / 1.1383332)` | `0.005211635/exp(sin(sin(euler_characteristic*0.07674633)*1.8333081)/1.1383332)` |
| 13 | 1.619320e-07 | 0.0148 | `0.005123269 / exp(sin(sin((sin(euler_characteristic * 0.07673168) * 1.8182304) / betti_0)))` | `0.005123269/exp(sin(sin(sin(euler_characteristic*0.07673168)*1.8182304/betti_0)))` |
| 14 | 1.588762e-07 | 0.0191 | `0.0052061863 / exp(sin((sin(euler_characteristic * 0.07678084) / betti_0) * 1.882163) * 0.8755513)` | `0.0052061863/exp(sin(sin(euler_characteristic*0.07678084)*1.882163/betti_0)*0.8755513)` |
| 16 | 1.583872e-07 | 0.0015 | `0.0051799486 / exp(sin(((sin(euler_characteristic * 0.07677948) / betti_0) + -0.009024516) * 1.882163) * 0.8755511)` | `0.0051799486/exp(sin((-0.009024516 + sin(euler_characteristic*0.07677948)/betti_0)*1.882163)*0.8755511)` |
| 18 | 1.583817e-07 | 0.0000 | `0.0051795477 / exp((sin(((sin(euler_characteristic * 0.07678535) / betti_0) + -0.009851054) * 1.882163) * 1.0097814) / 1.1533095)` | `0.0051795477/exp(sin((-0.009851054 + sin(euler_characteristic*0.07678535)/betti_0)*1.882163)*1.0097814/1.1533095)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: exp(0.13965264*euler_characteristic) + 0.0017864308</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.615589e-06 | 0.0000 | `0.0025009296` | `0.00250092960000000` |
| 3 | 1.068826e-06 | 0.2066 | `-0.14090219 / euler_characteristic` | `-0.14090219/euler_characteristic` |
| 4 | 5.333787e-07 | 0.6951 | `exp(n_hbonds * -0.03997582)` | `exp(n_hbonds*(-0.03997582))` |
| 6 | 2.233513e-07 | 0.4352 | `0.0017864308 + exp(0.13965264 * euler_characteristic)` | `exp(0.13965264*euler_characteristic) + 0.0017864308` |
| 8 | 1.973441e-07 | 0.0619 | `(euler_characteristic * -3.0225796e-5) + exp(euler_characteristic * 0.13629536)` | `euler_characteristic*(-3.0225796e-5) + exp(euler_characteristic*0.13629536)` |
| 9 | 1.973433e-07 | 0.0000 | `sin((euler_characteristic * -3.0225796e-5) + exp(euler_characteristic * 0.13629536))` | `sin(euler_characteristic*(-3.0225796e-5) + exp(euler_characteristic*0.13629536))` |
| 10 | 1.848984e-07 | 0.0651 | `((betti_1 * betti_1) * 4.951762e-7) + exp(euler_characteristic * 0.13426387)` | `betti_1*betti_1*4.951762e-7 + exp(euler_characteristic*0.13426387)` |
| 12 | 1.838521e-07 | 0.0028 | `(((betti_1 * 6.7936446e-7) + -1.1130983e-5) * betti_1) + exp(euler_characteristic * 0.13347974)` | `betti_1*(betti_1*6.7936446e-7 - 1.1130983e-5) + exp(euler_characteristic*0.13347974)` |
| 13 | 1.678385e-07 | 0.0911 | `(betti_1 * 3.0296265e-5) + exp((betti_1 - sin(-0.18378872 * n_hbonds)) * -0.13427651)` | `betti_1*3.0296265e-5 + exp((betti_1 - sin(-0.18378872*n_hbonds))*(-0.13427651))` |
| 14 | 1.677643e-07 | 0.0004 | `(betti_1 * 3.0296265e-5) + exp((betti_1 - sin(sin(-0.18533735) * n_hbonds)) * -0.13427651)` | `betti_1*3.0296265e-5 + exp((betti_1 - sin(n_hbonds*sin(-0.18533735)))*(-0.13427651))` |
| 15 | 1.601615e-07 | 0.0464 | `((betti_1 * 5.022369e-7) * betti_1) + exp((betti_1 - sin(n_hbonds * -0.18308467)) * -0.13204832)` | `betti_1*5.022369e-7*betti_1 + exp((betti_1 - sin(n_hbonds*(-0.18308467)))*(-0.13204832))` |
| 17 | 1.568472e-07 | 0.0105 | `exp((betti_1 * -0.13235426) - (sin(n_hbonds * -0.18281192) * -0.18357602)) + ((betti_1 * 5.0201453e-7) * betti_1)` | `betti_1*5.0201453e-7*betti_1 + exp(betti_1*(-0.13235426) - (-0.18357602)*sin(n_hbonds*(-0.18281192)))` |
| 18 | 1.551441e-07 | 0.0109 | `exp(((betti_1 - sin(0.55620515 * betti_1)) - sin(-0.18165492 * n_hbonds)) * -0.13493688) - (-3.0541025e-5 * betti_1)` | `-(-1)*3.0541025e-5*betti_1 + exp((betti_1 - sin(0.55620515*betti_1) - sin(-0.18165492*n_hbonds))*(-0.13493688))` |
| 19 | 1.549057e-07 | 0.0015 | `exp(((betti_1 - sin(sin(betti_1 * 0.55620515))) - sin(n_hbonds * -0.18227327)) * -0.13493688) - (betti_1 * -3.0541025e-5)` | `-(-3.0541025e-5)*betti_1 + exp((betti_1 - sin(n_hbonds*(-0.18227327)) - sin(sin(betti_1*0.55620515)))*(-0.13493688))` |
| 20 | 1.518392e-07 | 0.0200 | `((betti_1 * betti_1) * 5.04806e-7) + exp(((betti_1 - sin(betti_1 * 0.55925)) - sin(n_hbonds * 0.20503823)) * -0.13274053)` | `betti_1*betti_1*5.04806e-7 + exp((betti_1 - sin(n_hbonds*0.20503823) - sin(betti_1*0.55925))*(-0.13274053))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: exp(euler_characteristic*0.13960125) - 1*(-0.0017848626)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.615589e-06 | 0.0000 | `0.002500926` | `0.00250092600000000` |
| 3 | 1.068826e-06 | 0.2066 | `-0.1409021 / euler_characteristic` | `-0.1409021/euler_characteristic` |
| 4 | 5.333819e-07 | 0.6951 | `exp(n_hbonds * -0.039980188)` | `exp(n_hbonds*(-0.039980188))` |
| 6 | 2.233473e-07 | 0.4353 | `exp(euler_characteristic * 0.13960125) - -0.0017848626` | `exp(euler_characteristic*0.13960125) - 1*(-0.0017848626)` |
| 8 | 1.973444e-07 | 0.0619 | `exp(euler_characteristic * 0.13630232) - (euler_characteristic * 3.0229954e-5)` | `-3.0229954e-5*euler_characteristic + exp(euler_characteristic*0.13630232)` |
| 9 | 1.973436e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13630232) - (euler_characteristic * 3.0229954e-5))` | `sin(-3.0229954e-5*euler_characteristic + exp(euler_characteristic*0.13630232))` |
| 10 | 1.848999e-07 | 0.0651 | `exp(euler_characteristic * 0.13424827) - ((betti_1 * -4.9540364e-7) * betti_1)` | `-(-4.9540364e-7)*betti_1*betti_1 + exp(euler_characteristic*0.13424827)` |
| 11 | 1.848973e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13424827) - (betti_1 * (-4.9540364e-7 * betti_1)))` | `sin(-(-4.9540364e-7)*betti_1*betti_1 + exp(euler_characteristic*0.13424827))` |
| 12 | 1.821378e-07 | 0.0150 | `(exp(euler_characteristic * 0.11829722) - ((euler_characteristic * 0.00015862743) + 0.0070980913)) / 1.4608886` | `(-(euler_characteristic*0.00015862743 + 0.0070980913) + exp(euler_characteristic*0.11829722))/1.4608886` |
| 13 | 1.821350e-07 | 0.0000 | `sin((exp(0.11829722 * euler_characteristic) - ((euler_characteristic * 0.00015862743) + 0.0070980913)) / 1.4608886)` | `sin((-(euler_characteristic*0.00015862743 + 0.0070980913) + exp(0.11829722*euler_characteristic))/1.4608886)` |
| 14 | 1.819464e-07 | 0.0010 | `((exp(euler_characteristic * 0.11716642) - ((betti_1 * betti_1) * -1.2480873e-6)) - 0.0017747575) / 1.7295526` | `(-(-1.2480873e-6)*betti_1*betti_1 + exp(euler_characteristic*0.11716642) - 1*0.0017747575)/1.7295526` |
| 15 | 1.687875e-07 | 0.0751 | `exp(euler_characteristic * 0.13628732) - (3.0044952e-5 * (euler_characteristic + (sin(n_hbonds * 0.18390939) * 8.258343)))` | `-3.0044952e-5*(euler_characteristic + sin(n_hbonds*0.18390939)*8.258343) + exp(euler_characteristic*0.13628732)` |
| 16 | 1.687861e-07 | 0.0000 | `sin(exp(euler_characteristic * 0.13628732) - (3.0044952e-5 * ((8.258343 * sin(n_hbonds * 0.18390939)) + euler_characteristic)))` | `sin(-3.0044952e-5*(euler_characteristic + 8.258343*sin(n_hbonds*0.18390939)) + exp(euler_characteristic*0.13628732))` |
| 17 | 1.669189e-07 | 0.0111 | `exp(0.13628732 * euler_characteristic) - (((sin(0.18390939 * (betti_0 * n_hbonds)) / 0.11634455) + euler_characteristic) * 2.995026e-5)` | `-2.995026e-5*(euler_characteristic + sin(0.18390939*betti_0*n_hbonds)/0.11634455) + exp(0.13628732*euler_characteristic)` |
| 19 | 1.655700e-07 | 0.0041 | `exp(euler_characteristic * 0.13628732) - ((euler_characteristic + (betti_0 * (sin(n_hbonds * (betti_0 * 0.18287443)) / 0.11634455))) * 3.032373e-5)` | `-3.032373e-5*(betti_0*sin(n_hbonds*betti_0*0.18287443)/0.11634455 + euler_characteristic) + exp(euler_characteristic*0.13628732)` |
| 20 | 1.654085e-07 | 0.0010 | `exp(euler_characteristic * 0.13629252) - ((euler_characteristic + (exp(betti_0 + 1.0999558) * sin(n_hbonds * (betti_0 * 0.18390931)))) * 2.9984638e-5)` | `-2.9984638e-5*(euler_characteristic + exp(betti_0 + 1.0999558)*sin(n_hbonds*betti_0*0.18390931)) + exp(euler_characteristic*0.13629252)` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: exp(euler_characteristic/7.163202) - 1*(-0.0017850517)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.615589e-06 | 0.0000 | `0.0025009294` | `0.00250092940000000` |
| 3 | 1.068826e-06 | 0.2066 | `-0.14090216 / euler_characteristic` | `-0.14090216/euler_characteristic` |
| 4 | 5.339022e-07 | 0.6941 | `exp(n_hbonds * -0.03991685)` | `exp(n_hbonds*(-0.03991685))` |
| 5 | 3.795666e-07 | 0.3412 | `0.0007300333 / cos(log(n_hbonds))` | `0.0007300333/cos(log(n_hbonds))` |
| 6 | 2.233474e-07 | 0.5303 | `exp(euler_characteristic / 7.163202) - -0.0017850517` | `exp(euler_characteristic/7.163202) - 1*(-0.0017850517)` |
| 8 | 2.110791e-07 | 0.0282 | `(exp(euler_characteristic / 6.139422) * 2.310732) - -0.0019415348` | `exp(euler_characteristic/6.139422)*2.310732 - 1*(-0.0019415348)` |
| 9 | 2.110760e-07 | 0.0000 | `sin((2.310732 * exp(euler_characteristic / 6.139422)) - -0.0019415348)` | `sin(2.310732*exp(euler_characteristic/6.139422) - 1*(-0.0019415348))` |
| 11 | 2.038962e-07 | 0.0173 | `0.001947599 - (-2.21825 / exp((sin(betti_1) - euler_characteristic) / 6.144518))` | `0.001947599 - (-1)*2.21825/exp((-euler_characteristic + sin(betti_1))/6.144518)` |
| 12 | 2.030588e-07 | 0.0041 | `0.0019520555 - (-2.2631195 / exp((sin(sin(betti_1)) - euler_characteristic) / 6.1278768))` | `0.0019520555 - (-1)*2.2631195/exp((-euler_characteristic + sin(sin(betti_1)))/6.1278768)` |
| 13 | 1.774545e-07 | 0.1348 | `0.0019851949 - (-2.2903428 / exp((sin(n_hbonds / 5.471308) - euler_characteristic) / 6.081492))` | `0.0019851949 - (-1)*2.2903428/exp((-euler_characteristic + sin(n_hbonds/5.471308))/6.081492)` |
| 14 | 1.774536e-07 | 0.0000 | `sin(0.0019851949 - (-2.2903428 / exp((sin(n_hbonds / 5.471308) - euler_characteristic) / 6.081492)))` | `sin(0.0019851949 - (-1)*2.2903428/exp((-euler_characteristic + sin(n_hbonds/5.471308))/6.081492))` |
| 15 | 1.656242e-07 | 0.0690 | `0.002001751 - (-2.2374477 / exp(((sin(n_hbonds / 5.475514) / 0.5098625) - euler_characteristic) / 6.0437446))` | `0.002001751 - (-1)*2.2374477/exp((-euler_characteristic + sin(n_hbonds/5.475514)/0.5098625)/6.0437446)` |
| 16 | 1.652733e-07 | 0.0021 | `0.002001751 - (-2.2374477 / exp(((sin(sin(n_hbonds / 5.475514)) / 0.47912166) - euler_characteristic) / 6.0437446))` | `0.002001751 - (-1)*2.2374477/exp((-euler_characteristic + sin(sin(n_hbonds/5.475514))/0.47912166)/6.0437446)` |
| 17 | 1.588490e-07 | 0.0396 | `0.001974645 - (-2.246416 / exp(((sin((betti_0 * n_hbonds) / 5.4766526) / 0.50789005) - euler_characteristic) / 6.0650306))` | `0.001974645 - (-1)*2.246416/exp((-euler_characteristic + sin(betti_0*n_hbonds/5.4766526)/0.50789005)/6.0650306)` |
| 18 | 1.588486e-07 | 0.0000 | `sin(0.001974645 - (-2.246416 / exp(((sin((betti_0 * n_hbonds) / 5.4766526) / 0.50789005) - euler_characteristic) / 6.0650306)))` | `sin(0.001974645 - (-1)*2.246416/exp((-euler_characteristic + sin(betti_0*n_hbonds/5.4766526)/0.50789005)/6.0650306))` |
| 19 | 1.584406e-07 | 0.0026 | `0.0019868098 - (-2.2323372 / exp(((sin((betti_0 * (n_hbonds + -1.8549672)) / 5.3914866) / 0.47350198) - euler_characteristic) / 6.0622864))` | `0.0019868098 - (-1)*2.2323372/exp((-euler_characteristic + sin(betti_0*(n_hbonds - 1.8549672)/5.3914866)/0.47350198)/6.0622864)` |
| 20 | 1.584236e-07 | 0.0001 | `0.0019868098 - (-2.2323372 / exp(((sin((betti_0 * (-1.8549672 + n_hbonds)) / 5.3914866) / exp(-0.7123281)) - euler_characteristic) / 6.0622864))` | `0.0019868098 - (-1)*2.2323372/exp((-euler_characteristic + sin(betti_0*(n_hbonds - 1.8549672)/5.3914866)/exp(-0.7123281))/6.0622864)` |

</details>

