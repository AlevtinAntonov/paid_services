from PyQt6 import QtWidgets as qtw, QtGui, QtSql, QtWidgets
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox

from model.db_params import db_parameters
from view.main_window import Ui_MainWindow


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_db()

        # Создаем модели для таблиц
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts_view')
        self.contracts_model.select()

        # # Создаем таблицы для отображения данных
        # self.tableView_ContractInfo.setModel(self.contracts_model)
        # self.tableView_ContractInfo.setSortingEnabled(True)
        # Очищаем QTableWidget перед добавлением данных
        self.tableWidget_Contracts.setRowCount(0)  # Сбрасываем количество строк
        self.tableWidget_Contracts.setColumnCount(
            self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.tableWidget_Contracts.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item = QtWidgets.QTableWidgetItem(self.contracts_model.data(self.contracts_model.index(row, column)))
                self.tableWidget_Contracts.setItem(row, column, item)  # Заполняем ячейку

        # Включаем сортировку
        self.tableWidget_Contracts.setSortingEnabled(True)



    def connect_db(self):
        # Проверяем, поддерживается ли драйвер
        if not QSqlDatabase.isDriverAvailable("QPSQL"):
            QMessageBox.critical(self, "Driver error драйвера",
                                 "Драйвер QPSQL не загружен not load. Пожалуйста, установите его.")
            return

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(db_parameters['host'])  # Хост
        self.db.setDatabaseName(db_parameters['dbname'])  # Имя вашей базы данных
        self.db.setUserName(db_parameters['user'])  # Имя пользователя
        self.db.setPassword(db_parameters['password'])  # Пароль
        self.db.setPort(db_parameters['port'])

        if not self.db.open():
            # Выводим сообщение об ошибке с подробностями
            QMessageBox.critical(self, "Connection error Ошибка подключения",
                                 "Don't connect Не удалось подключиться к базе данных.\nОшибка: " + self.db.lastError().text())
            return

        QMessageBox.information(self, "Успех", "Подключение к базе данных успешно!")
