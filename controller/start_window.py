import logging

from PyQt6 import QtWidgets as qtw
from PyQt6.QtWidgets import QMessageBox

from controller.classes.form_frame_no_1 import Form_Frame_1
from controller.classes.form_tab_contracts import FormTabContracts
from controller.classes.new_contract_dialog import ContractDialog
from model.db_connect import DatabaseConnector
from view.main_window import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG)

class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contract_id = None
        self.invoice_id = None

        # Создаем экземпляр DatabaseConnector и подключаемся к базе данных
        self.db_connector = DatabaseConnector()
        if not self.db_connector.connect():
            return  # Если подключение не удалось, выходим из конструктора

        self.action_NewContract.triggered.connect(self.add_new_contract)

        # lazy loaded widgets
        self.form_frame_1 = None
        self.form_frame_2 = None
        self.form_tab_contracts = FormTabContracts()
        # Добавляем формы на вкладку 0
        self.add_widget_to_tab(self.form_tab_contracts, "tab_Contracts")

        # Сигналы для смены вкладок
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        # Проверяем, какая вкладка текущая
        if index == 1:  # Например, вкладка 1 для tab_Payment
            if self.form_frame_1 is None:
                self.form_frame_1 = Form_Frame_1()
                self.add_widget_to_tab(self.form_frame_1, "tab_Payment")
        elif index == 2:  # Вкладка 2 для tab_Lessons
            if self.form_frame_2 is None:
                self.form_frame_2 = Form_Frame_1()
                self.add_widget_to_tab(self.form_frame_2, "tab_Lessons")

    def add_widget_to_tab(self, widget, tab_name):
        tab_widget = self.tabWidget.findChild(qtw.QWidget, tab_name)
        if tab_widget:
            # Ensure that the tab has a layout
            if tab_widget.layout() is None:
                tab_widget.setLayout(qtw.QVBoxLayout(tab_widget))

            layout = tab_widget.layout()  # Get the current layout
            layout.addWidget(widget)  # Add the widget to the layout
            logging.debug(f"Виджет {widget} добавлен на вкладку {tab_name}.")
        else:
            logging.warning(f"Вкладка с именем {tab_name} не найдена.")

    def add_new_contract(self):
        contract_dialog = ContractDialog()
        if contract_dialog.exec() == qtw.QDialog.DialogCode.Accepted:
            logging.debug("Contract dialog accepted")
            try:
                contract_dialog.save_new_contract()
                self.form_tab_contracts.table_contracts_view()
            except Exception as e:
                logging.error(f"Error while saving contract: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить новый контракт: {str(e)}")
