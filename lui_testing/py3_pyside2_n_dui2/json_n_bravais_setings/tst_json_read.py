import json
import logging
import sys
import os

def choice_if_decimal(num_in):

    str_f = "{:6.2f}".format(num_in)
    if str_f[-3:] == ".00":
        str_out = str_f[0:-3]

    else:
        str_out = str_f

    return str_out

def ops_list_from_json(json_path=None):
    if json_path is None:
        return None

    with open(json_path) as json_file:
        json_data = json.load(json_file)

    #print(json_data)


    lst_ops = []
    for key, value in json_data.items():
        recommended_str = "  "
        print("outer key:", key)
        print("outer dict:", value)
        for inner_key in value:
            if inner_key == "rmsd":
                rmsd_val = value["rmsd"]
                rmsd_str = " {:7.2}".format(rmsd_val)

            elif inner_key == "min_cc":
                try:
                    min_cc_val = value["min_cc"]
                    min_cc_str = " {:7.2}".format(min_cc_val)

                except TypeError:
                    min_cc_str = "    - "

                # TODO the format here is not always giving the same with

                # TODO think about someting like:
                #   "aa = list(round(i, ndigits=6) for i in aa)"

            elif inner_key == "max_cc":
                max_cc_val = value["max_cc"]
                try:
                    max_cc_str = " {:7.2}".format(max_cc_val)

                except TypeError:
                    max_cc_str = "    - "

                # print "__________________________________________
                # type(max_cc_val) =", type(max_cc_val)
                # TODO the format here is not always giving the same with

                # TODO think about someting like:
                #   "aa = list(round(i, ndigits=6) for i in aa)"

            elif inner_key == "bravais":
                bravais_val = value["bravais"]
                bravais_str = " " + str(bravais_val).ljust(3)

            elif inner_key == "max_angular_difference":
                angular_diff_val = value["max_angular_difference"]
                angular_diff_str = " {:7.2} ".format(angular_diff_val)

            elif inner_key == "correlation_coefficients":
                # corr_coeff_val = value["correlation_coefficients"]
                # corr_coeff_str = str(corr_coeff_val)
                pass

            elif inner_key == "unit_cell":
                unit_cell_val = value["unit_cell"]
                uc_d = unit_cell_val[0:3]
                uc_a = unit_cell_val[3:6]
                unit_cell_str_a = "{:6.1f}".format(uc_d[0])
                unit_cell_str_b = "{:6.1f}".format(uc_d[1])
                unit_cell_str_c = "{:6.1f}".format(uc_d[2])

                unit_cell_str_apl = choice_if_decimal(uc_a[0])
                unit_cell_str_bet = choice_if_decimal(uc_a[1])
                unit_cell_str_gam = choice_if_decimal(uc_a[2])

            elif inner_key == "recommended":
                recommended_val = value["recommended"]
                if recommended_val:
                    recommended_str = " Y"
                else:
                    recommended_str = " N"

            else:
                print("Fell off end of key list with inner_key=", inner_key)

        single_lin_lst = [
            int(key),
            angular_diff_str,
            rmsd_str,
            min_cc_str,
            max_cc_str,
            bravais_str,
            unit_cell_str_a,
            unit_cell_str_b,
            unit_cell_str_c,
            unit_cell_str_apl,
            unit_cell_str_bet,
            unit_cell_str_gam,
            recommended_str,
        ]

        lst_ops.append(single_lin_lst)

    sorted_lst_ops = sorted(lst_ops)
    return sorted_lst_ops

if __name__ == "__main__":
    ops_list_from_json("/scratch/dui_tst/X4_wide/dui_files/bravais_summary.json")
