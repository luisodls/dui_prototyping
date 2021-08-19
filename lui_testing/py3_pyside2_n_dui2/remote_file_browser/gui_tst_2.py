import sys, os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

def iter_dict(file_path):
    file_name = file_path.split("/")[-1]
    local_dict = {
        "file_name": file_name, "file_path": file_path, "list_child": []
    }
    if os.path.isdir(file_path):
        local_dict["isdir"] = True
        for new_file_name in os.listdir(file_path):
            new_file_path = os.path.join(file_path, new_file_name)
            local_dict["list_child"].append(
                iter_dict(new_file_path)
            )

    else:
        local_dict["isdir"] = False

    return local_dict


def iter_gui(list_dict, currentItem):
    for child in list_dict["list_child"]:
        if list_dict["isdir"]:
            dirItem = QTreeWidgetItem(currentItem)
            dirItem.setText(0, child["file_name"])
            iter_gui(child, dirItem)

        else:
            fileItem = QTreeWidgetItem(currentItem)
            fileItem.setText(0, child["file_name"])


class MyTree(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTree, self).__init__(parent=parent)
        self.show()

    def fillTree(self):
        self.clear()
        lst_dic = iter_dict(
            "/scratch/dui_prototyping"
        )
        iter_gui(lst_dic, self)


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
