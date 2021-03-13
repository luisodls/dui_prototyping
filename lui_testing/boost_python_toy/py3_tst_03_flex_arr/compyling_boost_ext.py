from subprocess import call as shell_call
from distutils import sysconfig

obj_name = "img_stream_ext"
inc_path = sysconfig.get_python_inc()
print("\n sysconfig.get_python_inc() =", inc_path)
for pos, single_shar in enumerate(inc_path):
    if(single_shar == "/" ):
        cut_inc_path = inc_path[0:pos]


import scitbx
scitbx_path = scitbx.__path__[0]
print("\n scitbx_path =", scitbx_path)
cut_scitbx_path = scitbx_path[0:-6]
print("cut_scitbx_path =", cut_scitbx_path)
com_lin_01 = "g++ -I" + inc_path + " -I" + \
    cut_inc_path +  " -fPIC -c "+ " -I" + cut_scitbx_path \
    + " -I/scratch/dials_conda/modules" \
    + " -I/scratch/dials_conda/build/annlib_adaptbx/include" \
    + " -I/scratch/dials_conda/build/include" \
    + " " + obj_name + ".cpp"


print("com_lin_01 =\n", com_lin_01)

lib_path = sysconfig.get_python_lib()

for pos, single_shar in enumerate(lib_path):
    if(single_shar == "/" ):
        cut_lib_path = lib_path[0:pos]

for pos, single_shar in enumerate(cut_lib_path):
    if(single_shar == "/" ):
        cut_cut_lib_path = cut_lib_path[0:pos]




com_lin_02 = "g++ -shared " + obj_name + ".o -L" +   \
    cut_cut_lib_path + " -lboost_python38 -L" +      \
    cut_lib_path + "/config -lpython3.8 -o " + obj_name + ".so"

print("\n Compiling line 1:")
print("cmd =", com_lin_01, "\n")
err_msg_01 = shell_call(com_lin_01, shell=True)
print("\n Compiling line 2:")
print("cmd =", com_lin_02, "\n")
err_msg_02 = shell_call(com_lin_02, shell=True)
print("\n Done compiling")

if(err_msg_01 != 0 or err_msg_02 !=0 ):
    print("Failed to compile some C++ extensions ")
