from dials.algorithms.spot_finding.threshold import DispersionThresholdStrategy
from dxtbx.datablock import DataBlockFactory
from dxtbx.model.experiment_list import ExperimentListFactory
from dials.algorithms.image.threshold import DispersionThresholdDebug
from dials.array_family import flex
import pickle

# remember to run DUI and generate the needed file in dui_files
# do import and then do mask tool

n_json_file_path = "/tmp/dui_run/dui_files/2_datablock.json"
datablocks = DataBlockFactory.from_json_file(n_json_file_path)
# TODO check length of datablock for safety
datablock = datablocks[0]
my_sweep = datablock.extract_sweeps()[0]
img_arr = my_sweep.get_raw_data(0)[0].as_double()
img_raw = my_sweep.get_raw_data(0)[0]

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
print "type(mask_flex) =", type(mask_flex)


##############################################################################
copy_pasted = '''
DispersionThresholdDebug(
                        raw_data[i_panel].as_double(),
                        mask[i_panel],
                        gain_map[i_panel],
                        size,
                        nsigma_b,
                        nsigma_s,
                        global_threshold,
                        min_local,
                    )
'''

gain_value = 1
gain_map = flex.double(img_raw.accessor(), gain_value)


print "type(img_arr  )", type(img_arr  )
print "type(mask_flex)", type(mask_flex)
print "type(gain_map )", type(gain_map )

print "img_arr.all()  ", img_arr.all()
print "mask_flex.all()", mask_flex.all()
print "gain_map.all() ", gain_map.all()


#db_gain = flex.double(flex.grid(img_arr.all()))
#db_gain = gain_map


test_algo = DispersionThresholdDebug(
                        img_arr,
                        mask_flex,
                        gain_value,
                        (3, 3),
                        6,3,0,2)

###############################################################################


'''
from matplotlib import pyplot as plt
plt.imshow( np_alg , interpolation = "nearest" )
plt.show()

'''
