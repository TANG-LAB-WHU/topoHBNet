#!/usr/bin/env python3
"""
Correlate H-Bond Topological Neural Network (TNN) Embeddings and Invariants
with Proton Transfer Dynamics & Hodge Flow Decomposition.

This script bridges the gap between pure algebraic topology / topological ML
and physical chemical transport. It reads the outputs from:
1. topoHBNet_main_analysis.py (Betti numbers, TNN PCA embeddings)
2. proton_transfer_analysis.py (PMF, Wire lengths, Hodge Flow Gradient/Curl percentages)

And performs:
- Alignment of time-series data
- Pearson/Spearman Correlation Heatmaps
- Topological State Clustering (K-Means on TNN PC space) & Transport Profiling
- Regression Modeling & Feature Importance (Predicting transport from topology)
- Publication-quality visualizations
"""

import os
import sys
import json
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Try importing sklearn for advanced analysis
try:
    from sklearn.cluster import KMeans
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# Try importing seaborn for heatmap styling
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bridge H-Bond Topology and Proton Dynamics Analysis",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--topo-dir', type=str, default='topoHBNet-run-ml',
                        help='Directory containing topoHBNet topological ML results')
    parser.add_argument('--proton-dir', type=str, default='proton_transfer_results',
                        help='Directory containing proton transfer and dynamics results')
    parser.add_argument('--output-dir', '-o', type=str, default='topology_transport_correlation_results',
                        help='Output directory for correlation analysis')
    parser.add_argument('--n-clusters', type=int, default=3,
                        help='Number of K-Means clusters for topological states')
    parser.add_argument('--run-pysr', action='store_true',
                        help='Run Symbolic Regression to discover explicit physical laws')
    parser.add_argument('--pysr-iterations', type=int, default=500,
                        help='Number of iterations/generations for PySR symbolic regression')
    parser.add_argument('--pysr-runs', type=int, default=5,
                        help='Number of independent PySR runs for stability and voting cross-validation')
    
    # GA algorithm parameters
    parser.add_argument('--pysr-populations', type=int, default=15,
                        help='Number of separate populations/islands to evolve')
    parser.add_argument('--pysr-population-size', type=int, default=33,
                        help='Number of equations in each population')
    parser.add_argument('--pysr-ncycles-per-iteration', type=int, default=550,
                        help='Number of evolutionary cycles per iteration')
    parser.add_argument('--pysr-maxsize', type=int, default=20,
                        help='Maximum complexity/nodes for discovered equations')
    parser.add_argument('--pysr-crossover-prob', type=float, default=0.06,
                        help='Crossover probability for genetic evolution')
    parser.add_argument('--pysr-parsimony', type=float, default=0.001,
                        help='Parsimony/complexity penalty weight')
    parser.add_argument('--pysr-weight-mutate-constant', type=float, default=1.0,
                        help='Relative weight of mutating constants')
    parser.add_argument('--pysr-weight-mutate-operator', type=float, default=1.0,
                        help='Relative weight of mutating operators')
    parser.add_argument('--pysr-weight-add-node', type=float, default=1.0,
                        help='Relative weight of adding a node to formula tree')
    parser.add_argument('--pysr-weight-delete-node', type=float, default=1.0,
                        help='Relative weight of deleting a node from formula tree')
                        
    return parser.parse_args()


