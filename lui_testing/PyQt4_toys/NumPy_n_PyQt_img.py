import numpy as np

#from PySide.QtGui import QImage, QLabel, QPixmap, QApplication
from PyQt4.QtGui import QImage, QLabel, QPixmap, QApplication

height = 300
width = 400

#building array
arr_i = np.zeros([height, width, 4], dtype=np.uint8)
arr_i[20:100, 40:200,0] = 255
arr_i[30:150, 80:250,1] = 255
arr_i[40:200, 120:300,2] = 255

#converting to QImage
q_img = QImage(arr_i.data, width, height, QImage.Format_RGB32)


#building app with IMG
app = QApplication([])
pix = QPixmap.fromImage(q_img)
lbl = QLabel()
lbl.setPixmap(pix)
lbl.show()

app.exec_()

