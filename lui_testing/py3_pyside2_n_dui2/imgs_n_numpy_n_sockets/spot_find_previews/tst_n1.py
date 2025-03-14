import numpy as np
from matplotlib import pyplot as plt

from dials.array_family import flex
from dxtbx.model import ExperimentList
from dxtbx.flumpy import to_numpy

def draw_pyplot(img_arr):
    plt.imshow(img_arr, interpolation = "nearest")
    plt.show()


def get_np_full_img(raw_dat):
    i23_multipanel = False
    print("Using the first panel only")
    data_xy_flex = raw_dat[0].as_double()
    np_arr = to_numpy(data_xy_flex)

    print("type(np_arr[0,0]) = " + str(type(np_arr[0,0])))

    return np_arr, i23_multipanel


if __name__ == "__main__":
    exp_path = "/tmp/run_dui2_nodes/run1/imported.expt"
    experiments = ExperimentList.from_file(exp_path)
    my_sweep = experiments.imagesets()[0]

    #print("dir(my_sweep)", dir(my_sweep))
    '''
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getinitargs__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__safe_for_unpickling__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'as_imageset', 'clear_cache', 'complete_set', 'data', 'external_lookup', 'get_array_range', 'get_beam', 'get_corrected_data', 'get_detector', 'get_detectorbase', 'get_format_class', 'get_gain', 'get_goniometer', 'get_image_identifier', 'get_mask', 'get_path', 'get_pedestal', 'get_raw_data', 'get_scan', 'get_spectrum', 'get_template', 'get_vendortype', 'has_dynamic_mask', 'indices', 'is_marked_for_rejection', 'mark_for_rejection', 'masker', 'params', 'partial_set', 'paths', 'reader', 'set_beam', 'set_detector', 'set_goniometer', 'set_scan', 'size', 'update_detector_px_mm_data']
    '''

    print("dir(my_sweep.params)", dir(my_sweep.params), "\n")
    print("my_sweep.params() =", my_sweep.params())


    on_sweep_img_num = 0
    raw_dat = my_sweep.get_raw_data(on_sweep_img_num)

    np_arr, i23_multipanel = get_np_full_img(raw_dat)

    draw_pyplot(np_arr)

    print("type(np_arr) = ", type(np_arr))

