import subprocess
import os, sys
def run_cmd(cmd_in):
    procExe = subprocess.Popen(cmd_in,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    line = None
    while procExe.poll() is None or line != '':
        line = procExe.stdout.readline()
        print("Print:" + line[:-1])


if __name__ == "__main__":
    lst_cmd = [
        "dials.import /scratch/dui_test/X4_wide/X4_wide_M1S4_2_*.cbf output.experiments=1_experiments.expt output.log=1_import.log",
        "dials.find_spots spotfinder.mp.nproc=4 input.experiments=1_experiments.expt output.experiments=2_experiments.expt output.reflections=2_reflections.refl output.log=2_find_spots.log",
        "dials.index input.experiments=2_experiments.expt input.reflections=2_reflections.refl output.experiments=3_experiments.expt output.reflections=3_reflections.refl output.log=3_index.log",
        "dials.refine_bravais_settings input.experiments=3_experiments.expt input.reflections=3_reflections.refl output.prefix=lin_4_ output.log=4_refine_bravais_settings.log",
        "dials.reindex input.reflections=3_reflections.refl change_of_basis_op=b,c,a output.reflections=5_reflections.refl",
        "dials.refine input.experiments=lin_4_bravais_setting_9.expt input.reflections=5_reflections.refl output.experiments=6_experiments.expt output.reflections=6_reflections.refl output.log=6_refine.log",
        "dials.integrate integration.mp.nproc=2 input.experiments=6_experiments.expt input.reflections=6_reflections.refl output.experiments=8_experiments.expt output.reflections=8_reflections.refl output.phil=8_integrate.phil output.log=8_integrate.log",
        "dials.symmetry input.experiments=8_experiments.expt input.reflections=8_reflections.refl output.experiments=9_experiments.expt output.reflections=9_reflections.refl output.log=9_symmetry.log output.json=9_symmetry.symmetry.json",
        "dials.scale input.experiments=9_experiments.expt input.reflections=9_reflections.refl output.experiments=10_experiments.expt output.reflections=10_reflections.refl output.log=10_scale.log",
        "dials.export mtz.hklout=scaled.mtz intensity=scale 10_experiments.expt 10_reflections.refl output.log=11_export.log",
    ]

    for command2run in lst_cmd:
        run_cmd(command2run)




tst5 = '''
process = subprocess.Popen(
    'my_command',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
    encoding='utf-8',
    errors='replace'
)

while True:
    realtime_output = process.stdout.readline()

    if realtime_output == '' and process.poll() is not None:
    break

    if realtime_output:
    print(realtime_output.strip(), flush=True)
'''
