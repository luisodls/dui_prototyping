import numpy as np
def slice_arr_2_str( data2d, inv_scale, x1, y1, x2, y2):
    data_xy_flex = data2d.as_double()
    np_arr = data_xy_flex.as_numpy_array()
    d1 = np_arr.shape[0]
    d2 = np_arr.shape[1]
    str_tup = str(tuple(np_arr.ravel()))
    str_data = "{\"d1\":" + str(d1) + ",\"d2\":" + str(d2) \
             + ",\"str_data\":\"" + str_tup[1:-1] + "\"}"

    return str_data

'''
def get_json_w_img_2d(experiments_list_path, img_num):
    pan_num = 0
    print("experiments_list_path, img_num:", experiments_list_path, img_num)
    experiments_path = experiments_list_path[0]
    print("importing from:", experiments_path)
    experiments = ExperimentListFactory.from_json_file(experiments_path)

    on_sweep_img_num, n_sweep = get_correct_img_num_n_sweep_num(
        experiments, img_num
    )

    my_sweep = experiments.imagesets()[n_sweep]
    data_xy_flex = my_sweep.get_raw_data(on_sweep_img_num)[pan_num].as_double()

    start_tm = time.time()
    np_arr = data_xy_flex.as_numpy_array()
    d1 = np_arr.shape[0]
    d2 = np_arr.shape[1]
    str_tup = str(tuple(np_arr.ravel()))
    str_data = "{\"d1\":" + str(d1) + ",\"d2\":" + str(d2) \
             + ",\"str_data\":\"" + str_tup[1:-1] + "\"}"

    end_tm = time.time()
    print("str/tuple use and compressing took ", end_tm - start_tm)

    return str_data
'''

def scale_np_arr(a, inv_scale):
    print("a =\n", a)
    a_d0 = a.shape[0]
    a_d1 = a.shape[1]
    small_d0 = int(a_d0 / inv_scale)
    b = np.zeros((small_d0, a_d1))
    for row_num in range(small_d0):
        for sub_row_num in range(inv_scale):
            b[row_num, :] += a[row_num * inv_scale + sub_row_num, :]

    print("b =\n", b)
    small_d1 = int(a_d1 / inv_scale)
    c = np.zeros((small_d0, small_d1))
    for col_num in range(c.shape[1]):
        for sub_col_num in range(inv_scale):
            c[:, col_num] += b[:, col_num * inv_scale + sub_col_num]

    print("c =\n", c)
    a_scl = np.copy(c)
    a_scl = a_scl / float(inv_scale ** 2)
    print("a_scl =\n", a_scl)


if __name__ == "__main__":
    d0, d1 = 15, 12
    big_arr = np.arange(d0 * d1, dtype=float).reshape(d0, d1)
    scaled_arr = scale_np_arr(big_arr, 3)
