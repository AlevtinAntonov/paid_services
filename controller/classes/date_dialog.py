from PyQt6 import QtWidgets as qtw

from view.date_input_dialog import Ui_DateInputDialog


class DateDialog(qtw.QDialog, Ui_DateInputDialog):
    def __init__(self, current_value):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_InputDate.setText(current_value)

        # self.show()

    def get_value(self):
        return self.lineEdit_InputDate.text()