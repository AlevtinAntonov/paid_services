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


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contract_id = None

        self.lineEdit_FilterChild.textChanged.connect(self.filter_data)

        # Создаем экземпляр DatabaseConnector и подключаемся к базе данных
        self.db_connector = DatabaseConnector()
        if not self.db_connector.connect():
            return  # Если подключение не удалось, выходим из конструктора

        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)
        self.tableWidget_Contracts.itemSelectionChanged.connect(self.on_contract_selected)
        self.tableWidget_Contracts.cellDoubleClicked.connect(self.on_cell_double_clicked)

        # Подключаем сигнал нажатия кнопки к функции load_selected_contract
        self.pushButton_SaveContactInfo.clicked.connect(self.save_selected_contract)
        self.table_contracts_view()
        self.setup_tbl_contracts_view()

    def on_item_changed(self, item):
        row = item.row()
        column = item.column()

        if column in [7, 9, 10]:  # для checkbox колонок
            new_state = item.checkState() == Qt.CheckState.Checked
            self.update_database(row, column, new_state)
        else:  # для текстовых ячеек
            new_value = item.text()  # получаем новое текстовое значение
            self.update_database(row, column, new_value)


    def update_database(self, row, column, new_value):
        try:
            contract_id = self.contracts_model.data(self.contracts_model.index(row, 0))

            column_map = {
                0: "contract_id",
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

            column_name = column_map.get(column)
            if column_name is None:
                logging.error(f"Invalid column index: {column}")
                return  # Не продолжаем, если индекс невалидный

            query = QtSql.QSqlQuery()
            query.prepare(f"UPDATE contracts SET {column_name} = :value WHERE contract_id = :id;")
            if new_value in [None, ""]:
                query.bindValue(":value", None)  # Устанавливаем NULL в запрос
            else:
                query.bindValue(":value", new_value)
            query.bindValue(":id", contract_id)

            if not query.exec():
                logging.error(f"Failed to update record: {query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                return False
            else:
                logging.debug("Record updated successfully.")

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")

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
                self.update_database(row, column, new_value)

    def table_contracts_view(self):
        self.tableWidget_Contracts.itemChanged.disconnect(self.on_item_changed)
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.contracts_model.select()

        """ Обновляет содержимое QTableWidget на основе данных модели. """
        self.tableWidget_Contracts.setRowCount(0)  # Очищаем существующие данные
        self.tableWidget_Contracts.setColumnCount(
            self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Отключаем отображение номеров строк
        self.tableWidget_Contracts.verticalHeader().setVisible(False)

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.tableWidget_Contracts.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))

                item = qtw.QTableWidgetItem()
                if column in [1, 2, 3, 4, 5, 8]:  # Запрет редактирования для 1-5 колонок
                    item.setText(str(item_data))  # Для остальных значений
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Убираем флаг редактирования
                else:
                    if isinstance(item_data, bool):  # Если это логическое значение
                        item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                        item.setFlags(
                            item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable |
                            Qt.ItemFlag.ItemIsSelectable)
                    else:
                        item.setText(str(item_data))  # Для остальных значений
                        item.setFlags(
                            item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | ~Qt.ItemFlag.ItemIsUserCheckable)

                self.tableWidget_Contracts.setItem(row, column, item)

        # Включаем сортировку
        # self.tableWidget_Contracts.setSortingEnabled(True)
        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)


    def filter_data(self):
        """ Фильтрация данных в таблице на основе ввода пользователя. """
        try:
            # Отключаем сигнал itemChanged перед фильтрацией
            self.tableWidget_Contracts.itemChanged.disconnect(self.on_item_changed)
            # Получаем текст фильтра из строки ввода
            filter_text = self.lineEdit_FilterChild.text().strip()

            # Проверяем наличие текста для фильтрации
            if filter_text:
                # Формируем условие фильтрации с использованием ILIKE для нечувствительности к регистру
                query = f"SELECT * FROM contracts_view WHERE child_fio ILIKE '%{filter_text}%'"
                self.contracts_model.setQuery(query)
            else:
                # Если фильтр пустой, сбрасываем фильтрацию с первоначальным запросом
                self.contracts_model.setTable('contracts_view')
                self.contracts_model.select()

            # Обновляем таблицу
            self.table_contracts_view()  # Теперь вызываем метод обновления таблицы

        except Exception as e:
            logging.error("Ошибка фильтрации: %s", str(e))
            qtw.QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            # Подключаем сигнал обратно после выполнения фильтрации
            self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)

    def on_contract_selected(self):

        # Получаем выбранные индексы
        selected_indexes = self.tableWidget_Contracts.selectedIndexes()
        if selected_indexes:
            # Получаем строку из первого выбранного индекса
            row = selected_indexes[0].row()
            # Предполагаем, что ID договора находится в 0 столбце
            self.contract_id = self.contracts_model.data(self.contracts_model.index(row, 0))
            print(f'on_contract_selected {self.contract_id=}')
            self.load_selected_contract(self.contract_id)

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
                # self.tableWidget_Contracts.itemChanged.disconnect(self.on_item_changed)
                # self.contracts_model.setTable('contracts_view')
                # self.contracts_model.select()
                # Обновляем таблицу
                self.table_contracts_view()  # Теперь вызываем метод обновления таблицы
                self.load_selected_contract(self.contract_id)
                # self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")
