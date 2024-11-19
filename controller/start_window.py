from PyQt6 import QtWidgets as qtw, QtGui

from view.main_window import Ui_MainWindow


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap("./img/File.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # self.action_2.setIcon(icon1)

