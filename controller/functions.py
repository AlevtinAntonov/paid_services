from PyQt6 import QtSql, QtCore

from datetime import datetime


def get_parents_fio():
    # Пример функции для получения имен уроков из базы данных
    parents_fio = []
    query = QtSql.QSqlQuery(
        "SELECT parent_fio FROM parents_view")  # Измените на правильный запрос для получения названий уроков
    while query.next():
        parents_fio.append(query.value(0))  # Предполагаем, что названия уроков находятся в первой колонке
    return parents_fio


def get_child_fio():
    # Пример функции для получения имен уроков из базы данных
    child_fio = []
    query = QtSql.QSqlQuery(
        "SELECT child_fio FROM children_view")  # Измените на правильный запрос для получения названий уроков
    while query.next():
        child_fio.append(query.value(0))  # Предполагаем, что названия уроков находятся в первой колонке
    return child_fio


def get_lesson_names():
    # Пример функции для получения имен уроков из базы данных
    lesson_names = []
    query = QtSql.QSqlQuery(
        "SELECT lesson_name FROM lessons")  # Измените на правильный запрос для получения названий уроков
    while query.next():
        lesson_names.append(query.value(0))  # Предполагаем, что названия уроков находятся в первой колонке
    return lesson_names


def get_team_names():
    # Пример функции для получения названий команд из базы данных
    team_names = []
    query = QtSql.QSqlQuery(
        "SELECT team_name FROM teams")  # Измените на правильный запрос для получения названий команд
    while query.next():
        team_names.append(query.value(0))  # Предполагаем, что названия команд находятся в первой колонке
    return team_names


def validate_and_convert_date(input_date: str) -> str:
    # Заменяем любые разделители на точки
    input_date = input_date.replace('/', '.').replace('-', '.').replace(' ', '.').replace(',', '.').replace('#', '.').replace(':', '.')

    # Разделяем строку на компоненты даты
    parts = input_date.split('.')

    # Получаем текущий год
    current_year = datetime.now().year

    # Проверяем количество частей
    if len(parts) == 3:  # формат "день.месяц.год"
        try:
            day = int(parts[0])
            month = int(parts[1])

            year = parts[2]
            if len(year) == 2:
                # Преобразуем двухзначный год в четырехзначный
                year = '20' + year if int(year) < 50 else '19' + year
            year = int(year)

            # Проверяем корректность даты
            date = QtCore.QDate(year, month, day)
            if date.isValid():
                return date.toString("dd.MM.yyyy")
            else:
                return "Неверная дата"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    elif len(parts) == 2:  # формат "день.месяц"
        try:
            day = int(parts[0])
            month = int(parts[1])

            # Используем текущий год
            year = current_year

            # Проверяем корректность даты
            date = QtCore.QDate(year, month, day)
            if date.isValid():
                return date.toString("dd.MM.yyyy")
            else:
                return "Неверная дата"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    return "Неверный формат даты"


if __name__ == '__main__':
    text = input("Enter any date: ")
    print(validate_and_convert_date(text))