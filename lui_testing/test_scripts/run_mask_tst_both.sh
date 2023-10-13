rm masked.expt
rm tmp_mask.pickle
dials.import input.template="/home/luiso/dif_dat/I23_only_3_imgs_twise/test_3_####.cbf"
#dials.import input.template="/home/lui/dif_dat/I23_only_3_imgs_twise/test_3_####.cbf"

#dials.generate_mask imported.expt untrusted.panel=5 untrusted.rectangle=909,1692,35,132 output.mask=tmp_mask.pickle
dials.generate_mask imported.expt untrusted.rectangle=90,169,55,122 untrusted.rectangle=909,1692,35,132,2 untrusted.rectangle=509,1492,35,132,7  output.mask=tmp_mask.pickle

dials.apply_mask imported.expt input.mask=tmp_mask.pickle
dials.image_viewer masked.expt
