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
| 1 | `LBHB_Fraction ≈ euler_characteristic*(-3.139346e-5)` | 2/5 | 40.0% |
| 2 | `LBHB_Fraction ≈ euler_characteristic*(-3.1393745e-5)` | 1/5 | 20.0% |
| 3 | `LBHB_Fraction ≈ euler_characteristic*(-3.1393567e-5)` | 1/5 | 20.0% |
| 4 | `LBHB_Fraction ≈ euler_characteristic*(-3.1393734e-5)` | 1/5 | 20.0% |

> [!IMPORTANT]
> **Consensus Physical Law Discovered:**
> $$LBHB_Fraction \approx euler_characteristic*(-3.139346e-5)$$
> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.

## 3. Topological Invariant Feature Stability Selection
We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.

| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |
| :--- | :--- | :--- | :--- | :--- |
| `euler_characteristic` | Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2) | 39/66 | 59.1% | ⚡ Medium |
| `betti_1` | Number of independent H-bond loops/cycles | 30/66 | 45.5% | ⚡ Medium |
| `n_hbonds` | Total number of hydrogen bonds in the network | 27/66 | 40.9% | ⚡ Medium |
| `betti_0` | Number of connected components in the network | 0/66 | 0.0% | ❄️ Low |
| `betti_2` | Number of topological voids/cavities | 0/66 | 0.0% | ❄️ Low |

> [!TIP]
> **Topological Driver Interpretation:**
> The topological invariant `euler_characteristic` is the most stable feature (appearing in 39/66 Pareto equations). This strongly indicates that `euler_characteristic` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.

## 4. Detailed Individual Run Fronts
Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):

