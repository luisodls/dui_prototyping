from dials.array_family import flex
import json
from dxtbx.model.experiment_list import ExperimentListFactory

def list_p_arrange(pos_col, hkl_col, pan_col, n_imgs):
    img_lst = []
    for time in range(n_imgs):
        img_lst.append([])

    txt_lab = "updating Predicted Reflections Data:"
    #my_bar = ProgBarBox(min_val=0, max_val=len(pos_col), text=txt_lab)
    print(" len(pos_col) = ", len(pos_col))

    for i, pos_tri in enumerate(pos_col):
        #my_bar(i)

        x_ini = '{:.2f}'.format(pos_tri[0] - 1)
        y_ini = '{:.2f}'.format((pos_tri[1] - 1) + pan_col[i] * 213)

        #x_ini = pos_tri[0] - 1
        #y_ini = (pos_tri[1] - 1) + pan_col[i] * 213

        if len(hkl_col) <= 1:
            local_hkl = ""

        else:
            local_hkl = hkl_col[i]
            if local_hkl == "(0, 0, 0)":
                local_hkl = "NOT indexed"

        xrs_size = 1
        int_z_centr = int(pos_tri[2])
        max_xrs_siz = 3
        for idx in range(int_z_centr - max_xrs_siz, int_z_centr + max_xrs_siz):
            xrs_size = max_xrs_siz - abs(int_z_centr - idx)
            if idx == int_z_centr:
                size2 = 2

            else:
                size2 = 0

            dat_to_append = [
                x_ini + "," + y_ini + "," +
                str(xrs_size) + "," + str(size2),
                local_hkl
             ]

            if idx >= 0 and idx < n_imgs:
                img_lst[idx].append(dat_to_append)

    #my_bar.ended()

    return img_lst


def get_refl_lst(expt_path, refl_path, img_num):
    experiments = ExperimentListFactory.from_json_file(expt_path)
    my_sweep = experiments.imagesets()[0]
    print("\n my_sweep.paths               ", my_sweep.paths())
    data_xy_flex = my_sweep.get_raw_data(0)[0].as_double()
    print("type(data_xy_flex) =", type(data_xy_flex))
    print("data_xy_flex.all() =", data_xy_flex.all())

    print("\n refl_path =", refl_path)

    table = flex.reflection_table.from_file(refl_path)
    pos_col = list(map(list, table["xyzcal.px"]))
    hkl_col = list(map(str, table["miller_index"]))
    pan_col = list(map(int, table["panel"]))

    n_imgs = len(my_sweep.indices())
    pred_spt_flat_data_lst = []
    if n_imgs > 0:
        pred_spt_flat_data_lst = list_p_arrange(
            pos_col, hkl_col, pan_col, n_imgs
        )
    return pred_spt_flat_data_lst[img_num]


if __name__ == "__main__":

    expt_path = "/scratch/dui_tst/dui_server_run/run6/refined.expt"
    refl_path = "/scratch/dui_tst/dui_server_run/run6/refined.refl"
    img_num = 0
    refl_lst = get_refl_lst(expt_path, refl_path, img_num)

    #print("\n img_num[", img_num, "] (refl) = \n", refl_lst)

    print("\n saving in json file")
    with open("refl_img.json", "w") as fp:
        json.dump(refl_lst, fp, indent = 2)

