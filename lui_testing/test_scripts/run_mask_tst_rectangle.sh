dials.import input.template="/home/luiso/dif_dat/I23_only_3_imgs_twise/test_3_####.cbf"
dials.generate_mask /tmp/run_dui2_nodes/run1/imported.expt untrusted.rectangle=909,1692,35,132 output.mask=tmp_mask.pickle
dials.apply_mask imported.expt input.mask=tmp_mask.pickle
dials.image_viewer masked.expt
