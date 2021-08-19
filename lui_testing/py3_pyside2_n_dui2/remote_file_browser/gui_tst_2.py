import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

'''
def iterate(currentDir, currentItem):
    l_dir = os.listdir(currentDir)
    for file_name in l_dir:
        path = os.path.join(currentDir, file_name)
        if os.path.isdir(path):
            dirItem = QTreeWidgetItem(currentItem)
            dirItem.setText(0, file_name)
            iterate(path, dirItem)
            print("file_name(dir) =", file_name)

        else:
            fileItem = QTreeWidgetItem(currentItem)
            fileItem.setText(0, file_name)
'''

def iterate(file_path):
    file_name = file_path.split("/")[-1]
    local_dict = {
        "file_name": file_name, "file_path": file_path, "list_child": []
    }
    debuging = '''
    print("\n", file_path)
    print("file_name =", file_name)
    '''
    if os.path.isdir(file_path):
        local_dict["isdir"] = True
        for new_file_name in os.listdir(file_path):
            new_file_path = os.path.join(file_path, new_file_name)
            local_dict["list_child"].append(
                iterate(new_file_path)
            )

    else:
        local_dict["isdir"] = False


    return local_dict

class MyTree(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTree, self).__init__(parent=parent)
        self.show()

    def fillTree(self):
        self.clear()
        #iterate(startDir, self)
        lst_dic = iterate(
            "/scratch/dui_prototyping/lui_testing/py3_pyside2_n_dui2"
        )
        print("lst_dic =", lst_dic)


class Client(QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.t_view = MyTree()
        mainLayout.addWidget(self.t_view)
        send2serverButton = QPushButton("Launch command")
        send2serverButton.clicked.connect(self.request_launch)
        mainLayout.addWidget(send2serverButton)
        self.setLayout(mainLayout)

    def request_launch(self):
        self.t_view.fillTree(

        )
        print("Launch \n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())
