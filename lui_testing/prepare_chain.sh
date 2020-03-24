
source /scratch/conda_s_gcc_dials/build/setpaths.sh
cd /tmp/
ls
mkdir dui2run
cd dui2run/
mkdir tst_chain
cd tst_chain/
mkdir imp_dir
cd imp_dir/
dials.import /scratch/dui_data/X4_wide/X4_wide_M1S4_2_000*.cbf
dials.import /scratch/dui_tst/X4_wide/X4_wide_M1S4_2_000*.cbf

cd ..


dials.python /scratch/dui_prototyping/lui_testing/py3_pyside2_n_dui2/subprocess_n_connections/chain_tst_02.py
