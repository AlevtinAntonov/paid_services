from PyQt6 import QtWidgets as qtw, QtSql

from controller.functions import get_value_with_default
from view.add_child_parent_dialog import Ui_Dialog_ChildParents


class ChildParentDialog(qtw.QDialog, Ui_Dialog_ChildParents):
    def __init__(self, selected_child_model=None):
        super().__init__()
        self.selected_child_model = selected_child_model
        self.setupUi(self)

        self.data_load_child_parents()


    def data_load_child_parents(self):
        self.label_ChildFullName.setText(get_value_with_default(self.selected_child_model, 1))
        self.label_ChildDateOfBirth.setText(get_value_with_default(self.selected_child_model, 2))
        self.label_ChildGenderName.setText(get_value_with_default(self.selected_child_model, 3))

        document_string = (f'Тип документа: {document_type}\n Серия: {document_serie} номер: {document_number}\n '
                           f'Выдан: {document_issued_by}\n Дата выдачи: {document_issued_date}')

        self.label_ChildDocumentData.setText(document_string)
