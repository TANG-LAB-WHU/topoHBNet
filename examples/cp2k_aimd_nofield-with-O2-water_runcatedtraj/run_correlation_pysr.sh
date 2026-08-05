#!/bin/bash
#SBATCH --job-name=topo_corr_pysr
#SBATCH --partition=9a14a
#SBATCH --account=tangsiqi
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=192        # Allocate all 192 CPU cores in 9a14a partition
#SBATCH --output=pysr_run_%j.log

# Load environment
# module load nvidia/cuda/12.9 2>/dev/null || module load nvidia/cuda/12.2 2>/dev/null

# Activate conda environment
source ~/miniconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/.bashrc
conda activate topoHBNet_env

# Set PySR/juliacall thread environment variables to 1 (we are using 192 processes instead of 192 threads)
export JULIA_NUM_THREADS=1
export PYTHON_JULIACALL_THREADS=1
export PYTHON_JULIACALL_HANDLE_SIGNALS=yes

# Restrict math libraries to 1 thread to prevent thread explosion
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_MAX_THREADS=1
export OPENBLAS_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=""

# Offline flags for PySR and Julia
export PYTHON_JULIAPKG_OFFLINE=yes
export JULIA_PKG_OFFLINE=true
export JULIA_DEPOT_PATH="/scratch/tangsiqi/julia_depot"

# Fix GLIBCXX version error by pointing to Conda's modern C++ library
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"

# Change to the submit directory
if [ -n "$SLURM_SUBMIT_DIR" ]; then
    cd "$SLURM_SUBMIT_DIR"
else
    cd "$(dirname "$0")"
fi

echo "============================================================"
echo "  H-Bond Topology & Proton Transport Correlation Analysis"
echo "  Running multi-run PySR Symbolic Regression"
echo "  Node: $(hostname)  |  Partition: 9a14a"
echo "  Working Dir: $(pwd)"
echo "  Conda Env: $CONDA_DEFAULT_ENV"
echo "  Start Time: $(date)"
echo "============================================================"

# Run the correlation and symbolic regression analysis script
python -u correlate_topology_and_transport.py \
    --topo-dir topoHBNet-run-ml \
    --proton-dir proton_transfer_results \
    --elec-dir interfacial_analysis_results \
    --output-dir topology_transport_correlation_results \
    --equil-start-frame 4000 \
    --n-clusters 0 \
    --run-pysr

EXIT_CODE=$?

echo "============================================================"
echo "  Job finished with exit code: $EXIT_CODE"
echo "  End Time: $(date)"
echo "============================================================"

exit $EXIT_CODE
