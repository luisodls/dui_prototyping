from dials.array_family import flex
from dxtbx.model.experiment_list import ExperimentListFactory
import time

def get_experiments(experiment_path):
    print("importing from:" + experiment_path)
    for repeat in range(10):
        try:
            new_experiments = ExperimentListFactory.from_json_file(
                experiment_path
            )
            break

        except OSError:
            new_experiments = None
            print("OS Err catch in ExperimentListFactory, trying again")
            time.sleep(0.333)

    return new_experiments


if __name__ == "__main__":
    print("\n on_sweep_img_num =", 5)
    experiments = get_experiments(
        "/scratch/30day_tmp/run_dui2_nodes/run1/imported.expt"
        #"/tmp/run_dui2_nodes/run1/imported.expt"
    )
    my_sweep = experiments.imagesets()[0]
    raw_dat = my_sweep.get_raw_data(5)
    data_xy_flex = raw_dat[0].as_double()
    np_arr = data_xy_flex.as_numpy_array()
