import os, sys, glob, shutil

#shutil.copy('source.txt', 'destination.txt')

lst_n_imgs = [103, 211, 95, 265, 155]
lst_dir_name = []
for num_dir_0, size_n in enumerate(lst_n_imgs):
    print("num_dir_0, size_n =", num_dir_0, size_n)
    dir_name = "C2sum_n"+ str(num_dir_0) + "_w_" + str(size_n) + "_imgs"
    print("dir_name =", dir_name)
    lst_dir_name.append(dir_name)

    try:
        os.mkdir(dir_name)

    except FileExistsError:
        sys.exit("Dir Exists Error")

lst_ini = sorted(glob.glob("*.cbf.gz"))

#########################################

num_sub_lst = 0
pos_dir = 0

for file_ini in lst_ini:
    num_sub_lst += 1
    num_str = "{:0>4s}".format(str(num_sub_lst))
    #print("num_sub_lst =", num_str)
    dir_name = lst_dir_name[pos_dir]
    file_end = dir_name + "/" + file_ini[0:-11] + num_str + ".cbf.gz"
    print("file_ini =", file_ini, " //  file_end =", file_end)
    shutil.copy( file_ini, file_end)

    if num_sub_lst == lst_n_imgs[pos_dir]:
        num_sub_lst = 0
        pos_dir +=1
        print("\n dir")

