import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtUiTools


'''

class DoLoadHTML(QObject):
    def __init__(self, parent = None):
        super(DoLoadHTML, self).__init__(parent)
        self.main_obj = parent

        data_init = ini_data()
        self.uni_url = data_init.get_url()

        self.l_stat = HandleLoadStatusLabel(self.main_obj)
        self.main_obj.window.HtmlReport.loadStarted.connect(
            self.l_stat.load_started
        )
        self.main_obj.window.HtmlReport.loadProgress.connect(
            self.l_stat.load_progress
        )
        self.main_obj.window.HtmlReport.loadFinished.connect(
            self.l_stat.load_finished
        )
        self.lst_html = []

        first_half = """<html>
            <head>
            <title>A Sample Page</title>
            </head>
            <body>
            <h3>"""

        second_half = """</h3>
            </body>
            </html>"""

        self.not_avail_html = first_half \
        + "There is no report available for this step." \
        + second_half

        self.loading_html = first_half \
        + "  Loading ..." \
        + second_half

        self.failed_html = first_half \
        + "  Failed Connection" \
        + second_half

    def __call__(self, do_request = False):
        print("Do Request =", do_request)
        if do_request:
            print("network load_html ... Start")
            nod_p_num = self.main_obj.curr_nod_num
            found_html = False
            for html_info in self.lst_html:
                if(
                    html_info["number"] == nod_p_num
                    and
                    len(html_info["html_report"]) > 5
                ):
                    found_html = True
                    full_file = html_info["html_report"]

            if not found_html:
                self.main_obj.window.HtmlReport.setHtml(self.loading_html)
                self.l_stat.load_started()
                try:
                    cmd = {
                        "nod_lst":[nod_p_num],
                        "cmd_lst":["get_report"]
                    }
                    req_gt = requests.get(self.uni_url, stream = True, params = cmd)
                    compresed = req_gt.content
                    full_file = zlib.decompress(compresed).decode('utf-8')

                    found_html = False
                    for html_info in self.lst_html:
                        if(
                            html_info["number"] == nod_p_num
                        ):
                            found_html = True
                            html_info["html_report"] = full_file

                    if not found_html:
                        self.lst_html.append(
                            {
                                "number"       :nod_p_num,
                                "html_report"   :full_file
                            }
                        )

                except ConnectionError:
                    print("\n ConnectionError (DoLoadHTML) \n")
                    full_file = ''

                except requests.exceptions.RequestException:
                    print("\n requests.exceptions.RequestException (DoLoadHTML) \n")
                    full_file = self.failed_html

                except zlib.error:
                    print("\n zlib.error (DoLoadHTML) \n")
                    full_file = self.not_avail_html

            if len(full_file) < 5:
                self.main_obj.window.HtmlReport.setHtml(self.not_avail_html)

            else:
                self.main_obj.window.HtmlReport.setHtml(full_file)

            print("network load_html ... End")

        else:
            self.main_obj.window.HtmlReport.setHtml(self.not_avail_html)

'''

class Form(QObject):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        self.window = QtUiTools.QUiLoader().load("simple.ui")

        self.num = 0

        #Next line is NOT doing what I wanted, to return data with connect
        self.data_test = self.window.Button1.clicked.connect(self.clicked)

        self.window.PrintDataButton.clicked.connect(self.imprime)
        self.window.show()

    def clicked(self):
        print("clicked")
        self.num += 1
        print("self.num =", self.num)
        return int(self.num)

    def imprime(self):
        print("self.data_test =", self.data_test)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

