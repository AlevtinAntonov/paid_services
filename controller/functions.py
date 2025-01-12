import logging
import re

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore, QtSql
from datetime import datetime

from PyQt6.QtWidgets import QMessageBox

from model.db_connect import DatabaseConnector

def show_error(message):
    QMessageBox.critical(None, "Ошибка", message)
    return

def save_cancel_translate(self):
    # Изменяем текст кнопок на русский
    save_button = self.button_box.button(qtw.QDialogButtonBox.StandardButton.Save)
    cancel_button = self.button_box.button(qtw.QDialogButtonBox.StandardButton.Cancel)

    save_button.setText("Сохранить")
    cancel_button.setText("Отмена")

def setup_table_view(table_widget, column_widths, headers):
    table_widget.setColumnHidden(0, True)  # Скрываем ID
    for index, width in enumerate(column_widths):
        table_widget.setColumnWidth(index + 1, width)  # Учитываем, что ID находится на нулевом индексе
    table_widget.setHorizontalHeaderLabels(headers)


def get_data_from_db(data_type):
    """
    Получает данные из базы данных в зависимости от типа запрашиваемых данных.

    :param data_type: Тип запрашиваемых данных ('parents', 'children', 'lessons', 'teams')
    :return: Список с данными
    """
    # Определяем запросы в виде словаря
    queries = {
        'parents': "SELECT parent_fio FROM parents_view",
        'children': "SELECT child_fio FROM children_view",
        'lessons': "SELECT lesson_building FROM lessons_view",
        'teams': "SELECT team_name FROM teams",
        'genders': "SELECT gender_name FROM genders",
        'months': "SELECT month_name FROM months ORDER BY sorting",
        'buildings': "SELECT building_number FROM buildings ORDER BY building_number",
        'teachers': "SELECT (last_name || ' ' || first_name || ' ' || patronymic) AS teacher_fio "
                    "FROM teachers WHERE is_visible = TRUE ORDER BY teacher_fio",
    }

    if data_type not in queries:
        raise ValueError("Неверный тип данных. Используйте 'parents', 'children', 'lessons' или 'teams'.")

    query = QtSql.QSqlQuery(queries[data_type])  # Выполняем запрос

    data = []
    while query.next():  # Считываем все результаты
        data.append(query.value(0))  # Добавляем значение в список

    return data


def get_data_id_from_db(data_type, data):
    """
    Получает данные из базы данных в зависимости от типа запрашиваемых данных.

    :param data_type: Тип запрашиваемых данных ('parents', 'children', 'lessons', 'teams')
    :param data: Значение для поиска
    :return: person_id, lesson_id или team_id
    """
    # Определяем запросы в виде словаря
    queries = {
        'parents': "SELECT person_id FROM parents_view WHERE parent_fio = :datas",
        'children': "SELECT person_id FROM children_view WHERE child_fio = :datas",
        'lessons': "SELECT lesson_id FROM lessons_view WHERE lesson_building = :datas",
        'teams': "SELECT team_id FROM teams WHERE team_name = :datas",
        'months': "SELECT month_id FROM months WHERE month_name = :datas",
        'buildings': "SELECT building_id FROM buildings WHERE building_number = :datas",
        'genders': "SELECT gender_id FROM genders WHERE gender_name = :datas",
        'teachers': "SELECT teacher_id FROM teachers WHERE (last_name || ' ' || first_name || ' ' || patronymic) = :datas ",
    }

    if data_type not in queries:
        raise ValueError("Неверный тип данных. Используйте 'parents', 'children', 'lessons' или 'teams'.")

    query = QtSql.QSqlQuery()
    query.prepare(queries[data_type])  # Подготовка запроса
    query.bindValue(":datas", data)  # Привязка значения

    if query.exec():
        if query.next():  # Если есть хотя бы одна строка с результатом
            return query.value(0)  # Возвращаем значение
        else:
            logging.warning("No datas found for the provided value: %s", data)
            return None
    else:
        logging.error("Query execution failed: %s", query.lastError().text())
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

def get_value_with_default(model, index, default='-'):
    value = get_data(model, index)
    return value if value not in [None, ''] else default


def get_document_details(selected_model, start_index=9):
    # Список индексов для получения значений
    indexes = {
        "Тип документа": start_index,
        "Серия": start_index + 1,
        "Номер": start_index + 2,
        "Выдан": start_index + 3,
        "Дата выдачи": start_index + 4,
    }

    # Получаем значения и формируем документ
    document_details = {key: get_value_with_default(selected_model, index) for key, index in indexes.items()}

    # Формируем строку с деталями документа
    document_string = '\n'.join(
        f'{key}: {document_details[key]}' for key in indexes.keys()
    )

    return document_string



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


