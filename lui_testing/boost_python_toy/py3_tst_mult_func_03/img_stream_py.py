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

def scale_np_arr(big_np_arr, inv_scale):
    a_d0 = big_np_arr.shape[0]
    a_d1 = big_np_arr.shape[1]
    small_d0 = int(a_d0 / inv_scale)
    short_arr = np.zeros((small_d0, a_d1))
    for row_num in range(small_d0):
        row_cou = 0
        for sub_row_num in range(inv_scale):
            big_row = row_num * inv_scale + sub_row_num
            if big_row < a_d0:
                short_arr[row_num,:] += big_np_arr[big_row, :]
                row_cou += 1

        short_arr[row_num,:] /= float(row_cou)

    small_d1 = int(a_d1 / inv_scale)
    small_arr = np.zeros((small_d0, small_d1))
    for col_num in range(small_arr.shape[1]):
        col_cou = 0
        for sub_col_num in range(inv_scale):
            big_col = col_num * inv_scale + sub_col_num
            if big_col < a_d1:
                small_arr[:,col_num] += short_arr[:,big_col]
                col_cou += 1

        small_arr[:,col_num] /= float(col_cou)

    return small_arr

if __name__ == "__main__":
    d0, d1 = 15, 10
    big_arr = np.arange(d0 * d1, dtype=float).reshape(d0, d1)
    print("big_arr =\n", big_arr)
    scaled_arr = scale_np_arr(big_arr, 5)
    print("scaled_arr =\n", scaled_arr)