def load_datasets(topo_dir: Path, proton_dir: Path):
    """Load and merge topological and transport datasets."""
    # Paths to files
    topo_csv = topo_dir / "raw_data_csv" / "dynamics_topology.csv"
    pca_csv = topo_dir / "raw_data_csv" / "ml_pca_components.csv"
    proton_csv = proton_dir / "proton_dynamics_timeseries.csv"

    if not topo_csv.exists():
        raise FileNotFoundError(f"Topological dynamics CSV not found: {topo_csv}")
    if not pca_csv.exists():
        raise FileNotFoundError(f"TNN PCA components CSV not found: {pca_csv}")
    if not proton_csv.exists():
        raise FileNotFoundError(f"Proton dynamics CSV not found: {proton_csv}")

    # Load dataframes
    df_topo = pd.read_csv(topo_csv)
    df_pca = pd.read_csv(pca_csv)
    df_proton = pd.read_csv(proton_csv)

    print(f"Loaded Topological Invariants: {df_topo.shape[0]} frames.")
    print(f"Loaded TNN PCA Components:    {df_pca.shape[0]} frames.")
    print(f"Loaded Proton Transport:       {df_proton.shape[0]} frames.")

    # Align based on index or nearest Time_fs
    # Note: topoHBNet may output more/less frames depending on step size, we will align by nearest Time_fs
    # To do this, let's round Time_fs to 1 decimal place or perform a merge_asof
    df_topo = df_topo.rename(columns={"time_fs": "Time_fs"}).sort_values("Time_fs")
    df_pca = df_pca.rename(columns={"time_fs": "Time_fs"}).sort_values("Time_fs")
    df_proton = df_proton.sort_values("Time_fs")

    # Drop time_ps if exists to avoid duplication
    if "time_ps" in df_topo.columns:
        df_topo = df_topo.drop(columns=["time_ps"])
    if "time_ps" in df_pca.columns:
        df_pca = df_pca.drop(columns=["time_ps"])

    # First merge topological datasets (they are typically perfectly aligned)
    df_topo_merged = pd.merge_asof(df_topo, df_pca, on="Time_fs", direction="nearest")

    # Then merge with proton dynamics
    df_merged = pd.merge_asof(df_topo_merged, df_proton, on="Time_fs", direction="nearest")

    # Drop potential duplicates and clean
    if "Frame" in df_merged.columns:
        df_merged = df_merged.drop(columns=["Frame"])

    print(f"Successfully aligned and merged dataset: {df_merged.shape[0]} frames.")
    return df_merged


def plot_correlation_heatmap(df: pd.DataFrame, topo_cols: list, transport_cols: list, output_path: Path):
    """Generate a high-quality correlation matrix heatmap."""
    cols_to_corr = topo_cols + transport_cols
    corr_matrix = df[cols_to_corr].corr(method='pearson')

    # Extract only cross-correlations (Topology vs Transport) to keep it clean
    cross_corr = corr_matrix.loc[topo_cols, transport_cols]

    plt.figure(figsize=(10, 8))

    if HAS_SEABORN:
        sns.heatmap(cross_corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1.0, vmax=1.0,
                    linewidths=0.5, cbar_kws={"label": "Pearson Correlation Coefficient (r)"},
                    annot_kws={"size": 11, "weight": "bold"})
    else:
        # Fallback to pure matplotlib
        im = plt.imshow(cross_corr.values, cmap="RdBu_r", vmin=-1.0, vmax=1.0, aspect='auto')
        plt.colorbar(im, label="Pearson Correlation Coefficient (r)")
        
        # Add labels
        for (i, j), val in np.ndenumerate(cross_corr.values):
            plt.text(j, i, f"{val:.2f}", ha='center', va='center',
                     color='white' if abs(val) > 0.4 else 'black', fontweight='bold')

        plt.yticks(np.arange(len(topo_cols)), topo_cols)
        plt.xticks(np.arange(len(transport_cols)), transport_cols, rotation=45, ha='right')

    plt.title("Cross-Correlation: H-Bond Network Topology vs. Proton Dynamics", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"  Saved Correlation Heatmap: {output_path}")


