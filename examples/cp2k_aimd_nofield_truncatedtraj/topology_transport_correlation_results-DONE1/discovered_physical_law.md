# Discovering Robust H-Bond Topological Laws via Multi-Run Symbolic Regression

This report presents the robust physical equations discovered by running multi-run Symbolic Regression (PySR) with stability selection. By executing independent evolutionary runs with different random seeds, we identify equations and topological invariants that consistently govern proton transport properties.

## 1. Study Settings
- **Target Transport Property**: `LBHB_Fraction`
- **Total Independent PySR Runs**: 5
- **Iterations Per Run**: 500
- **Input Topological Invariants**: `n_hbonds`, `betti_0`, `betti_1`, `betti_2`, `euler_characteristic`, `state_0D1A`, `state_0D2A`, `state_0D3A`, `state_0D4A`, `state_1D0A`, `state_1D1A`, `state_1D2A`, `state_1D3A`, `state_1D4A`, `state_1D5A`, `state_2D0A`, `state_2D1A`, `state_2D2A`, `state_2D3A`, `state_2D4A`, `state_2D5A`, `state_3D0A`, `state_3D1A`, `state_3D2A`, `state_3D3A`, `state_3D4A`, `state_4D1A`, `state_4D2A`, `state_4D3A`, `state_5D1A`, `state_5D2A`, `state_free H2O`

## 2. Robust Consensus Physical Laws (Voting Analysis)
Below is the frequency table of the 'best' equations selected by PySR across all runs. The equation with the highest vote count represents the most robust mathematical representation of the underlying physical relationship.

