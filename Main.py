import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.MainWindow import MainWindow
from test import Ui_MainWindow
from untitled import Ui_Form

class MW(QMainWindow, Ui_Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())