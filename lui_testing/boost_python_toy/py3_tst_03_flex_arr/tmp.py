from distutils import sysconfig

dict_conf_vars = sysconfig.get_config_vars()
print("\n", dict_conf_vars["prefix"])
prefix_path = dict_conf_vars["prefix"]
cut_prefix = prefix_path[0:-10]
print("cut_prefix =", cut_prefix)
inc_path = cut_prefix + "build/include"
print("inc_path =", inc_path)
'''
print("sysconfig.get_config_vars   ", sysconfig.get_config_vars())
print("type(sysconfig.get_config_vars) ", type(sysconfig.get_config_vars()))
for key in dict_conf_vars:
    print("\n", key, ":", dict_conf_vars[key])

import sys
print(sys.path)

import scitbx
print("\n",scitbx.__path__)

import cctbx
print("\n",dir(cctbx))
'''
