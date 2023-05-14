def lst_sort(lst_in):
    lst_out = [lst_in[0]]
    for elem in lst_in:
        for pos, iner_elem in enumerate(lst_out):
            if elem < iner_elem:
                lst_out.insert(pos, elem)

    print("lst_out =", lst_out)

if __name__ == "__main__":
    str_ini = ["aaab", "bbc", "1"]
    lst_sort(str_ini)
