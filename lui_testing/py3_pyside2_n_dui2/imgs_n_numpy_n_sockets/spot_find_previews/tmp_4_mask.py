
from dials.array_family import flex
from dxtbx.model import ExperimentList



n_json_file_path = "/tmp/run_dui2_nodes/run1/imported.expt"
n_json_file_path = "/tmp/run_dui2_nodes/run2/masked.expt"
experiments = ExperimentList.from_file(n_json_file_path)
my_sweep = experiments.imagesets()[0]

on_sweep_img_num = 0
image = my_sweep.get_raw_data(on_sweep_img_num)[0]


print(dir(experiments), "\n\n")
print(dir(my_sweep.external_lookup), "\n\n")
print(my_sweep.external_lookup.mask.filename, "\n\n")


#######################################################################################

'''
mask_file = "/tmp/run_dui2_nodes/run2/tmp_mask.pickle"
#mask_file = "/scratch/30day_tmp/run_dui2_nodes/run2/tmp_mask.pickle"

mask_file = self.imageset.external_lookup.mask.filename
'''
