from PyQt6 import QtWidgets as qtw, QtSql

from controller.functions import get_data_from_db, get_data_id_from_db, show_error, execute_query, get_selected_id
from view.teacher_choice_dialog import Ui_TeacherChoice


class TeacherChoiceDialog(qtw.QDialog, Ui_TeacherChoice):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data_load()

    def data_load(self):
        teachers_fio = get_data_from_db('teachers')
        self.comboBox_TeacherChoice.addItem("")
        self.comboBox_TeacherChoice.addItems(teachers_fio)
        self.comboBox_TeacherChoice.setEditable(True)

    def get_contract_data(self):
        if self.comboBox_TeacherChoice.currentText() != '-':
            teacher_id = get_data_id_from_db('teachers', self.comboBox_TeacherChoice.currentText())
            if not teacher_id:
                return show_error("Таких ФИО нет в базе\n проверьте ввод:")
            return teacher_id
        return 'is_visible_set_false'

    def update_data(self, lesson_id):
        teacher_id = self.get_contract_data()
        print(f'Обработка связи для teacher_id={teacher_id}, lesson_id={lesson_id}')

        query = QtSql.QSqlQuery()

        # 1. Проверка существующей записи
        check_query = """SELECT is_visible FROM teachers_lessons 
                         WHERE teacher_id = :teacher_id AND lesson_id = :lesson_id;"""
        query.prepare(check_query)
        query.bindValue(":teacher_id", teacher_id)
        query.bindValue(":lesson_id", lesson_id)

        if not execute_query(query) or not query.next():  # Запись не найдена
            # 2. Проверка наличия других записей с lesson_id
            check_lessons_query = """SELECT COUNT(*) FROM teachers_lessons 
                                     WHERE lesson_id = :lesson_id;"""
            query.prepare(check_lessons_query)
            query.bindValue(":lesson_id", lesson_id)

            if execute_query(query) and query.next() and query.value(0) > 0:
                # Если записи с таким lesson_id существуют, обновить их
                update_visibility_query = """UPDATE teachers_lessons 
                                              SET is_visible = FALSE 
                                              WHERE lesson_id = :lesson_id AND teacher_id != :teacher_id;"""
                query.prepare(update_visibility_query)
                query.bindValue(":lesson_id", lesson_id)
                query.bindValue(":teacher_id", teacher_id)
                execute_query(query)

            # 3. Добавление новой записи
            insert_query = """INSERT INTO teachers_lessons (teacher_id, lesson_id, is_visible) 
                              VALUES (:teacher_id, :lesson_id, TRUE);"""
            query.prepare(insert_query)
        else:
            # 4. Обновление существующей записи (например, если нужно изменить is_visible)
            update_query = """UPDATE teachers_lessons 
                              SET is_visible = TRUE 
                              WHERE teacher_id = :teacher_id AND lesson_id = :lesson_id;"""
            query.prepare(update_query)

        # Привязка значений
        query.bindValue(":teacher_id", teacher_id)
        query.bindValue(":lesson_id", lesson_id)

        return execute_query(query)


