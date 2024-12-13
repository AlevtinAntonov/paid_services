from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox
from model.db_params import db_parameters

class DatabaseConnector:
    """
    Класс для подключения к PostgreSQL базе данных.
    """

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QPSQL")

    def connect(self):
        """
        Подключение к базе данных.
        """
        # Устанавливаем параметры подключения
        self.db.setHostName(db_parameters['host'])
        self.db.setDatabaseName(db_parameters['dbname'])
        self.db.setUserName(db_parameters['user'])
        self.db.setPassword(db_parameters['password'])
        self.db.setPort(db_parameters['port'])

        # Проверяем, поддерживается ли драйвер
        # if not QSqlDatabase.isDriverAvailable("QPSQL"):
        #     QMessageBox.critical(None, "Ошибка драйвера",
        #                          "Драйвер QPSQL не загружен. Пожалуйста, установите его.")
        #     return False
        #
        # # Открываем соединение
        # if not self.db.open():
        #     QMessageBox.critical(None, "Ошибка подключения",
        #                          "Не удалось подключиться к базе данных.\nОшибка: " + self.db.lastError().text())
        #     return False
        #
        # QMessageBox.information(None, "Успех", "Подключение к базе данных успешно!")
        return True
