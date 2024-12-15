from PyQt6 import QtWidgets as qtw

from view.delete_invoice_dialog import Ui_DeleteInvoiceDialog


class DeleteInvoiceDialog(qtw.QDialog, Ui_DeleteInvoiceDialog):
    def __init__(self, invoice_month, invoice_sum):
        super().__init__()
        self.setupUi(self)
        self.label_DeleteMonthName.setText(invoice_month)
        self.label_DeleteInvoiceSum.setText(invoice_sum)

        # self.show()