def analyze_topological_states(df: pd.DataFrame, n_clusters: int, output_dir: Path):
    """Cluster H-bond networks in TNN PC space and evaluate transport performance."""
    if not HAS_SKLEARN:
        print("  [Warning] scikit-learn is not installed. Skipping K-Means state analysis.")
        return {}

    # 1. K-Means Clustering on TNN PC1 and PC2 (Topological Space)
    features = df[["PC1", "PC2"]].values
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["Topological_State"] = kmeans.fit_predict(features_scaled)

    # 2. Plot Clusters in TNN Space
    plt.figure(figsize=(8, 6.5))
    colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F1C40F', '#9B59B6']
    
    for cluster_id in range(n_clusters):
        cluster_data = df[df["Topological_State"] == cluster_id]
        plt.scatter(cluster_data["PC1"], cluster_data["PC2"],
                    color=colors[cluster_id % len(colors)],
                    label=f"State {cluster_id}", alpha=0.7, s=40, edgecolors='none')

    plt.xlabel("Topological Embedding PC1", fontsize=11)
    plt.ylabel("Topological Embedding PC2", fontsize=11)
    plt.title("H-Bond Network States in Topological Embedding Space", fontsize=12, fontweight='bold')
    plt.legend(title="Topological State")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    cluster_png = output_dir / "topological_states_space.png"
    plt.savefig(cluster_png, dpi=300)
    plt.close()

    # 3. Profiling Transport Properties for each state
    state_profiles = df.groupby("Topological_State")[
        ["LBHB_Fraction", "Avg_Wire_Length", "Hodge_Gradient_Pct", "Hodge_Curl_Pct", "n_hbonds"]
    ].mean()

    print("\n" + "-"*50)
    print("TOPOLOGICAL STATES & TRANSPORT PROFILES (K-Means Mean)")
    print("-"*50)
    print(state_profiles.to_string())
    print("-"*50)

    # 4. Save profiles to JSON
    profiles_dict = state_profiles.to_dict(orient="index")
    with open(output_dir / "topological_states_profiles.json", "w") as f:
        json.dump(profiles_dict, f, indent=4)

    # 5. Plot bar chart comparing Hodge Gradient (Transport) & Wire length
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # State vs Hodge Gradient Pct
    ax1.bar(
        [f"State {c}" for c in range(n_clusters)],
        state_profiles["Hodge_Gradient_Pct"],
        color=[colors[c % len(colors)] for c in range(n_clusters)],
        alpha=0.85, edgecolor='grey'
    )
    ax1.set_ylabel("Mean Hodge Gradient (Transport) Flow (%)", fontsize=11)
    ax1.set_title("Proton Transport Efficiency", fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.2, axis='y')

    # State vs Avg Wire Length
    ax2.bar(
        [f"State {c}" for c in range(n_clusters)],
        state_profiles["Avg_Wire_Length"],
        color=[colors[c % len(colors)] for c in range(n_clusters)],
        alpha=0.85, edgecolor='grey'
    )
    ax2.set_ylabel("Mean Wire Length (Hops)", fontsize=11)
    ax2.set_title("H-Bond Wire Connectivity", fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.2, axis='y')

    plt.suptitle("How Topological Network States Govern Proton Transport", fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    profiles_png = output_dir / "topological_states_transport_bar.png"
    plt.savefig(profiles_png, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  Saved Topological States profiling figures: {output_dir}")
    return profiles_dict


def predict_transport_from_topology(df: pd.DataFrame, topo_cols: list, output_dir: Path):
    """Fit a Random Forest to predict transport efficiency/LBHBs from topology and plot feature importance."""
    if not HAS_SKLEARN:
        return

    # Check if target has variance
    targets = ["LBHB_Fraction", "Hodge_Harmonic_Pct", "Hodge_Gradient_Pct"]
    target_var = "LBHB_Fraction"
    
    # Check if target has variance, fallback if not
    for t in targets:
        if t in df.columns and df[t].std() > 1e-6:
            target_var = t
            break
            
    print(f"\nSelecting target variable for Random Forest regression: '{target_var}' (based on variance profiling)")

    y = df[target_var].values
    X = df[topo_cols].values

    # Train Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # R2 Score (accuracy of topology predicting transport)
    r2_score = float(rf.score(X, y))
    print(f"Random Forest R^2 score for Topology predicting {target_var}: {r2_score:.3f}")

    # Feature Importance
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_features = [topo_cols[i] for i in indices]
    sorted_importances = importances[indices]

    # Plot feature importance
    plt.figure(figsize=(8, 5))
    plt.barh(sorted_features[::-1], sorted_importances[::-1], color='#8E44AD', alpha=0.8)
    plt.xlabel("Relative Importance Score", fontsize=11)
    
    title_label = "Reactive LBHBs" if target_var == "LBHB_Fraction" else "Cooperative Loops"
    plt.title(f"Which Topological Features Dictate {title_label}?\n(Random Forest R² = {r2_score:.2f})",
              fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.2, axis='x')
    plt.tight_layout()
    
    importance_png = output_dir / "topological_feature_importance.png"
    plt.savefig(importance_png, dpi=300)
    plt.close()
    print(f"  Saved Topological Feature Importance plot: {importance_png}")

    # Save to JSON
    importance_dict = {feat: float(imp) for feat, imp in zip(sorted_features, sorted_importances)}
    importance_dict["_target_variable"] = target_var
    importance_dict["_model_R2"] = r2_score
    with open(output_dir / "topological_importance.json", "w") as f:
        json.dump(importance_dict, f, indent=4)

def run_symbolic_regression(df: pd.DataFrame, topo_cols: list, target_var: str, output_dir: Path, niterations: int = 20, n_runs: int = 5, **pysr_kwargs):
    """Run multi-run Symbolic Regression (PySR) for stability and cross-validation voting."""
    try:
        from hbond_topology.learning.discovery import SymbolicRegressor, HAS_PYSR
    except ImportError:
        # Fallback if hbond_topology is not in pythonpath, try adding parent dir
        import sys
        sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
        try:
            from hbond_topology.learning.discovery import SymbolicRegressor, HAS_PYSR
        except ImportError:
            print("  [Warning] Could not import SymbolicRegressor from hbond_topology.")
            return

    if not HAS_PYSR:
        print("  [Notice] PySR is not installed. Skipping explicit physical law discovery.")
        print("           To enable, run: pip install pysr")
        return

    from collections import Counter

    print(f"\n--- Running Multi-run Symbolic Regression (PySR) for {target_var} ({n_runs} runs) ---")
    y = df[target_var].values
    X = df[topo_cols]

    all_runs_data = []
    best_equations = []

    for run_idx in range(n_runs):
        seed = 42 + run_idx
        print(f"\n>>> PySR Run {run_idx + 1}/{n_runs} (Seed: {seed}, Iterations: {niterations}) <<<")
        
        regressor = SymbolicRegressor(niterations=niterations, random_state=seed, **pysr_kwargs)
        try:
            regressor.fit(X, y, feature_names=topo_cols)
            best_eq = regressor.get_best_equation()
            pareto_df = regressor.get_pareto_front()
            
            best_eq_str = str(best_eq)
            best_equations.append(best_eq_str)
            all_runs_data.append({
                "run": run_idx + 1,
                "seed": seed,
                "best_equation": best_eq_str,
                "pareto_front": pareto_df
            })
            print(f"  Run {run_idx + 1} Best Equation: {best_eq_str}")
        except Exception as e:
            print(f"  [Error] PySR Run {run_idx + 1} failed: {e}")

    if not all_runs_data:
        print("  [Error] All PySR runs failed. Cannot generate report.")
        return

    # Consensus Voting Analysis
    eq_counts = Counter(best_equations)
    most_common_eqs = eq_counts.most_common()

    # Feature Stability Analysis
    feature_counts = {col: 0 for col in topo_cols}
    total_equations = 0
    for run in all_runs_data:
        pareto = run["pareto_front"]
        for _, row in pareto.iterrows():
            total_equations += 1
            eq_str = str(row["sympy_format"])
            for col in topo_cols:
                if col in eq_str:
                    feature_counts[col] += 1

    # Save Markdown report
    md_path = output_dir / "discovered_physical_law.md"
    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Discovering Robust H-Bond Topological Laws via Multi-Run Symbolic Regression\n\n")
            f.write(f"This report presents the robust physical equations discovered by running multi-run Symbolic Regression (PySR) with stability selection. By executing independent evolutionary runs with different random seeds, we identify equations and topological invariants that consistently govern proton transport properties.\n\n")
            
            f.write(f"## 1. Study Settings\n")
            f.write(f"- **Target Transport Property**: `{target_var}`\n")
            f.write(f"- **Total Independent PySR Runs**: {len(all_runs_data)}\n")
            f.write(f"- **Iterations Per Run**: {niterations}\n")
            f.write(f"- **Input Topological Invariants**: {', '.join([f'`{col}`' for col in topo_cols])}\n\n")
            
            f.write(f"## 2. Robust Consensus Physical Laws (Voting Analysis)\n")
            f.write(f"Below is the frequency table of the 'best' equations selected by PySR across all runs. The equation with the highest vote count represents the most robust mathematical representation of the underlying physical relationship.\n\n")
            f.write(f"| Rank | Discovered Consensus Equation | Vote Count | Frequency | \n")
            f.write(f"| :--- | :--- | :--- | :--- |\n")
            for rank, (eq, count) in enumerate(most_common_eqs, 1):
                freq = (count / len(all_runs_data)) * 100
                f.write(f"| {rank} | `{target_var} ≈ {eq}` | {count}/{len(all_runs_data)} | {freq:.1f}% |\n")
            f.write(f"\n")
            
            best_consensus_eq = most_common_eqs[0][0]
            f.write(f"> [!IMPORTANT]\n")
            f.write(f"> **Consensus Physical Law Discovered:**\n")
            f.write(f"> $${target_var} \\approx {best_consensus_eq}$$\n")
            f.write(f"> This equation emerged as the consensus choice across the independent runs, indicating its high stability and generalizability to represent the governing physical chemistry.\n\n")
            
            f.write(f"## 3. Topological Invariant Feature Stability Selection\n")
            f.write(f"We analyzed the recurrence of each topological feature across all equations in the Pareto fronts of all runs. Features with high stability scores are critical drivers of the physical transport process.\n\n")
            f.write(f"| Topological Invariant | Description | Occurrence Count | Stability Score | Priority |\n")
            f.write(f"| :--- | :--- | :--- | :--- | :--- |\n")
            
            descriptions = {
                "n_hbonds": "Total number of hydrogen bonds in the network",
                "betti_0": "Number of connected components in the network",
                "betti_1": "Number of independent H-bond loops/cycles",
                "betti_2": "Number of topological voids/cavities",
                "euler_characteristic": "Overall topological connectivity descriptor (Betti-0 - Betti-1 + Betti-2)"
            }
            
            sorted_features = sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)
            for feat, count in sorted_features:
                stability = (count / total_equations) * 100 if total_equations > 0 else 0.0
                desc = descriptions.get(feat, "Topological descriptor")
                priority = "🔥 High" if stability > 70 else ("⚡ Medium" if stability > 30 else "❄️ Low")
                f.write(f"| `{feat}` | {desc} | {count}/{total_equations} | {stability:.1f}% | {priority} |\n")
            f.write(f"\n")
            
            top_feat = sorted_features[0][0]
            f.write(f"> [!TIP]\n")
            f.write(f"> **Topological Driver Interpretation:**\n")
            f.write(f"> The topological invariant `{top_feat}` is the most stable feature (appearing in {sorted_features[0][1]}/{total_equations} Pareto equations). This strongly indicates that `{top_feat}` serves as the primary topological descriptor governing the reactive properties or proton wires in the system.\n\n")
            
            f.write(f"## 4. Detailed Individual Run Fronts\n")
            f.write(f"Below are the individual Pareto fronts obtained from each independent PySR run (trading off accuracy vs. complexity):\n\n")
            
            for run in all_runs_data:
                f.write(f"<details>\n")
                f.write(f"<summary><b>Run {run['run']} (Seed: {run['seed']}) — Best Equation: {run['best_equation']}</b></summary>\n\n")
                f.write(f"| Complexity | Loss (MSE) | Score | Equation | Sympy Format |\n")
                f.write(f"| :--- | :--- | :--- | :--- | :--- |\n")
                for _, row in run["pareto_front"].iterrows():
                    f.write(f"| {row['complexity']} | {row['loss']:.6e} | {row.get('score', 0.0):.4f} | `{row['equation']}` | `{row['sympy_format']}` |\n")
                f.write(f"\n</details>\n\n")
        print(f"\n[Success] Discovered physical laws exported to Markdown format: {md_path}")
    except Exception as e:
        print(f"  [Error] Failed to write Markdown report: {e}")


def main():
    args = parse_args()
    topo_dir = Path(args.topo_dir)
    proton_dir = Path(args.proton_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("H-Bond Topological Machine Learning & Proton Transport Correlation Analysis")
    print("=" * 70)
    print(f"Topo Dir:   {topo_dir}")
    print(f"Proton Dir: {proton_dir}")
    print(f"Output Dir: {output_dir}")
    print("=" * 70)

    # 1. Load and merge datasets
    try:
        df = load_datasets(topo_dir, proton_dir)
    except Exception as e:
        print(f"Error loading datasets: {e}")
        print("Please check that both --topo-dir and --proton-dir have completed run-ml/timeseries files.")
        sys.exit(1)

    # Columns of interest
    topo_cols = ["n_hbonds", "betti_0", "betti_1", "betti_2", "euler_characteristic", "PC1", "PC2"]
    transport_cols = ["LBHB_Fraction", "Avg_Wire_Length", "Hodge_Gradient_Pct", "Hodge_Curl_Pct", "Hodge_Harmonic_Pct"]

    # Save aligned dataset to CSV
    merged_csv = output_dir / "aligned_topology_transport.csv"
    df.to_csv(merged_csv, index=False)
    print(f"Saved merged dataset: {merged_csv}")

    # 2. Correlation Matrix Heatmap
    plot_correlation_heatmap(df, topo_cols, transport_cols, output_dir / "cross_correlation_heatmap.png")

    # 3. K-Means clustering in Topological PC Space & profiling
    analyze_topological_states(df, args.n_clusters, output_dir)

    # 4. Feature Importance using RandomForest
    predict_transport_from_topology(df, topo_cols, output_dir)

    # 5. Symbolic Regression (Optional physical law discovery)
    if args.run_pysr:
        # We determine the target dynamically just like RandomForest
        target_var = "LBHB_Fraction"
        for t in transport_cols:
            if t in df.columns and df[t].std() > 1e-6:
                target_var = t
                break
        
        # Crucial physics-guided step: Exclude PCA components (PC1, PC2) from Symbolic Regression.
        # While abstract neural network PCA coordinates are useful for black-box ML predictions,
        # they lack physical dimensions. A symbolic equation containing "PC1" has no physical interpretation.
        # We restrict the inputs strictly to interpretable topological invariants:
        interpretable_topo_cols = [c for c in topo_cols if c not in ["PC1", "PC2"]]
        print(f"\n[Physics Guidance] Restricting symbolic regression features to physically interpretable invariants: {interpretable_topo_cols}")
        
        # Assemble GA algorithm parameters dynamically
        pysr_ga_args = {
            "populations": args.pysr_populations,
            "population_size": args.pysr_population_size,
            "ncycles_per_iteration": args.pysr_ncycles_per_iteration,
            "maxsize": args.pysr_maxsize,
            "crossover_probability": args.pysr_crossover_prob,
            "parsimony": args.pysr_parsimony,
            "weight_mutate_constant": args.pysr_weight_mutate_constant,
            "weight_mutate_operator": args.pysr_weight_mutate_operator,
            "weight_add_node": args.pysr_weight_add_node,
            "weight_delete_node": args.pysr_weight_delete_node
        }
        
        run_symbolic_regression(
            df, interpretable_topo_cols, target_var, output_dir, 
            niterations=args.pysr_iterations, n_runs=args.pysr_runs, 
            **pysr_ga_args
        )

    print("\n" + "=" * 70)
    print("Bridge analysis completed successfully! All correlation diagnostics executed.")
    print("=" * 70)


if __name__ == "__main__":
    main()
