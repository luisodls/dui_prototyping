"""
Display a plot and an image with minimal setup.

pg.plot() and pg.image() are indended to be used from an interactive prompt
to allow easy data inspection (but note that PySide unfortunately does not
call the Qt event loop while the interactive prompt is running, in this case
it is necessary to call QApplication.exec_() to make the windows appear).
"""
import PySide
import numpy as np
import pyqtgraph as pg

arr_i = np.arange(400 * 400).reshape(400, 400)
pg.image(arr_i, title="Simplest possible image example")


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
