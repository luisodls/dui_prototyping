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
