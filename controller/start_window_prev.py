from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
import logging

from controller.functions import get_lesson_names, get_team_names
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
        self.setup_tbl_contracts_view()

        self.tableWidget_Contracts.itemChanged.connect(self.on_item_changed)

    def tbl_contracts_view(self):
        # Создаем модели для таблиц
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.contracts_model.select()

        self.tableWidget_Contracts.setRowCount(0)  # Сбрасываем количество строк
        self.tableWidget_Contracts.setColumnCount(
            self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Получаем доступные названия уроков и групп из БД
        lesson_names = get_lesson_names()
        team_names = get_team_names()  # Получение доступных названий команд из БД

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.tableWidget_Contracts.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))

                if column == 4:  # Если это четвертая колонка
                    combo_box = qtw.QComboBox()
                    combo_box.addItems(lesson_names)  # Заполнение значениями из базы данных
                    combo_box.setCurrentText(str(item_data))  # Установите текущее значение из БД
                    self.tableWidget_Contracts.setCellWidget(row, column, combo_box)
                    combo_box.currentIndexChanged.connect(lambda index, r=row: self.on_combobox_changed(index, r))
                elif column == 5:  # Если это пятая колонка (название команды)
                    team_combo_box = qtw.QComboBox()
                    team_combo_box.addItems(team_names)  # Заполнение значениями из базы данных
                    team_combo_box.setCurrentText(str(item_data))  # Установите текущее значение из БД
                    self.tableWidget_Contracts.setCellWidget(row, column, team_combo_box)
                    team_combo_box.currentIndexChanged.connect(lambda index, r=row: self.on_combobox_changed(index, r))
                else:

                    item = qtw.QTableWidgetItem()
                    if column == 1 or column == 2 or column == 3:  # Запрет редактирования для 1-й - 3-й колонок
                        item.setText(str(item_data))  # Для остальных значений
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Убираем флаг редактирования
                    else:
                        if isinstance(item_data, bool):  # Если это логическое значение
                            item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                            item.setFlags(
                                item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable |
                                Qt.ItemFlag.ItemIsSelectable)
                            item.setTextAlignment(
                                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)  # Выравнивание

                        else:
                            item.setText(str(item_data))  # Для остальных значений
                            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)

                    self.tableWidget_Contracts.setItem(row, column, item)

        # Включаем сортировку
        self.tableWidget_Contracts.setSortingEnabled(True)



    def on_combobox_changed(self, index, row):
        combo_box = self.tableWidget_Contracts.cellWidget(row, 4)  # Получаем QComboBox
        new_value = combo_box.currentText()  # Получаем текущее значение
        logging.debug(f'Combobox value changed at row {row}, new value: {new_value}')
        self.update_database(row, 4, new_value)  # Обновляем базу данных

    def on_item_changed(self, item):
        row = item.row()
        column = item.column()

        logging.debug('Item flags: %s', item.flags())

        # Проверка на чекбокс
        if column in [7, 9]:
            new_state = item.checkState() == Qt.CheckState.Checked  # Получаем новое состояние чекбокса
            logging.debug(f'Checkbox state changed at row {row}, column {column}. New state: {new_state}')
            self.update_database(row, column, new_state)
        else:  # Это текстовая ячейка
            new_value = item.text()  # Получаем новое текстовое значение
            logging.debug(f'Text value changed at row {row}, column {column}. New value: {new_value}')
            self.update_database(row, column, new_value)

    def update_database(self, row, column, new_state):
        try:
            # Получаем contract_id из таблицы
            contract_id = self.contracts_model.data(
                self.contracts_model.index(row, 0))  # Предполагаем, что contract_id в первом столбце

            # Словарь для соответствия номеров столбцов и имен полей
            column_map = {
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

            if column in [1, 2, 6, 7, 8, 9]:
                query = QtSql.QSqlQuery()
                query.prepare(f"UPDATE contracts SET {column_name} = :value WHERE contract_id = :id;")
                query.bindValue(":value", new_state)
                query.bindValue(":id", contract_id)

                if not query.exec():
                    QMessageBox.critical(None, "Ошибка", "Не удалось обновить запись:\n" + query.lastError().text())
                    logging.error(f"Failed to update record: {query.lastError().text()}")
                    return False
                else:
                    logging.debug("Record updated successfully.")
            else:
                print("Изменения не должны быть записаны для данного столбца.")

        except Exception as e:
            print("Ошибка при обновлении базы данных:", e)

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


