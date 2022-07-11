
Notes_from_DUI_demo = '''
Remove arrow heads from the lines on the tree. The direction of flow is implicit
There is no radial_profile threshold algorithm yet for ED spot-finding. This is not in CCP4's DIALS though.
Set d_min as well as d_max on the spot-finding simple input
heuristic to always tick the detector.fix=distance box for ED (scattering angle of highest resolution spot < 5°, for example)
Online help as a priority
'''

from dxtbx.model.experiment_list import (
    ExperimentListFactory,
    InvalidExperimentListError,
)

def get_template_info(exp_path):
    experiments = ExperimentListFactory.from_json_file(
        exp_path
    )
    print("dir(experiments.beams) =", dir(experiments.beams))
    print("experiments.beams =", experiments.beams)
    print("experiments.beams() =", experiments.beams())
    print("experiments.beams()[0] =", experiments.beams()[0])
    print("type(experiments.beams()[0]) =", type(experiments.beams()[0]))
    print("dir(experiments.beams()[0]) =", dir(experiments.beams()[0]))
    print(
        "experiments.beams()[0].get_wavelength() =",
        experiments.beams()[0].get_wavelength()
    )
    print(
        "type(experiments.beams()[0].get_wavelength()) =",
        type(experiments.beams()[0].get_wavelength())
    )

if __name__ == "__main__":
    get_template_info("/tmp/run2/imported.expt")
