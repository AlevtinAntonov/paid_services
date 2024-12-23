from PyQt6 import QtWidgets as qtw

from view.delete_dialog import Ui_DeleteDialog


class DeleteDialog(qtw.QDialog, Ui_DeleteDialog):
    def __init__(self, label_text_one, label_data_one, label_text_two=None, label_data_two=None):
        super().__init__()
        self.setupUi(self)
        self.label_TextOne.setText(label_text_one)
        self.label_TextTwo.setText(label_text_two)
        self.label_DeleteDataOne.setText(label_data_one)
        self.label_DeleteDataTwo.setText(label_data_two)

        # self.show()
