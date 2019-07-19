from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy
from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory

import pickle

n_json_file_path = "/tmp/dui_run/dui_files/2_datablock.json"
datablocks = DataBlockFactory.from_json_file(n_json_file_path)
# TODO check length of datablock for safety
datablock = datablocks[0]
my_sweep = datablock.extract_sweeps()[0]
img_arr = my_sweep.get_raw_data(0)[0].as_double()


###############################################################################

experiments = ExperimentListFactory.from_json_file(
                n_json_file_path, check_format=False
            )

imageset_tmp = experiments.imagesets()[0]
mask_file = imageset_tmp.external_lookup.mask.filename

pick_file = open(mask_file, "rb")
mask_tup_obj = pickle.load(pick_file)
pick_file.close()

mask_flex = mask_tup_obj[0]
mask_np_arr = mask_flex.as_numpy_array()
np_mask = mask_np_arr


##############################################################################

algorithm = DispersionThresholdStrategy(
        kernel_size = (3, 3),
        gain = 1,
        n_sigma_b = 6,
        n_sigma_s = 3,
        min_count = 2,
        global_threshold = 0
)

algr = algorithm(img_arr, mask_flex)

np_alg = algr.as_numpy_array()

print np_alg


from matplotlib import pyplot as plt
plt.imshow( np_alg , interpolation = "nearest" )
plt.show()

