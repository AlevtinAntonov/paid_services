import logging

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from controller.date_dialog import DateDialog
from controller.functions import validate_and_convert_date, get_data, get_data_from_db, populate_combobox, \
    get_data_id_from_db
from model.db_connect import DatabaseConnector
from view.main_window import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG)

def fill_table_widget(model, table_widget, non_editable_columns):
    """Обновляет содержимое QTableWidget на основе данных модели."""
    table_widget.setRowCount(0)  # Очищаем существующие данные
    table_widget.setColumnCount(model.columnCount())  # Устанавливаем количество столбцов
    table_widget.verticalHeader().setVisible(False)  # Отключаем отображение номеров строк

    # Заполнение QTableWidget данными из модели
    for row in range(model.rowCount()):
        table_widget.insertRow(row)  # Вставляем новую строку
        for column in range(model.columnCount()):
            item_data = model.data(model.index(row, column))
            item = qtw.QTableWidgetItem()

            # Если колонка не редактируемая
            if column in non_editable_columns:
                item.setText(str(item_data))  # Для других значений
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Убираем флаг редактирования
            else:
                if isinstance(item_data, bool):  # Если это логическое значение
                    item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable |
                                  Qt.ItemFlag.ItemIsSelectable)
                else:
                    item.setText(str(item_data))  # Для остальных значений
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable |
                                  ~Qt.ItemFlag.ItemIsUserCheckable)

            table_widget.setItem(row, column, item)


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contract_id = None



        # Создаем экземпляр DatabaseConnector и подключаемся к базе данных
        self.db_connector = DatabaseConnector()
        if not self.db_connector.connect():
            return  # Если подключение не удалось, выходим из конструктора
        self.lineEdit_FilterChild.textChanged.connect(self.filter_data)

        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)
        self.tableWidget_Contracts.itemSelectionChanged.connect(self.on_contract_selected)
        self.tableWidget_Contracts.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.tableWidget_Invoices.itemChanged.connect(self.on_item_changed_invoices)
        self.tableWidget_Invoices.itemSelectionChanged.connect(self.on_invoice_selected)

        self.tableWidget_VisitLog.itemChanged.connect(self.on_item_changed_visit_log)

        # Подключаем сигнал нажатия кнопки к функции load_selected_contract
        self.pushButton_SaveContactInfo.clicked.connect(self.save_selected_contract)
        self.pushButton_NewContract.clicked.connect(self.add_new_contract)
        self.pushButton_PrintContract.clicked.connect(self.print_selected_contract)
        self.pushButton_Close.clicked.connect(self.close)
        self.table_contracts_view()
        self.setup_tbl_contracts_view()

    def on_item_changed(self, item):
        row = item.row()
        column = item.column()

        if column in [7, 9, 10]:  # для checkbox колонок
            new_state = item.checkState() == Qt.CheckState.Checked
            self.update_database(row, column, new_state, 'contracts')
        else:  # для текстовых ячеек
            new_value = item.text()  # получаем новое текстовое значение
            self.update_database(row, column, new_value, 'contracts')

    def on_item_changed_invoices(self, item):
        row = item.row()
        column = item.column()
        if column in [0, 1, 5, 6, 7, 8,9]:
            new_value = item.text()  # получаем новое текстовое значение
            self.update_database(row, column, new_value, 'invoices')
        elif column in [3, 4]:
            if column == 3:
                new_value = int(item.text())  # получаем цифровое значение
            else:
                new_value = validate_and_convert_date(item.text()) if item.text() not in [None, ""] else None
            self.update_database(row, column, new_value, 'payments')

    def on_item_changed_visit_log(self, item):
        row = item.row()
        column = item.column()
        if column in [2, 3, 4, 5]:
            new_value = int(item.text())  # получаем цифровое значение
        else:
            new_value = item.text() # получаем новое текстовое значение
        self.update_database(row, column, new_value, 'visit_log')

    def update_database(self, row, column, new_value, tbl_name):
        try:
            print(f"{row=} {column=} {new_value=} {tbl_name=}") # отладочная инфо
            if tbl_name == 'contracts':
                column_id = 'contract_id'
                value_id = self.contracts_model.data(self.contracts_model.index(row, 0))
                column_map = {
                    1: "contract_number",
                    2: "contract_date",
                    4: "lesson_name",
                    5: "team_name",
                    6: "remarks",
                    7: "signed",
                    8: "cancel_date",
                    9: "cancel_agreement_signed",
                    10: "without_payment"
                }
            elif tbl_name == 'visit_log':
                column_id = 'invoice_id'
                value_id = self.visit_log_model.data(self.visit_log_model.index(row, 0))
                column_map = {
                    2: "lessons_fact",
                    3: "lessons_illness",
                    4: "lessons_quarantine",
                    5: "lessons_other_reasons",
                    6: "visit_log_remarks",
                }
            elif tbl_name == 'invoices':
                column_id = 'invoice_id'
                value_id = self.invoices_model.data(self.invoices_model.index(row, 8))
                column_map = {
                    1: "month_name",
                    5: "rest_of_money",
                    6: "lessons_per_month",
                    7: "remarks",
                }
            elif tbl_name == 'payments':
                column_id = 'payment_id'
                value_id = self.invoices_model.data(self.invoices_model.index(row, 9))
                invoice_id = self.invoices_model.data(self.invoices_model.index(row, 8))
                col_name = 'sum_paid'
                if column == 4:
                    col_name = 'payment_date'
                    print(f"{new_value=}")

                    print(new_value)
                column_map = {
                    3: "sum_paid",
                    4: "payment_date",
                }
                # Проверяем, существует ли value_id в таблице payments
                check_query = QtSql.QSqlQuery()
                check_query.prepare(f"SELECT COUNT(*) FROM payments WHERE {column_id} = :id;")
                check_query.bindValue(":id", value_id)
                check_query.exec()
                check_query.next()
                exists = check_query.value(0) > 0  # Проверяем, если запись существует

                if not exists:
                    # Если записи не существует, добавляем новую строку
                    insert_query = QtSql.QSqlQuery()
                    insert_query.prepare(
                        f"INSERT INTO payments (invoice_id, {col_name}) VALUES (:invoice_id, :col_data);")
                    insert_query.bindValue(":invoice_id", invoice_id)
                    insert_query.bindValue(":col_data", new_value)

                    if not insert_query.exec():
                        logging.error(f"Failed to insert new record: {insert_query.lastError().text()}")
                        QMessageBox.critical(None, "Ошибка",
                                             "Не удалось добавить новую запись:\n" + insert_query.lastError().text())
                        return False
                    else:
                        logging.debug("Record inserted successfully.")
                        return True  # Выходим после добавления новой записи
            else:
                return

            column_name = column_map.get(column)
            if column_name is None:
                logging.error(f"Invalid column index: {column}")
                return  # Не продолжаем, если индекс невалидный

            query = QtSql.QSqlQuery()
            query.prepare(f"UPDATE {tbl_name} SET {column_name} = :value WHERE {column_id} = :id;")
            print(f"UPDATE {tbl_name} SET {column_name} = :value WHERE {column_id} = :id; {new_value=} {value_id=}")
            if new_value in [None, ""]:
                query.bindValue(":value", None)  # Устанавливаем NULL в запрос
            else:
                query.bindValue(":value", new_value)
            query.bindValue(":id", value_id)

            if not query.exec():
                logging.error(f"Failed to update record: {query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                return False
            else:
                logging.debug("Record updated successfully.")
                # self.table_contracts_view()
                self.table_invoices_view(self.contract_id)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")
        # finally:


    def setup_tbl_contracts_view(self):
        self.tableWidget_Contracts.setColumnHidden(0, True)  # Скрываем ID
        self.tableWidget_Contracts.setColumnWidth(1, 50)
        self.tableWidget_Contracts.setColumnWidth(2, 80)
        self.tableWidget_Contracts.setColumnWidth(3, 250)
        self.tableWidget_Contracts.setColumnWidth(4, 150)
        self.tableWidget_Contracts.setColumnWidth(5, 110)
        self.tableWidget_Contracts.setColumnWidth(6, 170)
        self.tableWidget_Contracts.setColumnWidth(7, 50)
        self.tableWidget_Contracts.setColumnWidth(8, 80)
        self.tableWidget_Contracts.setColumnWidth(9, 50)
        self.tableWidget_Contracts.setColumnWidth(10, 50)

        self.tableWidget_Contracts.setHorizontalHeaderLabels(['ID', 'Номер', 'Дата', 'Ребенок', 'Кружок', 'Группа',
                                                              'Примечание', 'Дог.\nподп.', 'Дата\nрасторж.',
                                                              'Согл.\nподп.', 'Без\nоплат'])

    def setup_tbl_invoices_view(self):
        self.tableWidget_Invoices.setColumnHidden(0, True)  # Скрываем ID
        self.tableWidget_Invoices.setColumnWidth(1, 100)
        self.tableWidget_Invoices.setColumnWidth(2, 80)
        self.tableWidget_Invoices.setColumnWidth(3, 80)
        self.tableWidget_Invoices.setColumnWidth(4, 100)
        self.tableWidget_Invoices.setColumnWidth(5, 100)
        self.tableWidget_Invoices.setColumnWidth(6, 80)
        self.tableWidget_Invoices.setColumnWidth(7, 200)

        self.tableWidget_Invoices.setHorizontalHeaderLabels(['ID', 'Месяц', 'К\nоплате', 'Оплачено', 'Дата\nоплаты', 'Остаток',
                                                              'Занятий\nв месяц', 'Примечания'])

    def setup_tbl_visit_log_view(self):
        self.tableWidget_VisitLog.setColumnHidden(0, True)  # Скрываем ID
        self.tableWidget_VisitLog.setColumnWidth(1, 100)
        self.tableWidget_VisitLog.setColumnWidth(2, 80)
        self.tableWidget_VisitLog.setColumnWidth(3, 80)
        self.tableWidget_VisitLog.setColumnWidth(4, 80)
        self.tableWidget_VisitLog.setColumnWidth(5, 80)
        self.tableWidget_VisitLog.setColumnWidth(6, 80)

        self.tableWidget_VisitLog.setHorizontalHeaderLabels(['ID', 'Месяц', 'Факт\nзанятий', 'Пропуск\nсправка',
                                                             'Пропуск\nкарантин', 'Пропуск\nдругое', 'Примечания'])

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

    def table_invoices_view(self, contract_id):
        self.tableWidget_Invoices.itemChanged.disconnect(self.on_item_changed_invoices)
        self.invoices_model = QtSql.QSqlTableModel(self)
        self.invoices_model.setTable('invoices_view')
        self.invoices_model.select()

        # Установка фильтра по contract_id
        self.invoices_model.setFilter(f"contract_id = {contract_id}")
        self.invoices_model.select()  # Это загрузит данные согласно фильтру

        # Проверка на ошибки после выполнения запроса
        if self.invoices_model.lastError().isValid():
            print("Ошибка запроса:", self.invoices_model.lastError().text())
            return

        fill_table_widget(self.invoices_model, self.tableWidget_Invoices, [2])
        self.tableWidget_Invoices.itemChanged.connect(self.on_item_changed_invoices)

    def table_visit_log_view(self, contract_id):
        self.tableWidget_VisitLog.itemChanged.disconnect(self.on_item_changed_visit_log)
        print('table_visit_log_view')
        self.visit_log_model = QtSql.QSqlTableModel(self)
        self.visit_log_model.setTable('visit_log_view')
        self.visit_log_model.select()
        print(f"contract_id = {contract_id}")
        # Установка фильтра по contract_id
        # self.visit_log_model.setFilter(f"invoice_id = {invoice_id}")
        self.visit_log_model.setFilter(f"contract_id = {contract_id}")
        self.visit_log_model.select()  # Это загрузит данные согласно фильтру

        # Проверка на ошибки после выполнения запроса
        if self.visit_log_model.lastError().isValid():
            print("Ошибка запроса:", self.visit_log_model.lastError().text())
            return

        fill_table_widget(self.visit_log_model, self.tableWidget_VisitLog, [1])
        self.tableWidget_VisitLog.itemChanged.connect(self.on_item_changed_visit_log)

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

    def on_contract_selected(self):

        # Получаем выбранные индексы
        selected_indexes = self.tableWidget_Contracts.selectedIndexes()
        if selected_indexes:
            # Получаем строку из первого выбранного индекса
            row = selected_indexes[0].row()
            # ID договора находится в 0 столбце
            self.contract_id = self.contracts_model.data(self.contracts_model.index(row, 0))
            print(f'on_contract_selected {self.contract_id=}')
            self.load_selected_contract(self.contract_id)
            self.table_invoices_view(self.contract_id)
            self.setup_tbl_invoices_view()
            self.table_visit_log_view(self.contract_id)
            self.setup_tbl_visit_log_view()

    def on_invoice_selected(self):
        print('on_invoice_selected')
        selected_indexes = self.tableWidget_Invoices.selectedIndexes()
        if selected_indexes:
            # Получаем строку из первого выбранного индекса
            row = selected_indexes[0].row()
            # ID инвойса находится в 8 столбце
            self.invoice_id = self.invoices_model.data(self.invoices_model.index(row, 8))
            print(f'on_invoice_selected {self.invoice_id=}')
            # self.table_visit_log_view(self.invoice_id)
            # self.setup_tbl_visit_log_view()

    def load_selected_contract(self, contract_id):
        # Получаем список ФИО родителей
        parents_fio = get_data_from_db('parents')
        child_fio = get_data_from_db('children')
        lesson_names = get_data_from_db('lessons')

        # Инициализация модели для выбранного контракта
        self.selected_contract_model = QtSql.QSqlTableModel(self)
        self.selected_contract_model.setTable('contracts_data')

        # Установка фильтра по contract_id
        self.selected_contract_model.setFilter(f"contract_id = {contract_id}")
        self.selected_contract_model.select()  # Это загрузит данные согласно фильтру

        # Проверка на ошибки после выполнения запроса
        if self.selected_contract_model.lastError().isValid():
            print("Ошибка запроса:", self.selected_contract_model.lastError().text())
            return

        # Обновление данных
        if self.selected_contract_model.rowCount() > 0:
            logging.debug(f'{self.selected_contract_model.rowCount()=}')

            self.lineEdit_ContractNumber.setText(get_data(self.selected_contract_model, 1))
            self.lineEdit_ContractDate.setText(get_data(self.selected_contract_model, 2))  # Получение даты
            self.lineEdit_ContractDateStart.setText(get_data(self.selected_contract_model, 3))  # Начало договора
            self.lineEdit_ContractDateEnd.setText(get_data(self.selected_contract_model, 4))  # Конец договора
            populate_combobox(self.selected_contract_model, self.comboBox_ContractApplicant, parents_fio, 5)
            populate_combobox(self.selected_contract_model, self.comboBox_ContractChild, child_fio, 6)
            populate_combobox(self.selected_contract_model, self.comboBox_ContractLessons, lesson_names, 7)
            self.lineEdit_ContractRemaks.setText(get_data(self.selected_contract_model, 8))  # Примечания

        else:
            print(f"Нет данных для contract_id: {contract_id}.")
        print(f'1 load_selected_contract {contract_id=}')

    def save_selected_contract(self):

        print(f'save_selected_contract {self.contract_id=}')

        # Получение введенных данных
        contract_number = self.lineEdit_ContractNumber.text() if self.lineEdit_ContractNumber.text() not in [None,
                                                                                                             ""] else None
        contract_date = validate_and_convert_date(self.lineEdit_ContractDate.text()) if self.lineEdit_ContractDate.text() not in [None,
                                                                                                       ""] else None
        contract_start_date = validate_and_convert_date(self.lineEdit_ContractDateStart.text()) if self.lineEdit_ContractDateStart.text() not in [
            None, ""] else None
        contract_end_date = validate_and_convert_date(self.lineEdit_ContractDateEnd.text()) if self.lineEdit_ContractDateEnd.text() not in [None,
                                                                                                                 ""] else None
        parents_fio = self.comboBox_ContractApplicant.currentText() if self.comboBox_ContractApplicant.currentText() not in [
            None, ""] else None
        child_fio = self.comboBox_ContractChild.currentText() if self.comboBox_ContractChild.currentText() not in [None,
                                                                                                                   ""] else None
        lesson_name = self.comboBox_ContractLessons.currentText() if self.comboBox_ContractLessons.currentText() not in [
            None, ""] else None
        remarks = self.lineEdit_ContractRemaks.text() if self.lineEdit_ContractRemaks.text() not in [None, ""] else None

        print(contract_number, contract_date, contract_start_date, contract_end_date, parents_fio, child_fio,
              lesson_name, remarks)

        applicant_id = get_data_id_from_db('parents', parents_fio)
        child_id = get_data_id_from_db('children', child_fio)
        lesson_id = get_data_id_from_db('lessons', lesson_name)
        print(applicant_id, child_id, lesson_id)
        # Логика для сохранения данных в базу данных
        try:
            query = QtSql.QSqlQuery()
            query.prepare(f"UPDATE contracts SET contract_number = :c_number, contract_date = :c_date, "
                          f"contract_start_date = :c_start_date, contract_end_date = :c_end_date, "
                          f"parent_id = :applicant_id, child_id = :child_id, lesson_id = :lesson_id,"
                          f"remarks = :remarks WHERE contract_id = :id;")
            query.bindValue(":c_number", contract_number)
            query.bindValue(":c_date", contract_date)
            query.bindValue(":c_start_date", contract_start_date)
            query.bindValue(":c_end_date", contract_end_date)
            query.bindValue(":applicant_id", applicant_id)
            query.bindValue(":child_id", child_id)
            query.bindValue(":lesson_id", lesson_id)
            query.bindValue(":remarks", remarks)
            query.bindValue(":id", self.contract_id)

            if not query.exec():
                logging.error(f"Failed to update record: {query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                return False
            else:
                logging.debug("Record updated successfully.")
                # Обновляем таблицу
                self.table_contracts_view()  # Теперь вызываем метод обновления таблицы
                self.load_selected_contract(self.contract_id)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")


    def add_new_contract(self):
        print(f'add_new_contract pressed {self.contract_id=}')

    def print_selected_contract(self):
        print(f'print_selected_contract pressed {self.contract_id=}')
