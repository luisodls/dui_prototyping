from main_gui import *

import sys

#from PyQt4 import QtGui, QtCore

def create_steps():

    steps = []

    import_step = step()
    import_step.Bttlabel = "\n\n     import    \n\n"
    import_step.default_action = "dials.import ~/data/th_8_2_0*"
    import_step.InnerBox = btn__img_ibox()
    steps.append(import_step)

    find_step = step()
    find_step.Bttlabel = "\n\n     find spots    \n\n"
    find_step.default_action = "dials.find_spots datablock.json"
    find_step.InnerBox = EmptyInnerBox()
    steps.append(find_step)

    index_step = step()
    index_step.Bttlabel = "\n\n     index    \n\n"
    index_step.default_action = "dials.index datablock.json strong.pickle"
    index_step.InnerBox = btn__img_ibox()
    steps.append(index_step)

    refine_step = step()
    refine_step.Bttlabel = "\n\n     refine    \n\n"
    refine_step.default_action = "dials.refine experiments.json indexed.pickle"
    refine_step.InnerBox = EmptyInnerBox()
    steps.append(refine_step)

    integrate_step = step()
    integrate_step.Bttlabel = "\n\n     integrate    \n\n"
    integrate_step.default_action = "dials.integrate refined_experiments.json refined.pickle"
    integrate_step.InnerBox = btn__img_ibox()
    steps.append(integrate_step)

    export_step = step()
    export_step.Bttlabel = "\n\n     export    \n\n"
    export_step.default_action = "dials.export integrated.pickle integrated.h5"
    export_step.InnerBox = EmptyInnerBox()
    steps.append(export_step)

    return steps


if __name__ == '__main__':

    app =  QApplication(sys.argv)
    btn_steps = create_steps()
    ex = MainWidget(btn_steps)
    sys.exit(app.exec_())

