from PyQt6 import QtWidgets as qtw

from view.main_window import Ui_MainWindow


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

