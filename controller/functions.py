from PyQt6 import QtSql


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