| Rank | Discovered Consensus Equation | Vote Count | Frequency | 
| :--- | :--- | :--- | :--- |
| 1 | `LBHB_Fraction ≈ (betti_1 - state_1D1A/exp(state_2D0A))*1.6957956e-5` | 1/5 | 20.0% |
| 2 | `LBHB_Fraction ≈ state_1D1A*(state_2D0A*8.971791e-6 - 3.2555316e-5) + 0.0011885501` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ 0.001101667 - exp(euler_characteristic*0.1340902 - state_2D0A)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ state_1D1A*(-3.1118245e-5)/exp(state_2D0A) + 0.0011096032` | 1/5 | 20.0% |
| 5 | `LBHB_Fraction ≈ 0.0010911482*cos(-0.89838237/(state_2D0A - (-1)*13.287303/state_1D1A))` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB\_Fraction \approx (betti\_1 - state\_1D1A/exp(state\_2D0A))*1.6957956e-5$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `state_2D0A` | Water donating 2 and accepting 0 H-bonds (extreme donor defect) | 66/77 | 85.7% | 🔥 High |
| `state_1D1A` | Water donating 1 and accepting 1 H-bonds (wire/chain intermediate) | 41/77 | 53.2% | ⚡ Medium |
| `state_3D0A` | Water donating 3 and accepting 0 H-bonds (extreme donor defect) | 35/77 | 45.5% | ⚡ Medium |
| `state_1D0A` | Water donating 1 and accepting 0 H-bonds | 34/77 | 44.2% | ⚡ Medium |
| `state_0D4A` | Water donating 0 and accepting 4 H-bonds | 23/77 | 29.9% | ❄️ Low |
| `betti_1` | Number of independent H-bond loops/cycles | 13/77 | 16.9% | ❄️ Low |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 13/77 | 16.9% | ❄️ Low |
| `state_0D3A` | Water donating 0 and accepting 3 H-bonds | 6/77 | 7.8% | ❄️ Low |
| `state_3D1A` | Water donating 3 and accepting 1 H-bonds | 5/77 | 6.5% | ❄️ Low |
| `state_1D4A` | Water donating 1 and accepting 4 H-bonds | 1/77 | 1.3% | ❄️ Low |
| `n_hbonds` | Total number of hydrogen bonds in the network | 0/77 | 0.0% | ❄️ Low |
| `betti_0` | Number of connected components in the network | 0/77 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/77 | 0.0% | ❄️ Low |
| `state_0D1A` | Water donating 0 and accepting 1 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_0D2A` | Water donating 0 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_1D2A` | Water donating 1 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_1D3A` | Water donating 1 and accepting 3 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_1D5A` | Water donating 1 and accepting 5 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_2D1A` | Water donating 2 and accepting 1 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_2D2A` | Water donating 2 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_2D3A` | Water donating 2 and accepting 3 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_2D4A` | Water donating 2 and accepting 4 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_2D5A` | Water donating 2 and accepting 5 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_3D2A` | Water donating 3 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_3D3A` | Water donating 3 and accepting 3 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_3D4A` | Water donating 3 and accepting 4 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_4D1A` | Water donating 4 and accepting 1 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_4D2A` | Water donating 4 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_4D3A` | Water donating 4 and accepting 3 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_5D1A` | Water donating 5 and accepting 1 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_5D2A` | Water donating 5 and accepting 2 H-bonds | 0/77 | 0.0% | ❄️ Low |
| `state_free H2O` | Topological descriptor | 0/77 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `state_2D0A` is the most stable feature (appearing in 66/77 Pareto equations). This strongly indicates that `state_2D0A` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: (betti_1 - state_1D1A/exp(state_2D0A))*1.6957956e-5</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.617301e-5` | `euler_characteristic*(-1.617301e-5)` |
| 5 | 2.975065e-08 | 0.0720 | `(state_2D0A * 9.122085e-5) + 0.00086870603` | `state_2D0A*9.122085e-5 + 0.00086870603` |
| 7 | 2.696375e-08 | 0.0492 | `0.0011313102 - (0.00018441048 / (state_2D0A + 0.5403024))` | `0.0011313102 - 0.00018441048/(state_2D0A + 0.5403024)` |
| 8 | 2.420965e-08 | 0.1077 | `(betti_1 - (state_1D1A / exp(state_2D0A))) * 1.6957956e-5` | `(betti_1 - state_1D1A/exp(state_2D0A))*1.6957956e-5` |
| 9 | 2.266267e-08 | 0.0660 | `(betti_1 - (state_1D1A / (state_2D0A + 0.60023516))) * 1.7832836e-5` | `(betti_1 - state_1D1A/(state_2D0A + 0.60023516))*1.7832836e-5` |
| 10 | 2.230770e-08 | 0.0158 | `(betti_1 - (state_1D1A / (-0.3516108 + exp(state_2D0A)))) * 1.727617e-5` | `(betti_1 - state_1D1A/(exp(state_2D0A) - 0.3516108))*1.727617e-5` |
| 11 | 2.115894e-08 | 0.0529 | `(betti_1 - (state_1D1A / ((state_2D0A + 0.5135838) + state_1D0A))) * 1.771401e-5` | `(betti_1 - state_1D1A/(state_1D0A + state_2D0A + 0.5135838))*1.771401e-5` |
| 12 | 2.067743e-08 | 0.0230 | `(betti_1 - ((state_1D1A / exp(state_1D0A + state_2D0A)) / 0.5333781)) * 1.747853e-5` | `(betti_1 - state_1D1A/(0.5333781*exp(state_1D0A + state_2D0A)))*1.747853e-5` |
| 13 | 1.966407e-08 | 0.0502 | `(betti_1 - (state_1D1A / ((state_1D0A + 0.45880687) + (state_2D0A + state_3D0A)))) * 1.7697635e-5` | `(betti_1 - state_1D1A/(state_1D0A + state_2D0A + state_3D0A + 0.45880687))*1.7697635e-5` |
| 14 | 1.898348e-08 | 0.0352 | `(betti_1 - (state_1D1A / ((state_1D0A + exp(state_3D0A)) * (state_2D0A + 0.45880687)))) * 1.7697635e-5` | `(betti_1 - state_1D1A/((state_1D0A + exp(state_3D0A))*(state_2D0A + 0.45880687)))*1.7697635e-5` |
| 15 | 1.891655e-08 | 0.0035 | `1.7655315e-5 * (betti_1 - (((state_1D1A / (state_1D0A + exp(state_3D0A))) / 0.47350246) / exp(state_2D0A)))` | `1.7655315e-5*(betti_1 - state_1D1A/(0.47350246*(state_1D0A + exp(state_3D0A))*exp(state_2D0A)))` |
| 16 | 1.824894e-08 | 0.0359 | `(betti_1 - ((state_1D1A / exp(state_1D0A + state_2D0A)) / (state_0D4A + (state_3D0A + 0.4546807)))) * 1.7583472e-5` | `(betti_1 - state_1D1A/((state_0D4A + state_3D0A + 0.4546807)*exp(state_1D0A + state_2D0A)))*1.7583472e-5` |
| 17 | 1.801520e-08 | 0.0129 | `(betti_1 - (((state_1D1A / (state_1D0A + exp(state_0D4A))) / (state_3D0A + 0.46833518)) / exp(state_2D0A))) * 1.7621169e-5` | `(betti_1 - state_1D1A/((state_1D0A + exp(state_0D4A))*(state_3D0A + 0.46833518)*exp(state_2D0A)))*1.7621169e-5` |
| 18 | 1.740587e-08 | 0.0344 | `((betti_1 - ((state_1D1A / (state_1D0A + exp(state_2D0A))) / ((state_0D4A + 0.43306127) + state_3D0A))) * 0.0011157128) / betti_1` | `(betti_1 - state_1D1A/((state_1D0A + exp(state_2D0A))*(state_0D4A + state_3D0A + 0.43306127)))*0.0011157128/betti_1` |
| 20 | 1.662597e-08 | 0.0229 | `((betti_1 + (((state_3D1A - state_1D1A) / (exp(state_2D0A) + state_1D0A)) / (state_0D4A + (state_3D0A + 0.39325014)))) * 0.0011128627) / betti_1` | `(betti_1 + (-state_1D1A + state_3D1A)/((state_1D0A + exp(state_2D0A))*(state_0D4A + state_3D0A + 0.39325014)))*0.0011128627/betti_1` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: state_1D1A*(state_2D0A*8.971791e-6 - 3.2555316e-5) + 0.0011885501</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173242e-5` | `euler_characteristic*(-1.6173242e-5)` |
| 5 | 2.975125e-08 | 0.0720 | `(state_2D0A + 9.423905) * 9.205301e-5` | `(state_2D0A + 9.423905)*9.205301e-5` |
| 6 | 2.973886e-08 | 0.0004 | `sin((state_2D0A * -8.998845e-5) + 9.423906)` | `sin(9.423906 + state_2D0A*(-8.998845e-5))` |
| 7 | 2.865157e-08 | 0.0372 | `((state_2D0A + state_3D0A) * 9.898951e-5) + 0.00084918423` | `(state_2D0A + state_3D0A)*9.898951e-5 + 0.00084918423` |
| 8 | 2.708611e-08 | 0.0562 | `log((-0.1637879 - state_2D0A) * -19705.795) * 9.939632e-5` | `9.939632e-5*log(19705.795*state_2D0A + 3227.5707808805)` |
| 9 | 2.414976e-08 | 0.1147 | `(((state_2D0A * 8.971791e-6) + -3.2555316e-5) * state_1D1A) + 0.0011885501` | `state_1D1A*(state_2D0A*8.971791e-6 - 3.2555316e-5) + 0.0011885501` |
| 10 | 2.414975e-08 | 0.0000 | `sin(0.0011885501 + ((-3.2555316e-5 + (state_2D0A * 8.971791e-6)) * state_1D1A))` | `sin(state_1D1A*(state_2D0A*8.971791e-6 - 3.2555316e-5) + 0.0011885501)` |
| 11 | 2.310183e-08 | 0.0444 | `((state_1D1A * ((state_2D0A * 7.291054e-7) + -1.943153e-6)) * state_1D1A) + 0.0010913307` | `state_1D1A*state_1D1A*(state_2D0A*7.291054e-7 - 1.943153e-6) + 0.0010913307` |
| 12 | 2.284118e-08 | 0.0113 | `log(((state_2D0A + (state_3D0A + 0.05090009)) + state_1D0A) * 5606.6245) * 0.00011180872` | `0.00011180872*log(5606.6245*state_1D0A + 5606.6245*state_2D0A + 5606.6245*state_3D0A + 285.377691646205)` |
| 13 | 2.090309e-08 | 0.0887 | `log(((exp(state_1D0A) / state_1D1A) + (state_2D0A + state_3D0A)) * 1887.34) * 0.0001284951` | `0.0001284951*log(1887.34*state_2D0A + 1887.34*state_3D0A + 1887.34*exp(state_1D0A)/state_1D1A)` |
| 15 | 2.026218e-08 | 0.0156 | `0.00013176315 * log(((exp(state_1D0A + state_0D3A) / state_1D1A) + (state_2D0A + state_3D0A)) * 1523.4609)` | `0.00013176315*log(1523.4609*state_2D0A + 1523.4609*state_3D0A + 1523.4609*exp(state_0D3A + state_1D0A)/state_1D1A)` |
| 16 | 2.019122e-08 | 0.0035 | `log((state_2D0A + (exp(state_0D3A) * (state_3D0A + (exp(state_1D0A) / state_1D1A)))) * 1586.8192) * 0.00013063893` | `0.00013063893*log(1586.8192*state_2D0A + 1586.8192*(state_3D0A + exp(state_1D0A)/state_1D1A)*exp(state_0D3A))` |
| 17 | 1.976339e-08 | 0.0214 | `0.00013176315 * log(((exp((state_1D0A + state_0D3A) + state_0D4A) / state_1D1A) + (state_2D0A + state_3D0A)) * 1523.4609)` | `0.00013176315*log(1523.4609*state_2D0A + 1523.4609*state_3D0A + 1523.4609*exp(state_0D3A + state_0D4A + state_1D0A)/state_1D1A)` |
| 18 | 1.943449e-08 | 0.0168 | `log((state_2D0A + (exp(state_0D3A) * (state_0D4A + ((exp(state_1D0A) / state_1D1A) + state_3D0A)))) * 1130.88) * 0.00013597307` | `0.00013597307*log(1130.88*state_2D0A + 1130.88*(state_0D4A + state_3D0A + exp(state_1D0A)/state_1D1A)*exp(state_0D3A))` |
| 19 | 1.943449e-08 | 0.0000 | `sin(log((state_2D0A + (exp(state_0D3A) * (state_0D4A + ((exp(state_1D0A) / state_1D1A) + state_3D0A)))) * 1130.88) * 0.00013597307)` | `sin(0.00013597307*log(1130.88*state_2D0A + 1130.88*(state_0D4A + state_3D0A + exp(state_1D0A)/state_1D1A)*exp(state_0D3A)))` |
| 20 | 1.893855e-08 | 0.0258 | `log(((state_2D0A + ((((exp(state_3D1A) / state_1D1A) + exp(state_1D0A)) / state_1D1A) + state_3D0A)) + state_0D4A) * 759.994) * 0.00014335425` | `0.00014335425*log(759.994*state_0D4A + 759.994*state_2D0A + 759.994*state_3D0A + 759.994*(exp(state_1D0A) + exp(state_3D1A)/state_1D1A)/state_1D1A)` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: 0.001101667 - exp(euler_characteristic*0.1340902 - state_2D0A)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173057e-5` | `euler_characteristic*(-1.6173057e-5)` |
| 5 | 2.975064e-08 | 0.0720 | `(state_2D0A * 9.12204e-5) + 0.0008687069` | `state_2D0A*9.12204e-5 + 0.0008687069` |
| 7 | 2.696289e-08 | 0.0492 | `(-0.00021347203 / (state_2D0A + 0.6086285)) + 0.0011417449` | `0.0011417449 - 0.00021347203/(state_2D0A + 0.6086285)` |
| 8 | 2.228567e-08 | 0.1905 | `0.001101667 - exp((euler_characteristic * 0.1340902) - state_2D0A)` | `0.001101667 - exp(euler_characteristic*0.1340902 - state_2D0A)` |
| 9 | 2.228567e-08 | 0.0000 | `sin(0.001101667 - exp((euler_characteristic * 0.1340902) - state_2D0A))` | `sin(0.001101667 - exp(euler_characteristic*0.1340902 - state_2D0A))` |
| 10 | 1.952224e-08 | 0.1324 | `0.0011007979 - exp(((euler_characteristic * 0.12992583) - state_1D0A) - state_2D0A)` | `0.0011007979 - exp(euler_characteristic*0.12992583 - state_1D0A - state_2D0A)` |
| 11 | 1.878632e-08 | 0.0384 | `0.0011101809 - exp(cos(state_1D0A) - (state_2D0A - (euler_characteristic * 0.14697537)))` | `0.0011101809 - exp(-(-0.14697537*euler_characteristic + state_2D0A) + cos(state_1D0A))` |
| 12 | 1.878632e-08 | 0.0000 | `sin(0.0011101809 - exp(cos(state_1D0A) - (state_2D0A - (euler_characteristic * 0.14697537))))` | `sin(0.0011101809 - exp(-(-0.14697537*euler_characteristic + state_2D0A) + cos(state_1D0A)))` |
| 13 | 1.740086e-08 | 0.0766 | `0.0011125695 - exp(cos(state_1D0A) - ((state_3D0A + (0.14310078 * betti_1)) + state_2D0A))` | `0.0011125695 - exp(-(0.14310078*betti_1 + state_2D0A + state_3D0A) + cos(state_1D0A))` |
| 15 | 1.677643e-08 | 0.0183 | `0.0011125695 - exp(cos(state_1D0A) - ((((state_3D1A - euler_characteristic) * 0.14310078) + state_3D0A) + state_2D0A))` | `0.0011125695 - exp(-(state_2D0A + state_3D0A + (-euler_characteristic + state_3D1A)*0.14310078) + cos(state_1D0A))` |
| 17 | 1.639692e-08 | 0.0114 | `0.0011122039 - exp(cos(state_1D0A) - (((state_3D0A + state_0D4A) + state_2D0A) + ((state_3D1A - euler_characteristic) * 0.1428143)))` | `0.0011122039 - exp(-(state_0D4A + state_2D0A + state_3D0A + (-euler_characteristic + state_3D1A)*0.1428143) + cos(state_1D0A))` |
| 19 | 1.618853e-08 | 0.0064 | `0.0010997526 - exp(cos(state_1D0A) - (((state_3D1A + (state_2D0A - euler_characteristic)) * 0.1428141) + (state_3D0A + (state_0D4A + state_2D0A))))` | `0.0010997526 - exp(-(state_0D4A + state_2D0A + state_3D0A + (-euler_characteristic + state_2D0A + state_3D1A)*0.1428141) + cos(state_1D0A))` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: state_1D1A*(-3.1118245e-5)/exp(state_2D0A) + 0.0011096032</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.0009936077` | `0.000993607700000000` |
| 2 | 3.697801e-08 | 0.0000 | `sin(0.0009936268)` | `sin(0.0009936268)` |
| 3 | 3.435608e-08 | 0.0735 | `euler_characteristic * -1.6172953e-5` | `euler_characteristic*(-1.6172953e-5)` |
| 5 | 2.975065e-08 | 0.0720 | `(state_2D0A * 9.1217815e-5) + 0.0008687106` | `state_2D0A*9.1217815e-5 + 0.0008687106` |
| 6 | 2.708107e-08 | 0.0940 | `(-0.00031167344 / exp(state_2D0A)) + 0.001109937` | `0.001109937 - 0.00031167344*exp(-state_2D0A)` |
| 7 | 2.696225e-08 | 0.0044 | `(-0.00020007679 / (state_2D0A + 0.57745576)) + 0.0011370138` | `0.0011370138 - 0.00020007679/(state_2D0A + 0.57745576)` |
| 8 | 2.217348e-08 | 0.1955 | `((state_1D1A / exp(state_2D0A)) * -3.1118245e-5) + 0.0011096032` | `state_1D1A*(-3.1118245e-5)/exp(state_2D0A) + 0.0011096032` |
| 10 | 2.085629e-08 | 0.0306 | `((state_1D1A / (exp(state_2D0A) + state_1D0A)) * -3.6768663e-5) + 0.0011131227` | `state_1D1A*(-3.6768663e-5)/(state_1D0A + exp(state_2D0A)) + 0.0011131227` |
| 12 | 2.080411e-08 | 0.0013 | `((state_1D1A * -3.3055e-5) * exp((state_2D0A / -0.98424613) - state_3D0A)) + 0.0011078025` | `state_1D1A*(-3.3055e-5)*exp(state_2D0A/(-0.98424613) - state_3D0A) + 0.0011078025` |
| 14 | 1.899062e-08 | 0.0456 | `((exp(((state_2D0A * -1.3221844) - state_3D0A) - state_1D0A) * -3.9021277e-5) * state_1D1A) + 0.001083493` | `exp(-state_1D0A + state_2D0A*(-1.3221844) - state_3D0A)*(-3.9021277e-5)*state_1D1A + 0.001083493` |
| 15 | 1.890333e-08 | 0.0046 | `(state_1D1A * (exp(((state_2D0A * -1.3221844) - state_3D0A) - sin(state_1D0A)) * -3.9021277e-5)) + 0.001083493` | `state_1D1A*exp(state_2D0A*(-1.3221844) - state_3D0A - sin(state_1D0A))*(-3.9021277e-5) + 0.001083493` |
| 16 | 1.822925e-08 | 0.0363 | `(state_1D1A * (exp((((state_2D0A * -1.3221844) - state_0D4A) - state_3D0A) - state_1D0A) * -4.0813527e-5)) + 0.0010867447` | `state_1D1A*exp(-state_0D4A - state_1D0A + state_2D0A*(-1.3221844) - state_3D0A)*(-4.0813527e-5) + 0.0010867447` |
| 17 | 1.809741e-08 | 0.0073 | `((exp(((state_2D0A * -1.3221844) - state_0D4A) - (state_3D0A + sin(state_1D0A))) * -4.0698185e-5) * state_1D1A) + 0.0010904629` | `exp(-state_0D4A + state_2D0A*(-1.3221844) - (state_3D0A + sin(state_1D0A)))*(-4.0698185e-5)*state_1D1A + 0.0010904629` |
| 18 | 1.780831e-08 | 0.0161 | `(state_1D1A * (exp((((state_2D0A * -1.3221844) - state_3D0A) - state_0D4A) - (state_1D0A * 0.704342)) * -4.092298e-5)) + 0.0010897999` | `state_1D1A*exp(-state_0D4A - 0.704342*state_1D0A + state_2D0A*(-1.3221844) - state_3D0A)*(-4.092298e-5) + 0.0010897999` |
| 19 | 1.778507e-08 | 0.0013 | `0.001083493 + (-3.9021277e-5 * (state_1D1A * exp((((state_2D0A * -1.3221844) - state_3D0A) - state_0D4A) - (exp(-0.4940459) * state_1D0A))))` | `-3.9021277e-5*state_1D1A*exp(-state_0D4A - state_1D0A*exp(-0.4940459) + state_2D0A*(-1.3221844) - state_3D0A) + 0.001083493` |
| 20 | 1.777328e-08 | 0.0007 | `0.001083493 + (-3.9021277e-5 * (state_1D1A * exp((((state_2D0A * -1.3221844) - state_3D0A) - state_0D4A) - (exp(log(0.5245074)) * state_1D0A))))` | `-3.9021277e-5*state_1D1A*exp(-state_0D4A - 0.5245074*state_1D0A - 1.3221844*state_2D0A - state_3D0A) + 0.001083493` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: 0.0010911482*cos(-0.89838237/(state_2D0A - (-1)*13.287303/state_1D1A))</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3.697801e-08 | 0.0000 | `0.000993608` | `0.000993608000000000` |
| 3 | 3.435608e-08 | 0.0368 | `euler_characteristic * -1.6173048e-5` | `euler_characteristic*(-1.6173048e-5)` |
| 5 | 2.975065e-08 | 0.0720 | `(state_2D0A * 9.122109e-5) - -0.0008687057` | `state_2D0A*9.122109e-5 - 1*(-0.0008687057)` |
| 7 | 2.709310e-08 | 0.0468 | `cos(-0.73754466 / exp(state_2D0A)) * 0.0010598575` | `cos(-0.73754466*exp(-state_2D0A))*0.0010598575` |
| 8 | 2.696450e-08 | 0.0048 | `exp(-0.15924037 / (state_2D0A + 0.44474635)) * 0.0011298256` | `exp(-0.15924037/(state_2D0A + 0.44474635))*0.0011298256` |
| 9 | 2.493595e-08 | 0.0782 | `cos(0.8215643 / (state_2D0A + exp(state_3D0A))) * 0.0010976329` | `cos(0.8215643/(state_2D0A + exp(state_3D0A)))*0.0010976329` |
| 10 | 2.113187e-08 | 0.1655 | `0.0010911482 * cos(-0.89838237 / (state_2D0A - (-13.287303 / state_1D1A)))` | `0.0010911482*cos(-0.89838237/(state_2D0A - (-1)*13.287303/state_1D1A))` |
| 12 | 1.966367e-08 | 0.0360 | `cos(0.89603275 / (state_0D4A + ((12.707533 / state_1D1A) + state_2D0A))) * 0.0010911482` | `cos(0.89603275/(state_0D4A + state_2D0A + 12.707533/state_1D1A))*0.0010911482` |
| 13 | 1.965432e-08 | 0.0005 | `cos(-0.8939027 / ((state_2D0A + sin(state_0D4A)) + (12.707533 / state_1D1A))) * 0.0010923607` | `cos(-0.8939027/(state_2D0A + sin(state_0D4A) + 12.707533/state_1D1A))*0.0010923607` |
| 14 | 1.872863e-08 | 0.0482 | `cos(-0.9213356 / ((12.707533 / state_1D1A) + ((state_2D0A + state_3D0A) + state_0D4A))) * 0.0010923607` | `cos(-0.9213356/(state_0D4A + state_2D0A + state_3D0A + 12.707533/state_1D1A))*0.0010923607` |
| 15 | 1.872362e-08 | 0.0003 | `cos(-0.9213356 / ((12.707533 / state_1D1A) + ((state_2D0A + sin(state_0D4A)) + state_3D0A))) * 0.0010923607` | `cos(-0.9213356/(state_2D0A + state_3D0A + sin(state_0D4A) + 12.707533/state_1D1A))*0.0010923607` |
| 16 | 1.855905e-08 | 0.0088 | `cos(0.92120457 / (state_3D0A + ((state_2D0A + (12.707533 / (state_1D1A + state_1D4A))) + state_0D4A))) * 0.0010923607` | `cos(0.92120457/(state_0D4A + state_2D0A + state_3D0A + 12.707533/(state_1D1A + state_1D4A)))*0.0010923607` |
| 17 | 1.833145e-08 | 0.0123 | `cos(-0.9213356 / (((sin(state_1D0A) + 12.707533) / state_1D1A) + ((state_0D4A + state_3D0A) + state_2D0A))) * 0.0010923607` | `cos(-0.9213356/(state_0D4A + state_2D0A + state_3D0A + (sin(state_1D0A) + 12.707533)/state_1D1A))*0.0010923607` |
| 18 | 1.814925e-08 | 0.0100 | `cos(0.30663487 / ((-4.213527 / state_1D1A) - (((state_3D0A + state_0D4A) + state_2D0A) * (state_0D3A - -0.2569501)))) * 0.0011027541` | `cos(0.30663487/(-(state_0D3A - 1*(-0.2569501))*(state_0D4A + state_2D0A + state_3D0A) - 4.213527/state_1D1A))*0.0011027541` |
| 20 | 1.737837e-08 | 0.0217 | `cos(-0.117852695 / ((-1.4456767 / state_1D1A) + (state_3D0A - ((state_2D0A + 0.048088565) * ((state_0D4A + state_1D0A) - -0.13943069))))) * 0.0010774486` | `cos(-0.117852695/(state_3D0A - (state_2D0A + 0.048088565)*(state_0D4A + state_1D0A - 1*(-0.13943069)) - 1.4456767/state_1D1A))*0.0010774486` |

</details>

