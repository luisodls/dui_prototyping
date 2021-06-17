from dials.array_family import flex
import json
#import time
#import zlib
from dxtbx.model.experiment_list import ExperimentListFactory

if __name__ == "__main__":

    exp_path = "/scratch/dui_tst/dui_server_run/run6/refined.expt"
    experiments = ExperimentListFactory.from_json_file(exp_path)
    my_sweep = experiments.imagesets()[0]
    print("\n my_sweep.paths               ", my_sweep.paths())
    data_xy_flex = my_sweep.get_raw_data(0)[0].as_double()
    print("type(data_xy_flex) =", type(data_xy_flex))
    print("data_xy_flex.all() =", data_xy_flex.all())

    refl_path = "/scratch/dui_tst/dui_server_run/run6/refined.refl"
    print("\n refl_path =", refl_path)
