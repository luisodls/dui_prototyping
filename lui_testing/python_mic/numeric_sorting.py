def build_lst_w_names(size = 20, n_times = 3):
    lst_out = []
    for iters in range(n_times):
        for inner_iters in range(size):
            new_str = "aa_" + str(iters) + "_bb_" + str(inner_iters) + "_cc"
            lst_out.append(new_str)

    return lst_out

def get_number_from_string(str_in):
    num_char = ""
    for char_part in str_in:
        if char_part in "0123456789":
            num_char += char_part

    return int(num_char)




if __name__ == "__main__":
    my_lst = build_lst_w_names(size = 15, n_times = 2)

    print("my_lst =", my_lst)
    new_lst = sorted(my_lst, key=get_number_from_string)
    print("\n new_lst =", new_lst)

    lst_n_2 = sorted(my_lst)
    print("\n lst_n_2 =", lst_n_2)
