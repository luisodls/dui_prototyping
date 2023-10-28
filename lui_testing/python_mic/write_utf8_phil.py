lst_str = []

lst_str.append("untrusted {")
lst_str.append("  panel = 1")
lst_str.append("  rectangle = 676 1188 48 136")
lst_str.append("}")
lst_str.append("untrusted {")
lst_str.append("  panel = 2")
lst_str.append("  circle = 1644 88 189")
lst_str.append("}")
lst_str.append("untrusted {")
lst_str.append("  panel = 4")
lst_str.append("  rectangle = 724 1276 40 148")
lst_str.append("}")

f = open('tst.phil', 'w', encoding="utf-8")

for str_2_write in lst_str:
    f.write(str_2_write + "\n")

f.close()
