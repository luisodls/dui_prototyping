
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
cd ..

