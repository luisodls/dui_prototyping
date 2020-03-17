
mkdir tst1
cd tst1
dials.import /tmp/dui2run/imgs/X4_wide_M1S4_2_00*.cbf image_range=1,12
cd ..
mkdir tst2
cd tst2/
dials.find_spots  ../tst1/*.expt ../tst1/*.refl spotfinder.threshold.dispersion.gain=1.1 spotfinder.threshold.dispersion.kernel_size=3,3 spotfinder.threshold.dispersion.sigma_background=6.0 spotfinder.threshold.dispersion.sigma_strong=3.5 spotfinder.threshold.dispersion.min_local=2 spotfinder.threshold.dispersion.global_threshold=0.0 spotfinder.mp.nproc=4
cd ..
mkdir tst3
cd tst3/
dials.index ../tst1/*.expt ../tst2/*.refl indexing.method=fft1d
cd ..
mkdir tst4
cd tst4/
dials.refine ../tst3/*.expt ../tst3/*.refl refinement.reflections.outlier.algorithm=tukey
cd ..
mkdir tst5
cd tst5/
dials.integrate ../tst4/*.expt ../tst4/*.refl integration.mp.nproc=4
cd ..
mkdir tst6
cd tst6/
dials.scale ../tst5/*.expt ../tst5/*.refl
cd ..
mkdir tst7
cd tst7/
dials.symmetry ../tst6/*.expt ../tst6/*.refl
cd ..

