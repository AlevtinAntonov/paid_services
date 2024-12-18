from PyQt6 import QtWidgets as qtw

from view.form_1 import Ui_Form_Frame_1


class Form_Frame_1(qtw.QWidget, Ui_Form_Frame_1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.show()

    # def get_value(self):
    #     return self.lineEdit_InputDate.text()