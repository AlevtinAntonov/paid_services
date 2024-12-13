from PyQt6 import QtCore, QtSql

from datetime import datetime

from model.db_connect import DatabaseConnector


def get_data_from_db(data_type):
    """
    Получает данные из базы данных в зависимости от типа запрашиваемых данных.

    :param data_type: Тип запрашиваемых данных ('parents', 'children', 'lessons', 'teams')
    :return: Список с данными
    """
    data = []
    if data_type == 'parents':
        query = QtSql.QSqlQuery("SELECT parent_fio FROM parents_view")
    elif data_type == 'children':
        query = QtSql.QSqlQuery("SELECT child_fio FROM children_view")
    elif data_type == 'lessons':
        query = QtSql.QSqlQuery("SELECT lesson_building FROM lessons_view")
    elif data_type == 'teams':
        query = QtSql.QSqlQuery("SELECT team_name FROM teams")
    else:
        raise ValueError("Неверный тип данных. Используйте 'parents', 'children', 'lessons' или 'teams'.")

    while query.next():
        data.append(query.value(0))
    return data

def get_data_id_from_db(data_type, data):
    """
    Получает данные из базы данных в зависимости от типа запрашиваемых данных.
    :param data_type: Тип запрашиваемых данных ('parents', 'children', 'lessons', 'teams')
    :param data: Значение для поиска
    :return: person_id, lesson_id или team_id
    """
    query = QtSql.QSqlQuery()

    if data_type == 'parents':
        query.prepare("SELECT person_id FROM parents_view WHERE parent_fio = :data")
    elif data_type == 'children':
        query.prepare("SELECT person_id FROM children_view WHERE child_fio = :data")
    elif data_type == 'lessons':
        query.prepare("SELECT lesson_id FROM lessons_view WHERE lesson_building = :data")
    elif data_type == 'teams':
        query.prepare("SELECT team_id FROM teams WHERE team_name = :data")
    else:
        raise ValueError("Неверный тип данных. Используйте 'parents', 'children', 'lessons' или 'teams'.")

    query.bindValue(":data", data)

    if query.exec():
        if query.next():
            return query.value(0)
        else:
            print("No data found.")
            return None
    else:
        print("Query execution failed:", query.lastError().text())
        return None

def get_data(selected_name, col):
    """
    Получает данные из модели по указанной колонке.

    :param selected_name: объект модели данных
    :param col: индекс колонки
    :return: строковое значение из модели или пустая строка
    """
    if selected_name.data(selected_name.index(0, col)) is not None:
        return str(selected_name.data(selected_name.index(0, col)))
    return ""


def populate_combobox(model_name, item_name, items_list, col):
    """
    Заполняет указанный комбобокс значениями из списка.

    :param item_name: Имя комбобокса (например, comboBox_ContractApplicant)
    :param items_list: Список значений для заполнения комбобокса
    """
    # Очистка комбобокса перед заполнением
    item_name.clear()
    item_name.addItems(items_list)  # Заполнение значениями из списка

    current_data = get_data(model_name, col)  # Получаем текущее значение из модели контрактов
    if current_data in items_list:
        item_name.setCurrentText(current_data)  # Устанавливаем текущее значение если оно в списке
    else:
        print(f"Текущее значение '{current_data}' не найдено в списке.")

def get_combobox_value(combo_box):
    """ Возвращает значение из comboBox или None. """
    value = combo_box.currentText()
    return value if value else None

def get_input_value(input_field):
    """ Возвращает текст из QLineEdit или None. """
    value = input_field.text()
    return value if value else None


def validate_and_convert_date(input_date: str) -> str:
    # Заменяем любые разделители на точки
    input_date = input_date.replace('/', '.').replace('-', '.').replace(' ', '.').replace(',', '.').replace('#',
                                                                                                            '.').replace(
        ':', '.')

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
    db_connector = DatabaseConnector()
    if not db_connector.connect():
        print('No database connected.')
    else:
        print('Database connected.')
        applicant_id = get_data_id_from_db('parents', 'Ванаг Екатерина Олеговна')
        print(applicant_id)
    # app = QtCore.QCoreApplication([])
    # print("Available Drivers 1:", QtSql.QSqlDatabase.drivers())
    #
    # db_driver = QtSql.QSqlDatabase.drivers()
    # print("Available Drivers 2:", QtSql.QSqlDatabase.drivers())


