from PyQt6 import QtWidgets as qtw

from controller.functions import get_data_from_db, get_data_id_from_db
from view.invoice_input_dialog import Ui_InvoiceInputDialog


class InvoiceDialog(qtw.QDialog, Ui_InvoiceInputDialog):
    def __init__(self, contract_id):
        super().__init__()
        self.contract_id = contract_id
        self.setupUi(self)
        self.month_names = get_data_from_db('months')
        self.comboBox_InvoiceMonth.addItems(self.month_names)
        # self.show()


    def get_value(self):
        value = self.lineEdit_NumberOfLessons.text()  # Получаем текст из lineEdit
        try:
            number_of_lessons = int(value)  # Пробуем преобразовать в целое число
            return number_of_lessons  # Если успешно, возвращаем число
        except ValueError:
            return 0  # Если возникла ошибка, возвращаем 0

    def get_txt(self):
        return self.lineEdit_InvoiceRemarks.text() if self.lineEdit_InvoiceRemarks.text() else None  # Получаем, возвращаем текст из lineEdit

    def get_month_id(self):
        return get_data_id_from_db('months', self.comboBox_InvoiceMonth.currentText())