<details>
<summary><b>Run 1 (Seed: 42) — Best Equation: euler_characteristic*(-3.139346e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.0018550089` | `0.00185500890000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.139346e-5` | `euler_characteristic*(-3.139346e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `0.004267227 - (-0.14214766 / euler_characteristic)` | `0.004267227 - (-1)*0.14214766/euler_characteristic` |
| 6 | 9.980553e-08 | 0.0710 | `sin(euler_characteristic * -0.075094424) * -0.0019950564` | `sin(euler_characteristic*(-0.075094424))*(-0.0019950564)` |
| 8 | 9.952158e-08 | 0.0014 | `(cos(euler_characteristic * -0.050489057) * -0.005027611) - 0.003033832` | `cos(euler_characteristic*(-0.050489057))*(-0.005027611) - 1*0.003033832` |
| 11 | 9.763151e-08 | 0.0064 | `-0.002132311 * cos(cos(-0.08112419 * n_hbonds) - (euler_characteristic * 0.028835509))` | `-0.002132311*cos(-0.028835509*euler_characteristic + cos(-0.08112419*n_hbonds))` |
| 12 | 9.763150e-08 | 0.0000 | `sin(cos(cos(n_hbonds * -0.08112419) - (euler_characteristic * 0.028835509)) * -0.002132311)` | `sin(cos(-0.028835509*euler_characteristic + cos(n_hbonds*(-0.08112419)))*(-0.002132311))` |
| 13 | 9.762491e-08 | 0.0001 | `cos(cos(n_hbonds * -0.08110444) - ((euler_characteristic + 0.18044916) * 0.029036772)) * -0.002129248` | `cos(-0.029036772*(euler_characteristic + 0.18044916) + cos(n_hbonds*(-0.08110444)))*(-0.002129248)` |
| 14 | 9.741649e-08 | 0.0021 | `cos(cos(n_hbonds * -0.08112576) - ((euler_characteristic + sin(euler_characteristic)) * 0.028836379)) * -0.002131875` | `cos(-0.028836379*(euler_characteristic + sin(euler_characteristic)) + cos(n_hbonds*(-0.08112576)))*(-0.002131875)` |
| 15 | 9.738281e-08 | 0.0003 | `cos(cos(n_hbonds * -0.08113331) - ((sin(sin(euler_characteristic)) + euler_characteristic) * 0.028840927)) * -0.0021335417` | `cos(-0.028840927*(euler_characteristic + sin(sin(euler_characteristic))) + cos(n_hbonds*(-0.08113331)))*(-0.0021335417)` |
| 16 | 9.646727e-08 | 0.0094 | `cos(((euler_characteristic + sin(euler_characteristic + n_hbonds)) * 0.028832512) - cos(0.08099212 * n_hbonds)) * -0.0021358267` | `cos((euler_characteristic + sin(euler_characteristic + n_hbonds))*0.028832512 - cos(0.08099212*n_hbonds))*(-0.0021358267)` |
| 18 | 9.599133e-08 | 0.0025 | `cos(cos(n_hbonds * 0.08094631) - (0.028842805 * (euler_characteristic + (0.54637045 / sin(n_hbonds + euler_characteristic))))) * -0.0021264867` | `cos(-0.028842805*(euler_characteristic + 0.54637045/sin(euler_characteristic + n_hbonds)) + cos(n_hbonds*0.08094631))*(-0.0021264867)` |
| 19 | 9.591607e-08 | 0.0008 | `cos(cos(n_hbonds * 0.08094631) - (0.028842805 * (euler_characteristic + (0.54637045 / sin(sin(n_hbonds + euler_characteristic)))))) * -0.0021264867` | `cos(-0.028842805*(euler_characteristic + 0.54637045/sin(sin(euler_characteristic + n_hbonds))) + cos(n_hbonds*0.08094631))*(-0.0021264867)` |
| 20 | 9.515232e-08 | 0.0080 | `cos(cos(n_hbonds * -0.08109831) - ((euler_characteristic + (-0.47321948 / sin((euler_characteristic + n_hbonds) / -1.0734403))) * 0.028840927)) * -0.002129248` | `cos(-0.028840927*(euler_characteristic - 0.47321948/sin((euler_characteristic + n_hbonds)/(-1.0734403))) + cos(n_hbonds*(-0.08109831)))*(-0.002129248)` |

</details>

<details>
<summary><b>Run 2 (Seed: 43) — Best Equation: euler_characteristic*(-3.139346e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.001855009` | `0.00185500900000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.139346e-5` | `euler_characteristic*(-3.139346e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `(0.1421496 / euler_characteristic) + 0.0042672595` | `0.0042672595 + 0.1421496/euler_characteristic` |
| 6 | 1.071470e-07 | 0.0000 | `0.004267271 - sin(-0.14215046 / euler_characteristic)` | `0.004267271 - sin(-0.14215046/euler_characteristic)` |
| 7 | 1.008575e-07 | 0.0605 | `0.0023261295 - (0.0056770425 / (betti_1 + -47.01507))` | `0.0023261295 - 0.0056770425/(betti_1 - 47.01507)` |
| 8 | 1.008575e-07 | 0.0000 | `0.0023261295 - sin(0.0056770425 / (betti_1 + -47.01507))` | `0.0023261295 - sin(0.0056770425/(betti_1 - 47.01507))` |
| 9 | 9.944730e-08 | 0.0141 | `(((betti_1 * -6.1374094e-6) + 0.0007773563) * betti_1) + -0.02262157` | `betti_1*(0.0007773563 + betti_1*(-6.1374094e-6)) - 0.02262157` |
| 10 | 9.944729e-08 | 0.0000 | `sin((((betti_1 * -6.1374094e-6) + 0.0007773563) * betti_1) + -0.02262157)` | `sin(betti_1*(0.0007773563 + betti_1*(-6.1374094e-6)) - 0.02262157)` |
| 11 | 9.916990e-08 | 0.0028 | `(-0.19140507 / (euler_characteristic + 7.8279867)) - (-0.03254353 / (euler_characteristic + 41.202312))` | `-(-1)*0.03254353/(euler_characteristic + 41.202312) - 0.19140507/(euler_characteristic + 7.8279867)` |
| 13 | 9.829961e-08 | 0.0044 | `0.0017849447 + (-0.004453325 / (euler_characteristic + (46.717422 + (56.071045 / (euler_characteristic + 56.071045)))))` | `0.0017849447 - 0.004453325/(euler_characteristic + 46.717422 + 56.071045/(euler_characteristic + 56.071045))` |
| 14 | 9.829959e-08 | 0.0000 | `sin(0.0017849447 + (-0.004453325 / (euler_characteristic + (46.717422 + (56.071045 / (euler_characteristic + 56.071045))))))` | `sin(0.0017849447 - 0.004453325/(euler_characteristic + 46.717422 + 56.071045/(euler_characteristic + 56.071045)))` |
| 16 | 9.812423e-08 | 0.0009 | `0.0017849447 - (-0.004453325 / (cos(euler_characteristic) - ((euler_characteristic + 46.717422) + (56.27101 / (euler_characteristic + 56.071045)))))` | `0.0017849447 - (-1)*0.004453325/(-(euler_characteristic + 46.717422 + 56.27101/(euler_characteristic + 56.071045)) + cos(euler_characteristic))` |
| 17 | 9.796413e-08 | 0.0016 | `0.0017849447 - (-0.004453325 / (sin(exp(betti_1)) - (euler_characteristic + ((56.071045 / (56.071045 + euler_characteristic)) + 46.717422))))` | `0.0017849447 - (-1)*0.004453325/(-(euler_characteristic + 46.717422 + 56.071045/(euler_characteristic + 56.071045)) + sin(exp(betti_1)))` |
| 18 | 9.777059e-08 | 0.0020 | `(0.004547865 / (sin(euler_characteristic * -4802.48) - (euler_characteristic + ((56.071045 / (euler_characteristic + 56.071033)) + 46.717422)))) + 0.0017816067` | `0.0017816067 + 0.004547865/(-(euler_characteristic + 46.717422 + 56.071045/(euler_characteristic + 56.071033)) + sin(euler_characteristic*(-4802.48)))` |
| 20 | 9.766519e-08 | 0.0005 | `0.0017849447 - (-0.004453325 / (sin(-46.909794 / (56.27101 - betti_1)) - (46.717422 + (euler_characteristic + (56.071045 / (euler_characteristic + 56.071045))))))` | `0.0017849447 - (-1)*0.004453325/(-(euler_characteristic + 46.717422 + 56.071045/(euler_characteristic + 56.071045)) + sin(-46.909794/(56.27101 - betti_1)))` |

</details>

<details>
<summary><b>Run 3 (Seed: 44) — Best Equation: euler_characteristic*(-3.1393745e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.0018550085` | `0.00185500850000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.1393745e-5` | `euler_characteristic*(-3.1393745e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `(0.14211437 / euler_characteristic) + 0.00426666` | `0.00426666 + 0.14211437/euler_characteristic` |
| 6 | 9.980683e-08 | 0.0710 | `sin(euler_characteristic / 13.32189) * 0.0019960715` | `sin(euler_characteristic/13.32189)*0.0019960715` |
| 8 | 9.936601e-08 | 0.0022 | `(-0.01886852 / sin(euler_characteristic / -39.690567)) - -0.02086176` | `-1*(-0.02086176) - 0.01886852/sin(euler_characteristic/(-39.690567))` |
| 11 | 9.914037e-08 | 0.0008 | `(1.2141004 - (((-1.2552903 / betti_1) + 0.00030975536) * euler_characteristic)) / -1.0363919` | `(1.2141004 - euler_characteristic*(0.00030975536 - 1.2552903/betti_1))/(-1.0363919)` |
| 12 | 9.826253e-08 | 0.0089 | `((euler_characteristic * -7.871162e-5) + (sin(euler_characteristic / -3.984373) * 0.00034416898)) - 0.002975998` | `euler_characteristic*(-7.871162e-5) + sin(euler_characteristic/(-3.984373))*0.00034416898 - 1*0.002975998` |

</details>

<details>
<summary><b>Run 4 (Seed: 45) — Best Equation: euler_characteristic*(-3.1393567e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.0018549822` | `0.00185498220000000` |
| 3 | 1.099853e-07 | 0.0767 | `euler_characteristic * -3.1393567e-5` | `euler_characteristic*(-3.1393567e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `0.0042682225 - (-0.1422085 / euler_characteristic)` | `0.0042682225 - (-1)*0.1422085/euler_characteristic` |
| 6 | 9.989459e-08 | 0.0701 | `sin(betti_1 * -0.073825635) * 0.0019943337` | `sin(betti_1*(-0.073825635))*0.0019943337` |
| 7 | 9.989458e-08 | 0.0000 | `sin(sin(betti_1 * -0.073825635) * 0.0019943337)` | `sin(sin(betti_1*(-0.073825635))*0.0019943337)` |
| 8 | 9.965603e-08 | 0.0024 | `sin(0.4931475 + (betti_1 * -0.08244955)) * 0.0019964168` | `sin(0.4931475 + betti_1*(-0.08244955))*0.0019964168` |
| 9 | 9.841239e-08 | 0.0126 | `sin(sin(betti_1 * 0.12117737) + 0.55998945) * 0.0019592638` | `sin(sin(betti_1*0.12117737) + 0.55998945)*0.0019592638` |
| 11 | 9.742439e-08 | 0.0050 | `sin((cos(n_hbonds * -0.3723352) + betti_1) * -0.073399425) * 0.0019870386` | `sin((betti_1 + cos(n_hbonds*(-0.3723352)))*(-0.073399425))*0.0019870386` |
| 13 | 9.643549e-08 | 0.0051 | `sin(((cos(-0.3306997 * n_hbonds) * 2.1582336) + betti_1) * -0.072977856) * 0.0019773152` | `sin((betti_1 + cos(-0.3306997*n_hbonds)*2.1582336)*(-0.072977856))*0.0019773152` |
| 14 | 9.643547e-08 | 0.0000 | `sin(sin((betti_1 + (cos(-0.3306997 * n_hbonds) * 2.1582336)) * -0.072977856) * 0.0019773152)` | `sin(sin((betti_1 + cos(-0.3306997*n_hbonds)*2.1582336)*(-0.072977856))*0.0019773152)` |
| 16 | 9.604525e-08 | 0.0020 | `0.0019740586 * sin(((cos(n_hbonds * 0.32980582) * exp(sin(exp(betti_1)))) + betti_1) * -0.07336985)` | `0.0019740586*sin((betti_1 + exp(sin(exp(betti_1)))*cos(n_hbonds*0.32980582))*(-0.07336985))` |
| 17 | 9.594587e-08 | 0.0010 | `sin((betti_1 + (cos(-0.32992235 * n_hbonds) * (sin(exp(betti_1)) + 1.692519))) * -0.07338035) * 0.0019694655` | `sin((betti_1 + (sin(exp(betti_1)) + 1.692519)*cos(-0.32992235*n_hbonds))*(-0.07338035))*0.0019694655` |
| 18 | 9.591488e-08 | 0.0003 | `0.0019740586 * sin((betti_1 + ((0.3063666 + exp(sin(exp(betti_1)))) * cos(n_hbonds * 0.32980582))) * -0.07336985)` | `0.0019740586*sin((betti_1 + (exp(sin(exp(betti_1))) + 0.3063666)*cos(n_hbonds*0.32980582))*(-0.07336985))` |
| 19 | 9.558409e-08 | 0.0035 | `0.0019740586 * sin(((betti_1 + cos(n_hbonds * 0.32931307)) + cos(n_hbonds / exp(sin(exp(betti_1))))) * -0.07336985)` | `0.0019740586*sin((betti_1 + cos(n_hbonds*0.32931307) + cos(n_hbonds/exp(sin(exp(betti_1)))))*(-0.07336985))` |
| 20 | 9.557448e-08 | 0.0001 | `sin((betti_1 + (cos(n_hbonds * -0.2865732) * exp(sin(cos(n_hbonds)) + sin(exp(betti_1))))) * -0.07338439) * 0.0019701351` | `sin((betti_1 + exp(sin(exp(betti_1)) + sin(cos(n_hbonds)))*cos(n_hbonds*(-0.2865732)))*(-0.07338439))*0.0019701351` |

</details>

<details>
<summary><b>Run 5 (Seed: 46) — Best Equation: euler_characteristic*(-3.1393734e-5)</b></summary>

| Complexity | Loss (MSE) | Score | Equation | Sympy Format |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 1.282176e-07 | 0.0000 | `0.001855009` | `0.00185500900000000` |
| 2 | 1.282176e-07 | 0.0000 | `sin(0.0018549558)` | `sin(0.0018549558)` |
| 3 | 1.099853e-07 | 0.1534 | `euler_characteristic * -3.1393734e-5` | `euler_characteristic*(-3.1393734e-5)` |
| 5 | 1.071470e-07 | 0.0131 | `(0.14214747 / euler_characteristic) - -0.004267223` | `-1*(-0.004267223) + 0.14214747/euler_characteristic` |
| 7 | 1.053346e-07 | 0.0085 | `log(log(betti_1) * 0.27317017) / betti_1` | `log(0.27317017*log(betti_1))/betti_1` |
| 8 | 9.970375e-08 | 0.0549 | `sin(0.072219566 * betti_1) / (n_hbonds / -0.315994)` | `sin(0.072219566*betti_1)/((n_hbonds/(-0.315994)))` |
| 10 | 9.966487e-08 | 0.0002 | `sin(betti_1 * 0.07222562) / ((n_hbonds + 0.9115795) / -0.31900913)` | `sin(betti_1*0.07222562)/(((n_hbonds + 0.9115795)/(-0.31900913)))` |
| 11 | 9.957143e-08 | 0.0009 | `sin(betti_1 * 0.07222562) / ((n_hbonds + sin(euler_characteristic)) / -0.31900913)` | `sin(betti_1*0.07222562)/(((n_hbonds + sin(euler_characteristic))/(-0.31900913)))` |
| 12 | 9.941746e-08 | 0.0015 | `sin(betti_1 * 0.072296) / ((exp(sin(euler_characteristic)) + n_hbonds) / -0.31900957)` | `sin(betti_1*0.072296)/(((n_hbonds + exp(sin(euler_characteristic)))/(-0.31900957)))` |
| 13 | 9.925321e-08 | 0.0017 | `sin(0.072219566 * betti_1) / ((n_hbonds + sin(0.6189226 * betti_1)) / -0.31900913)` | `sin(0.072219566*betti_1)/(((n_hbonds + sin(0.6189226*betti_1))/(-0.31900913)))` |
| 14 | 9.911916e-08 | 0.0014 | `sin(0.072219566 * betti_1) / ((n_hbonds + exp(sin(0.6189226 * betti_1))) / -0.31900913)` | `sin(0.072219566*betti_1)/(((n_hbonds + exp(sin(0.6189226*betti_1)))/(-0.31900913)))` |
| 15 | 9.831219e-08 | 0.0082 | `sin((-15.374511 / betti_1) + 16.073162) / ((sin(n_hbonds * 0.33924267) / 0.3065923) + euler_characteristic)` | `sin(16.073162 - 15.374511/betti_1)/(euler_characteristic + sin(n_hbonds*0.33924267)/0.3065923)` |
| 16 | 9.822254e-08 | 0.0009 | `sin(sin((-15.374545 / betti_1) + 16.072962) / ((sin(n_hbonds * -0.31889746) / 0.2955103) + euler_characteristic))` | `sin(sin(16.072962 - 15.374545/betti_1)/(euler_characteristic + sin(n_hbonds*(-0.31889746))/0.2955103))` |
| 17 | 9.821667e-08 | 0.0001 | `sin(sin((-15.374545 / betti_1) + 16.072962) / ((sin(-0.31889746 * n_hbonds) / sin(0.2955103)) + euler_characteristic))` | `sin(sin(16.072962 - 15.374545/betti_1)/(euler_characteristic + sin(-0.31889746*n_hbonds)/sin(0.2955103)))` |
| 18 | 9.804391e-08 | 0.0018 | `sin(sin((-15.374608 / betti_1) + 16.071888) / ((sin(0.7407599 - (n_hbonds * 0.30320933)) / -0.2573507) + euler_characteristic))` | `sin(sin(16.071888 - 15.374608/betti_1)/(euler_characteristic + sin(0.7407599 - 0.30320933*n_hbonds)/(-0.2573507)))` |

</details>

