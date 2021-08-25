import os
lst_files = sorted(os.listdir())
for file_name in lst_files[0:-2]:
    left_side = file_name[:9]

    mid_side =  str(int(file_name[9:12]) - 300)
    if len(mid_side) < 3:
        mid_side = "0" * (3 - len(mid_side)) + mid_side

    right_side = file_name[12:]

    new_file_name = left_side + mid_side + right_side

    #print( file_name, " to convert to ", new_file_name)
    os.rename(file_name, new_file_name)
