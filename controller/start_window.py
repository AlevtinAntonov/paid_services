from PyQt6 import QtWidgets as qtw, QtSql, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
import logging

from controller.functions import get_lesson_names, get_team_names, validate_and_convert_date
from model.db_connect import DatabaseConnector
from view.main_window import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG)


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Создаем экземпляр DatabaseConnector и подключаемся к базе данных
        self.db_connector = DatabaseConnector()
        if not self.db_connector.connect():
            return  # Если подключение не удалось, выходим из конструктора

        self.tbl_contracts_view()
        # self.refresh_table()
        self.setup_tbl_contracts_view()

        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)

    def tbl_contracts_view(self):
        # Создаем модели для таблиц
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.contracts_model.select()

        self.tableWidget_Contracts.setRowCount(0)  # Сбрасываем количество строк
        self.tableWidget_Contracts.setColumnCount(self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.tableWidget_Contracts.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))

                item = qtw.QTableWidgetItem()
                if column in [1, 2, 3, 4, 5]:  # Запрет редактирования для 1-5 колонок
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
        self.tableWidget_Contracts.setSortingEnabled(True)

    def on_item_changed(self, item):
        row = item.row()
        column = item.column()

        logging.debug(f'Item changed at row {row}, column {column}. New value: {item.text()}')

        if column in [7, 9]:  # для checkbox колонок
            new_state = item.checkState() == Qt.CheckState.Checked
            logging.debug(f'Checkbox state changed at row {row}, column {column}. New state: {new_state}')
            self.update_database(row, column, new_state)
        else:  # для текстовых ячеек
            new_value = item.text()  # получаем новое текстовое значение
            logging.debug(f'Text value changed at row {row}, column {column}. New value: {new_value}')
            self.update_database(row, column, new_value)

    def handle_date_input(self, input_value):
        # input_value = date_edit.text()
        new_date = validate_and_convert_date(input_value)
        if "Неверный формат даты" not in new_date and "Неверная дата" not in new_date:
            return new_date
            # date_edit.setDate(QtCore.QDate.fromString(new_date, "dd.MM.yyyy"))
        else:
            logging.debug(f'Ошибка в handle_date_input {input_value=} -> {new_date=} !!!')
            return None

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
            }

            column_name = column_map.get(column)
            logging.debug(f'Column index: {column}, Column name: {column_name}')
            if column_name is None:
                logging.error(f"Invalid column index: {column}")
                return  # Не продолжаем, если индекс невалидный

            if column in [2, 8]:  # Столбцы, связанные с датами
                formatted_date = self.handle_date_input(new_value)
                if formatted_date:
                    new_value = formatted_date

            logging.debug(f'Preparing SQL update for: {column_name}, new_value={new_value}, contract_id={contract_id}')

            query = QtSql.QSqlQuery()
            query.prepare(f"UPDATE contracts SET {column_name} = :value WHERE contract_id = :id;")
            query.bindValue(":value", new_value)
            query.bindValue(":id", contract_id)

            if not query.exec():
                logging.error(f"Failed to update record: {query.lastError().text()}")
                QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                return False
            else:
                logging.debug("Record updated successfully.")
                self.refresh_table()

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")

    def setup_tbl_contracts_view(self):
        self.tableWidget_Contracts.setColumnHidden(0, True)  # Скрываем ID
        self.tableWidget_Contracts.setColumnWidth(1, 50)
        self.tableWidget_Contracts.setColumnWidth(2, 80)
        self.tableWidget_Contracts.setColumnWidth(3, 200)
        self.tableWidget_Contracts.setColumnWidth(4, 160)
        self.tableWidget_Contracts.setColumnWidth(5, 100)
        self.tableWidget_Contracts.setColumnWidth(6, 200)
        self.tableWidget_Contracts.setColumnWidth(7, 50)
        self.tableWidget_Contracts.setColumnWidth(8, 80)
        self.tableWidget_Contracts.setColumnWidth(9, 50)

        self.tableWidget_Contracts.setHorizontalHeaderLabels(['ID', 'Номер', 'Дата', 'Ребенок', 'Кружок', 'Группа',
                                                              'Примечание', 'Подп.', 'Дата раст.', 'Согл.подп.'])

    def refresh_table(self):
        """Обновляет данные в tableWidget_Contracts из базы данных."""
        logging.debug("Refreshing table data from the database.")

        # Очищаем текущее содержимое таблицы
        self.tableWidget_Contracts.clearContents()
        self.tableWidget_Contracts.setRowCount(0)  # Убедитесь, что количество строк сброшено

        # Создаем и настраиваем модель для данных
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        if not self.contracts_model.select():  # Извлекаем данные из таблицы
            logging.error(f"Failed to select data from contracts_view: {self.contracts_model.lastError().text()}")
            return

        self.tableWidget_Contracts.setColumnCount(
            self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Заполняем QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.tableWidget_Contracts.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))
                logging.debug(
                    f'{range(self.contracts_model.rowCount())=} {range(self.contracts_model.columnCount())=} {item_data=}')

                item = qtw.QTableWidgetItem()  # Создаем элемент для таблицы

                if isinstance(item_data, bool):  # Если это логическое значение
                    logging.debug('Creating checkbox item.')
                    item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable |
                                  Qt.ItemFlag.ItemIsSelectable)
                else:
                    logging.debug('Creating text item.')
                    item.setText(str(item_data))  # Для остальных значений
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)

                logging.debug(f'Inserting item into table at row {row}, column {column}.')
                self.tableWidget_Contracts.setItem(row, column, item)  # Устанавливаем элемент в таблице

        # Включаем сортировку
        self.tableWidget_Contracts.setSortingEnabled(True)
        logging.debug("Table refreshed successfully.")
