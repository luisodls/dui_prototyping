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

if __name__ == "__main__":
    a = np.arange(60, dtype=float).reshape(6,10)
    print("a =\n", a)
    '''
    for x in np.nditer(a, op_flags=['readwrite'], flags = ['external_loop']):
        x[...]=x*2
    '''
    b = np.zeros((3,10))
    for row_num in range(b.shape[0]):
        for sub_row_num in range(2):
            b[row_num, :] += a[row_num * 2 + sub_row_num, :]

    print("b =\n", b)

    c = np.zeros((3,5))
    for col_num in range(c.shape[1]):
        for sub_col_num in range(2):
            c[:, col_num] += b[:, col_num * 2 + sub_col_num]

    print("c =\n", c)
    a_scl = np.copy(c)
    a_scl = a_scl / 4.0
    print("a_scl =\n", a_scl)