def get_value_id(table_model, tbl_name, row, value_id_index):
    """ Получить идентификатор записи в зависимости от типа таблицы. """
    if tbl_name in ['contracts', 'visit_log', 'invoices', 'payments']:
        return table_model.data(table_model.index(row, value_id_index))
    return None


def get_selected_id(table_widget, model, column):
    """ Получает ID из выбранной строки таблицы. """
    selected_indexes = table_widget.selectedIndexes()
    if selected_indexes:
        row = selected_indexes[0].row()
        return model.data(model.index(row, column))
    return None


def check_and_convert_to_int(value):
    """
    Проверяет, является ли переменная целым числом или может быть преобразована в целое число.
    Если не может быть преобразована, возвращает 0.

    :param value: Значение для проверки и преобразования.
    :return: Целое число.
    """
    try:
        # Пробуем преобразовать значение в целое число
        return int(value)
    except (ValueError, TypeError):
        # Если возникает ошибка, возвращаем 0
        return 0


def get_lesson_fact_visit(invoice_id):
    query = QtSql.QSqlQuery()
    query.prepare("SELECT lessons_fact FROM visit_log_view WHERE invoice_id = :invoice_id")
    query.bindValue(":invoice_id", invoice_id)

    if not query.exec():
        logging.error(f"Failed to execute query to find lesson_fact_visit: {query.lastError().text()}")
        QMessageBox.critical(None, "Ошибка",
                             "Не удалось получить данные о фактическом посещении:\n" + query.lastError().text())
        return None

    if query.next():
        return check_and_convert_to_int(query.value(0))  # Получаем значение

    logging.warning(f'No lesson_fact_visit found for invoice_id: {invoice_id}')
    return 0  # Если запись не найдена, возвращаем 0


def delete_related_records(invoice_id):
    queries = {
        "visit_log": "DELETE FROM visit_log WHERE invoice_id = :invoice_id",
        "payments": "DELETE FROM payments WHERE invoice_id = :invoice_id",
        "invoices": "DELETE FROM invoices WHERE invoice_id = :invoice_id"
    }

    for record_type, query in queries.items():
        delete_query = QtSql.QSqlQuery()
        delete_query.prepare(query)
        delete_query.bindValue(":invoice_id", invoice_id)

        if not delete_query.exec():
            logging.error(f"Failed to delete {record_type} record: {delete_query.lastError().text()}")
            QMessageBox.critical(None, "Ошибка",
                                 f"Не удалось удалить записи из {record_type}:\n" + delete_query.lastError().text())
            return False

    return True


def insert_invoice(contract_id, month_id, lessons_per_month, remarks):
    """Вставляет новую квитанцию в таблицу invoices и добавляет её в журнал посещений."""
    insert_query = QtSql.QSqlQuery()
    insert_query.prepare("""INSERT INTO invoices (contract_id, month_id, lessons_per_month, remarks) 
                             VALUES (:contract_id, :month_id, :lessons_per_month, :remarks)""")
    insert_query.bindValue(":contract_id", contract_id)
    insert_query.bindValue(":month_id", month_id)
    insert_query.bindValue(":lessons_per_month", lessons_per_month)
    insert_query.bindValue(":remarks", remarks)

    if not insert_query.exec():
        handle_query_error(None, insert_query, "Не удалось добавить новую запись в invoices")
        return False

    logging.debug("Record inserted successfully in invoices.")

    invoice_id = insert_query.lastInsertId()  # Получаем id последней вставленной записи
    return insert_visit_log(invoice_id)

def insert_new_lesson(lesson_name, building_id, lesson_rate, lessons_per_year):
    insert_query = QtSql.QSqlQuery()
    insert_query.prepare("""INSERT INTO lessons(lesson_name, building_id, lesson_rate, lessons_per_year) 
                             VALUES (:lesson_name, :building_id, :lesson_rate, :lessons_per_year)""")
    insert_query.bindValue(":lesson_name", lesson_name)
    insert_query.bindValue(":building_id", building_id)
    insert_query.bindValue(":lesson_rate", lesson_rate)
    insert_query.bindValue(":lessons_per_year", lessons_per_year)

    if not insert_query.exec():
        handle_query_error(None, insert_query, "Не удалось добавить новую запись в lessons")
        return False

    logging.debug("Record inserted successfully in lessons.")
    return True

def insert_new_teacher(last_name, first_name, patronymic, gender_id, phone, email):
    insert_query = QtSql.QSqlQuery()
    insert_query.prepare("""INSERT INTO teachers (last_name, first_name, patronymic, gender_id, phone, email)
                             VALUES (:last_name, :first_name, :patronymic, :gender_id, :phone, :email)""")
    insert_query.bindValue(":last_name", last_name)
    insert_query.bindValue(":first_name", first_name)
    insert_query.bindValue(":patronymic", patronymic)
    insert_query.bindValue(":gender_id", gender_id)
    insert_query.bindValue(":phone", phone)
    insert_query.bindValue(":email", email)

    if not insert_query.exec():
        handle_query_error(None, insert_query, "Не удалось добавить новую запись в teachers")
        return False

    logging.debug("Record inserted successfully in teachers.")
    return True

