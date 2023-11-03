dials.import input.template="/home/luiso/dif_dat/I23_big_good_2023_data/3p0_1_#####.cbf" dynamic_shadowing=True
dials.image_viewer imported.expt
dials.generate_mask ../run_dui2_nodes/mask_n_1.phil imported.expt
dials.apply_mask imported.expt input.mask=tmp_mask.pickle
dials.image_viewer masked.expt
