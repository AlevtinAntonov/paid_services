import logging

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from controller.classes.table_info_dict import table_info
from controller.date_dialog import DateDialog
from controller.fill_tables import fill_table_widget
from controller.functions import validate_and_convert_date, get_data, get_data_from_db, populate_combobox, \
    get_data_id_from_db, get_input_value, get_combobox_value
from model.db_connect import DatabaseConnector
from view.main_window import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG)


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contract_id = None

        # Создаем экземпляр DatabaseConnector и подключаемся к базе данных
        self.db_connector = DatabaseConnector()
        if not self.db_connector.connect():
            return  # Если подключение не удалось, выходим из конструктора

        self.setup_connections()
        self.table_contracts_view()
        self.setup_tbl_contracts_view()

    def setup_connections(self):
        self.lineEdit_FilterChild.textChanged.connect(self.filter_data)

        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)
        self.tableWidget_Contracts.itemSelectionChanged.connect(self.on_contract_selected)
        self.tableWidget_Contracts.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.tableWidget_Invoices.itemChanged.connect(self.on_item_changed_invoices)
        self.tableWidget_Invoices.itemSelectionChanged.connect(self.on_invoice_selected)

        self.tableWidget_VisitLog.itemChanged.connect(self.on_item_changed_visit_log)

        # Подключаем сигнал нажатия кнопки
        self.pushButton_SaveContactInfo.clicked.connect(self.save_selected_contract)
        self.pushButton_NewContract.clicked.connect(self.add_new_contract)
        self.pushButton_PrintContract.clicked.connect(self.print_selected_contract)
        self.pushButton_Close.clicked.connect(self.close)

    def on_item_changed(self, item):
        self.handle_item_changed(item, 'contracts')

    def on_item_changed_invoices(self, item):
        self.handle_item_changed(item, 'invoices', is_invoice=True)

    def on_item_changed_visit_log(self, item):
        self.handle_item_changed(item, 'visit_log', is_visit_log=True)

    def handle_item_changed(self, item, table, is_invoice=False, is_visit_log=False):
        row = item.row()
        column = item.column()
        new_value = item.text() if not item.checkState() == Qt.CheckState.Checked else item.checkState() == Qt.CheckState.Checked

        if is_invoice and column in [0, 1, 5, 6, 7, 8, 9]:
            new_value = item.text()
        elif is_invoice and column in [3, 4]:
            table = 'payments'
            new_value = int(new_value) if column == 3 else validate_and_convert_date(new_value) or None
        elif is_visit_log and column in [2, 3, 4, 5]:
            new_value = int(new_value)

        self.update_database(row, column, new_value, table)

    def update_database(self, row, column, new_value, tbl_name):
        try:
            print(f"{row=} {column=} {new_value=} {tbl_name=}")  # Отладочная информация

            table_info_selected = table_info.get(tbl_name)
            if not table_info_selected:
                logging.error(f"Unknown table name: {tbl_name}")
                return

            column_id = table_info_selected['column_id']
            value_id = self.get_value_id(tbl_name, row, table_info_selected['value_id_index'])
            column_map = table_info_selected['column_map']

            # Специальная обработка для таблицы payments
            if tbl_name == 'payments':
                logging.debug(f'if tbl_name == payments')
                return self.update_payment(row, column, new_value, value_id, table_info_selected)

            column_name = column_map.get(column)
            if column_name is None:
                logging.error(f"Invalid column index: {column}")
                return

            self.execute_update_query(tbl_name, column_name, new_value, column_id, value_id)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")

    def get_value_id(self, tbl_name, row, value_id_index):
        """ Получить идентификатор записи в зависимости от типа таблицы. """
        if tbl_name == 'contracts':
            return self.contracts_model.data(self.contracts_model.index(row, value_id_index))
        elif tbl_name == 'visit_log':
            return self.visit_log_model.data(self.visit_log_model.index(row, value_id_index))
        elif tbl_name in ['invoices', 'payments']:
            return self.invoices_model.data(self.invoices_model.index(row, value_id_index))
        return None

    def update_payment(self, row, column, new_value, value_id, table_info_selected):
        """ Обновить данные в таблице payments. """
        invoice_id = self.invoices_model.data(self.invoices_model.index(row, table_info_selected['invoice_id_index']))
        column_name = table_info_selected['column_map'].get(column)

        # Проверяем, существует ли value_id в таблице payments
        query = QtSql.QSqlQuery()
        query.prepare(f"SELECT COUNT(*) FROM payments WHERE {table_info_selected['column_id']} = :id")
        query.bindValue(":id", value_id)
        query.exec()
        query.next()
        exists = query.value(0) > 0

        if not exists:
            # Если записи не существует, добавляем новую строку
            insert_query = QtSql.QSqlQuery()
            insert_query.prepare(
                f"INSERT INTO payments (invoice_id, {table_info_selected['column_map'][column]}) VALUES (:invoice_id, :col_data)"
            )
            insert_query.bindValue(":invoice_id", invoice_id)
            insert_query.bindValue(":col_data", new_value)

            if not insert_query.exec():
                logging.error(f"Failed to insert new record: {insert_query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка",
                                     "Не удалось добавить новую запись:\n" + insert_query.lastError().text())
                return False

            logging.debug("Record inserted successfully.")
            return True  # Выходим после добавления новой записи

            # Если запись существует, обновляем ее
        return self.execute_update_query('payments', column_name, new_value, table_info_selected['column_id'], value_id)

    def execute_update_query(self, tbl_name, column_name, new_value, column_id, value_id):
        """ Выполнить обновление записи в таблице. """
        query = QtSql.QSqlQuery()
        query.prepare(f"UPDATE {tbl_name} SET {column_name} = :value WHERE {column_id} = :id")

        print(f"Executing: UPDATE {tbl_name} SET {column_name} = :value WHERE {column_id} = :id")

        if new_value in [None, ""]:
            query.bindValue(":value", None)  # Устанавливаем NULL в запрос
        else:
            query.bindValue(":value", new_value)

        query.bindValue(":id", value_id)

        if not query.exec():
            logging.error(f"Failed to update record: {query.lastError().text()}")
            QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
            return False

        logging.debug("Record updated successfully.")

        # Зависит от типа таблицы, можно вызывать разные методы для обновления интерфейса
        if tbl_name == 'contracts':
            self.table_contracts_view()
        elif tbl_name == 'invoices':
            self.table_invoices_view(self.contract_id)

        return True

    def setup_table_view(self, table_widget, column_widths, headers):
        table_widget.setColumnHidden(0, True)  # Скрываем ID
        for index, width in enumerate(column_widths):
            table_widget.setColumnWidth(index + 1, width)  # Учитываем, что ID находится на нулевом индексе
        table_widget.setHorizontalHeaderLabels(headers)

    def setup_tbl_contracts_view(self):
        column_widths = [50, 80, 250, 150, 110, 170, 50, 80, 50, 50]
        headers = ['ID', 'Номер', 'Дата', 'Ребенок', 'Кружок', 'Группа',
                   'Примечание', 'Дог.\nподп.', 'Дата\nрасторж.',
                   'Согл.\nподп.', 'Без\nоплат']
        self.setup_table_view(self.tableWidget_Contracts, column_widths, headers)

    def setup_tbl_invoices_view(self):
        column_widths = [100, 80, 80, 100, 100, 80, 200]
        headers = ['ID', 'Месяц', 'К\nоплате', 'Оплачено', 'Дата\nоплаты', 'Остаток',
                   'Занятий\nв месяц', 'Примечания']
        self.setup_table_view(self.tableWidget_Invoices, column_widths, headers)

    def setup_tbl_visit_log_view(self):
        column_widths = [100, 80, 80, 80, 80, 80]
        headers = ['ID', 'Месяц', 'Факт\nзанятий', 'Пропуск\nсправка',
                   'Пропуск\nкарантин', 'Пропуск\nдругое', 'Примечания']
        self.setup_table_view(self.tableWidget_VisitLog, column_widths, headers)

    def on_cell_double_clicked(self, row, column):
        if column in [8, ]:  # Проверяем, что это 8 колонка
            current_value = self.tableWidget_Contracts.item(row, column).text()  # Получаем текущее значение ячейки
            dialog = DateDialog(current_value)  # Создаем диалог с текущим значением
            if dialog.exec() == qtw.QDialog.DialogCode.Accepted:  # Проверяем, нажал ли пользователь "ОК"
                new_value = dialog.get_value()  # Получаем новое значение из диалога
                if new_value not in [None, '']:
                    new_value = validate_and_convert_date(new_value)
                if "Неверный формат даты" in new_value or "Неверная дата" in new_value or new_value in ["", None]:
                    new_value = None
                self.tableWidget_Contracts.item(row, column).setText(new_value)
                self.update_database(row, column, new_value, 'contracts')

    def table_contracts_view(self):
        self.tableWidget_Contracts.itemChanged.disconnect(self.on_item_changed)
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.contracts_model.select()
        print('table_contracts_view -> before fill_table_widget')
        fill_table_widget(self.contracts_model, self.tableWidget_Contracts, [1, 2, 3, 4, 5, 8])
        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)

    def setup_tables_views(self, model, table_widget, filter_condition=None, filter_value=None, columns=None, slot=None):
        table_widget.itemChanged.disconnect()  # Отключаем сигнал изменения
        model.select()  # Выполняем выборку

        if filter_condition and filter_value is not None:
            model.setFilter(f"{filter_condition} = {filter_value}")
            model.select()  # Выполняем выборку с фильтром

        # Проверка на ошибки после выполнения запроса
        if model.lastError().isValid():
            print("Ошибка запроса:", model.lastError().text())
            return

        fill_table_widget(model, table_widget, columns)

        if slot:  # Если слот указан, подключаем его
            table_widget.itemChanged.connect(slot)

    def table_contracts_view(self):
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.setup_tables_views(self.contracts_model, self.tableWidget_Contracts, columns=[1, 2, 3, 4, 5, 8],
                              slot=self.on_item_changed)

    def table_invoices_view(self, contract_id):
        self.invoices_model = QtSql.QSqlTableModel(self)
        self.invoices_model.setTable('invoices_view')
        self.setup_tables_views(self.invoices_model, self.tableWidget_Invoices, 'contract_id', contract_id, [2],
                              slot=self.on_item_changed_invoices)

    def table_visit_log_view(self, contract_id):
        self.visit_log_model = QtSql.QSqlTableModel(self)
        self.visit_log_model.setTable('visit_log_view')
        print(f'table_visit_log_view for contract_id = {contract_id}')
        self.setup_tables_views(self.visit_log_model, self.tableWidget_VisitLog, 'contract_id', contract_id, [1],
                              slot=self.on_item_changed_visit_log)

    def filter_data(self):
        """ Фильтрация данных в таблице на основе ввода пользователя. """
        try:
            self.tableWidget_Contracts.itemChanged.disconnect(self.on_item_changed)
            # Получаем текст фильтра из строки ввода
            filter_text = self.lineEdit_FilterChild.text().strip()

            # Проверяем наличие текста для фильтрации
            if filter_text:
                # Формируем условие фильтрации
                query = f"SELECT * FROM contracts_view WHERE child_fio ILIKE '%{filter_text}%'"
                self.contracts_model.setQuery(query)
                if self.contracts_model.lastError().isValid():
                    print("Ошибка выполнения запроса:", self.contracts_model.lastError().text())
            else:
                # Если фильтр пустой, сбрасываем фильтрацию
                self.contracts_model.setQuery("SELECT * FROM contracts_view")

            # Обновляем таблицу
            fill_table_widget(self.contracts_model, self.tableWidget_Contracts,
                              [1, 2, 3, 4, 5, 8])  # Заполняем таблицу заново
            self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)
        except Exception as e:
            logging.error("Ошибка фильтрации: %s", str(e))
            qtw.QMessageBox.critical(self, "Ошибка", str(e))

    def get_selected_id(self, table_widget, model, column):
        """ Получает ID из выбранной строки таблицы. """
        selected_indexes = table_widget.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            return model.data(model.index(row, column))
        return None

    def on_contract_selected(self):
        self.contract_id = self.get_selected_id(self.tableWidget_Contracts, self.contracts_model, 0)
        if self.contract_id is not None:
            print(f'on_contract_selected {self.contract_id=}')
            self.load_selected_contract(self.contract_id)
            self.table_invoices_view(self.contract_id)
            self.setup_tbl_invoices_view()
            self.table_visit_log_view(self.contract_id)
            self.setup_tbl_visit_log_view()

    def on_invoice_selected(self):
        self.invoice_id = self.get_selected_id(self.tableWidget_Invoices, self.invoices_model, 8)
        if self.invoice_id is not None:
            print(f'on_invoice_selected {self.invoice_id=}')


    def load_selected_contract(self, contract_id):
        """ Загружает данные выбранного контракта и обновляет соответствующие поля. """
        # Получаем данные из базы
        parents_fio = get_data_from_db('parents')
        child_fio = get_data_from_db('children')
        lesson_names = get_data_from_db('lessons')

        # Инициализация модели для выбранного контракта
        self.selected_contract_model = QtSql.QSqlTableModel(self)
        self.selected_contract_model.setTable('contracts_data')
        self.selected_contract_model.setFilter(f"contract_id = {contract_id}")
        self.selected_contract_model.select()

        # Проверка на ошибки после выполнения запроса
        if self.selected_contract_model.lastError().isValid():
            logging.debug(f"Ошибка запроса: {self.selected_contract_model.lastError().text()}")
            return

        # Обновление данных
        if self.selected_contract_model.rowCount() > 0:
            logging.debug(f'{self.selected_contract_model.rowCount()=}')
            self.lineEdit_ContractNumber.setText(get_data(self.selected_contract_model, 1))
            self.lineEdit_ContractDate.setText(get_data(self.selected_contract_model, 2))
            self.lineEdit_ContractDateStart.setText(get_data(self.selected_contract_model, 3))
            self.lineEdit_ContractDateEnd.setText(get_data(self.selected_contract_model, 4))

            populate_combobox(self.selected_contract_model, self.comboBox_ContractApplicant, parents_fio, 5)
            populate_combobox(self.selected_contract_model, self.comboBox_ContractChild, child_fio, 6)
            populate_combobox(self.selected_contract_model, self.comboBox_ContractLessons, lesson_names, 7)

            self.lineEdit_ContractRemaks.setText(get_data(self.selected_contract_model, 8))
        else:
            print(f"Нет данных для contract_id: {contract_id}.")
        print(f'1 load_selected_contract {contract_id=}')

    def save_selected_contract(self):
        """ Сохраняет данные выбранного контракта в базу данных. """
        print(f'save_selected_contract {self.contract_id=}')

        # Получение введенных данных
        contract_number = get_input_value(self.lineEdit_ContractNumber)
        contract_date = validate_and_convert_date(get_input_value(self.lineEdit_ContractDate))
        contract_start_date = validate_and_convert_date(get_input_value(self.lineEdit_ContractDateStart))
        contract_end_date = validate_and_convert_date(get_input_value(self.lineEdit_ContractDateEnd))

        parents_fio = get_combobox_value(self.comboBox_ContractApplicant)
        child_fio = get_combobox_value(self.comboBox_ContractChild)
        lesson_name = get_combobox_value(self.comboBox_ContractLessons)
        remarks = get_input_value(self.lineEdit_ContractRemaks)

        print(contract_number, contract_date, contract_start_date, contract_end_date, parents_fio, child_fio,
              lesson_name, remarks)

        # Получение ID из базы
        applicant_id = get_data_id_from_db('parents', parents_fio)
        child_id = get_data_id_from_db('children', child_fio)
        lesson_id = get_data_id_from_db('lessons', lesson_name)
        print(applicant_id, child_id, lesson_id)

        # Логика для сохранения данных в базу данных
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE contracts SET contract_number = :c_number, contract_date = :c_date, "
                          "contract_start_date = :c_start_date, contract_end_date = :c_end_date, "
                          "parent_id = :applicant_id, child_id = :child_id, lesson_id = :lesson_id, "
                          "remarks = :remarks WHERE contract_id = :id;")

            # Привязка значений
            query.bindValue(":c_number", contract_number)
            query.bindValue(":c_date", contract_date)
            query.bindValue(":c_start_date", contract_start_date)
            query.bindValue(":c_end_date", contract_end_date)
            query.bindValue(":applicant_id", applicant_id)
            query.bindValue(":child_id", child_id)
            query.bindValue(":lesson_id", lesson_id)
            query.bindValue(":remarks", remarks)
            query.bindValue(":id", self.contract_id)

            # Выполнение запроса и обработка результата
            if not query.exec():
                logging.error(f"Failed to update record: {query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                return False
            else:
                logging.debug("Record updated successfully.")
                # Обновляем таблицу и загружаем данные для выбранного контракта
                self.table_contracts_view()
                self.load_selected_contract(self.contract_id)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")

    def add_new_contract(self):
        print(f'add_new_contract pressed {self.contract_id=}')

    def print_selected_contract(self):
        print(f'print_selected_contract pressed {self.contract_id=}')