def insert_visit_log(invoice_id):
    """Добавляет новую запись в visit_log с заданным invoice_id."""
    insert_log_query = QtSql.QSqlQuery()
    insert_log_query.prepare("INSERT INTO visit_log (invoice_id) VALUES (:invoice_id)")
    insert_log_query.bindValue(":invoice_id", invoice_id)

    if not insert_log_query.exec():
        handle_query_error(None, insert_log_query, "Не удалось добавить новую запись в журнал посещений")
        return False

    logging.debug("Record inserted successfully in visit_log.")
    return True

def insert_new_record(dialog_class, insert_function, success_callback):
    dialog = dialog_class()
    logging.debug(f"{dialog_class.__name__} dialog opened")

    if dialog.exec() == qtw.QDialog.DialogCode.Accepted:
        logging.debug(f"{dialog_class.__name__} dialog accepted")
        try:
            data = dialog.get_data()
            insert_function(*data)  # Распаковываем данные для передачи в функцию вставки
            success_callback()  # Вызываем функцию для обновления таблицы
        except Exception as e:
            logging.error(f"Error while saving record: {str(e)}")
            show_error(f"Не удалось сохранить запись: {str(e)}")


def handle_query_error(self, query, message):
    """Обрабатывает ошибку выполнения запроса и показывает сообщение пользователю."""
    logging.error(f"{message}: {query.lastError().text()}")
    QMessageBox.critical(None, "Ошибка", f"{message}:\n{query.lastError().text()}")


def execute_query(query):
    """ Выполняет SQL-запрос и обрабатывает ошибки. """
    try:
        if not query.exec():
            error_message = f"Не удалось обновить запись:\n{query.lastError().text()}"
            logging.error(error_message)
            QMessageBox.critical(None, "Ошибка", error_message)
            return False

        logging.debug("Запись успешно обновлена.")
        return True

    except Exception as e:
        logging.error(f"Ошибка при выполнении запроса: {e}")
        return False


def validate_and_convert_date(input_date: str) -> str:
    # Проверяем, пустая ли строка или не содержит цифр
    if not input_date or not any(char.isdigit() for char in input_date):
        return None

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


def get_next_contract_number():
    """ Получает следующий номер контракта, основываясь на максимальном значении contract_number. """
    query = QtSql.QSqlQuery()

    # Запрос на получение максимального значения
    query.prepare("SELECT MAX(contract_number) FROM contracts")

    if not query.exec():
        logging.debug(f"Ошибка выполнения запроса: {query.lastError().text()}")
        return None  # Возвращаем None в случае ошибки

    if query.next():  # Переходим к первой строке результата
        max_value = query.value(0)  # Получаем значение из первого столбца
        if max_value is not None:  # Проверяем, что максимальное значение не None
            return max_value + 1  # Возвращаем следующий номер (максимальное значение + 1)

    return 1  # Если нет записей, возвращаем 1 как первый номер контракта


def is_valid_email(email):
    # Регулярное выражение для проверки корректности адреса электронной почты
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def update_visibility(lesson_id, teacher_id):
    query = QtSql.QSqlQuery()
    update_visibility_query = """UPDATE teachers_lessons 
                                SET is_visible = FALSE 
                                WHERE lesson_id = :lesson_id AND teacher_id = :teacher_id;"""
    query.prepare(update_visibility_query)
    query.bindValue(":lesson_id", lesson_id)
    query.bindValue(":teacher_id", teacher_id)
    return execute_query(query)

def update_column_visibility(table_name, id_column, id_value):
    query = QtSql.QSqlQuery()
    update_visibility_query = f"""UPDATE {table_name} 
                                SET is_visible = FALSE 
                                WHERE {id_column} = :id_value;"""
    query.prepare(update_visibility_query)
    query.bindValue(":id_value", id_value)
    return execute_query(query)



if __name__ == '__main__':
    # db_connector = DatabaseConnector()
    # if not db_connector.connect():
    #     print('No database connected.')
    # else:
    #     print('Database connected.')
    #     applicant_id = get_data_id_from_db('parents', 'Ванаг Екатерина Олеговна')
    #     print(applicant_id)
    # app = QtCore.QCoreApplication([])
    # print("Available Drivers 1:", QtSql.QSqlDatabase.drivers())
    #
    # db_driver = QtSql.QSqlDatabase.drivers()
    # print("Available Drivers 2:", QtSql.QSqlDatabase.drivers())
    print(validate_and_convert_date(None))
