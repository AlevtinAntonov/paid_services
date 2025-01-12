import logging

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtWidgets import QMessageBox
from PyQt6.sip import delete

from controller.classes.add_new_lesson_dialog import AddNewLessonDialog
from controller.classes.add_new_teacher_dialog import AddNewTeacherDialog
from controller.classes.delete_dialog import DeleteDialog
from controller.classes.teacher_choice_dialog import TeacherChoiceDialog
from controller.datas.table_info_dict import table_info
from controller.functions import setup_table_view, check_and_convert_to_int, get_data_id_from_db, is_valid_email, \
    show_error, get_selected_id, execute_query, update_visibility, insert_new_lesson, insert_new_teacher, \
    insert_new_record
from controller.setup_tbl_views import setup_tables_views
from view.form_tab_lessons import Ui_Form_TabLessons


class FormTabLessons(qtw.QWidget, Ui_Form_TabLessons):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lesson_id = None
        self.teacher_id = None

        self.setup_connections()
        self.table_view()
        self.setup_table_view()
        self.table_teachers_view()
        self.setup_table_teachers_view()

    def setup_connections(self):
        self.tableWidget_LessonsInfo.itemChanged.connect(self.on_item_changed)
        self.tableWidget_LessonsInfo.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.pushButton_DeleteLessonInfo.clicked.connect(self.delete_lesson)
        self.pushButton_InsertLessonInfo.clicked.connect(self.insert_lesson)

        self.tableWidget_Teachers.itemChanged.connect(self.on_item_changed_teachers)
        self.pushButton_DeleteTeacher.clicked.connect(self.delete_teacher)
        self.pushButton_InsertTeacher.clicked.connect(self.insert_teacher)

    def on_item_changed(self, item):
        self.handle_item_changed(item, 'lessons')

    def on_item_changed_teachers(self, item):
        self.handle_item_changed(item, 'teachers', is_teachers=True)

    def handle_item_changed(self, item, table, is_teachers=False):
        row = item.row()
        column = item.column()
        new_value = item.text()

        if column == 2 and not is_teachers:
            new_value = item.text()

        elif column in [4, 5] and not is_teachers:
            new_value = check_and_convert_to_int(new_value)
            if new_value == 0:
                return show_error("Должны быть только целые числа\n проверьте ввод:"), self.table_view()

        elif column == 3 and not is_teachers:
            new_value = check_and_convert_to_int(new_value)
            self.building_id = get_data_id_from_db('buildings', new_value)
            new_value = self.building_id
            if not self.building_id:
                return show_error("Номер здания состоит из 1 цифры\n и он должен существовать в базе данных\n"
                                  "проверьте ввод:"), self.table_view()

        elif column in [1, 2, 3] and is_teachers:
            new_value = item.text()

        elif column == 4 and is_teachers:
            self.gender_id = get_data_id_from_db('genders', new_value)
            if not self.gender_id:
                return show_error("Пол : мужской или женский\n проверьте ввод:"), self.table_teachers_view()
            new_value = self.gender_id

        elif column == 5 and is_teachers:
            if not (new_value.isdigit() and len(new_value) == 10):
                return (show_error(
                    "Телефон - должны быть только цифры и их должно быть 10\nНе удалось вставить запись:\n"),
                        self.table_teachers_view())

        elif column == 6 and is_teachers:
            if not is_valid_email(new_value):
                return show_error("Введён некорректный адрес электронной почты."), self.table_teachers_view()

        self.update_database(row, column, new_value, table)

    def update_database(self, row, column, new_value, tbl_name):
        try:
            table_info_selected = table_info.get(tbl_name)
            if not table_info_selected:
                logging.error(f"Unknown table name: {tbl_name}")
                return

            column_id = table_info_selected['column_id']
            value_id = self.get_value_id(tbl_name, row, table_info_selected['value_id_index'])
            column_map = table_info_selected['column_map']

            column_name = column_map.get(column)
            if column_name is None:
                logging.error(f"Invalid column index: {column}")
                return

            self.execute_update_query(tbl_name, column_name, new_value, column_id, value_id)

        except Exception as e:
            logging.error(f"Ошибка при обновлении базы данных: {e}")

    def execute_update_query(self, tbl_name, column_name, new_value, column_id, value_id):
        """ Выполнить обновление записи в таблице. """
        query = QtSql.QSqlQuery()
        query.prepare(f"UPDATE {tbl_name} SET {column_name} = :value WHERE {column_id} = :id")

        if new_value in [None, ""]:
            query.bindValue(":value", None)  # Устанавливаем NULL в запрос
        else:
            query.bindValue(":value", new_value)

        query.bindValue(":id", value_id)

        if not query.exec():
            logging.error(f"Failed to update record: {query.lastError().text()}")
            return show_error("Не удалось обновить запись:\n" + query.lastError().text())

        logging.debug("Record updated successfully.")

        # Зависит от типа таблицы, можно вызывать разные методы для обновления интерфейса
        if tbl_name == 'lessons':
            self.table_view()
        elif tbl_name == 'teachers':
            self.table_teachers_view()

        return True

    def get_value_id(self, tbl_name, row, value_id_index):
        """ Получить идентификатор записи в зависимости от типа таблицы. """
        if tbl_name == 'lessons':
            return self.lessons_view_model.data(self.lessons_view_model.index(row, value_id_index))
        elif tbl_name == 'teachers':
            return self.teachers_view_model.data(self.teachers_view_model.index(row, value_id_index))
        return None

    def setup_table_view(self):
        column_widths = [0, 300, 100, 100, 100, 300]
        headers = ['ID', 'ID teacher', 'Кружок\nназвание', 'Здание\n№', 'Ставка за\n1 занятие', 'Занятий\nв год',
                   'Педагог\nФИО']
        setup_table_view(self.tableWidget_LessonsInfo, column_widths, headers)

    def table_view(self):
        self.lessons_view_model = QtSql.QSqlTableModel(self)
        self.lessons_view_model.setTable('lessons_info_view')
        setup_tables_views(self.lessons_view_model, self.tableWidget_LessonsInfo, columns=[0, 1, 6, ],
                           slot=self.on_item_changed)

    def setup_table_teachers_view(self):
        column_widths = [200, 200, 200, 150, 150, 200]
        headers = ['ID', 'Педагог\nфамилия', 'Педагог\nимя', 'Педагог\nотчество', 'Пол', 'Телефон', 'Email']
        setup_table_view(self.tableWidget_Teachers, column_widths, headers)

    def table_teachers_view(self):
        self.teachers_view_model = QtSql.QSqlTableModel(self)
        self.teachers_view_model.setTable('teachers_view')
        setup_tables_views(self.teachers_view_model, self.tableWidget_Teachers, columns=[0, ],
                           slot=self.on_item_changed_teachers)

    def on_cell_double_clicked(self, row, column):
        lesson_id = get_selected_id(self.tableWidget_LessonsInfo, self.lessons_view_model, 0)
        if column in [6, ]:  # Проверяем, что это 6 колонка
            dialog_choice = TeacherChoiceDialog()  # Создаем диалог с текущим значением
            if dialog_choice.exec() == qtw.QDialog.DialogCode.Accepted:  # Проверяем, нажал ли пользователь "ОК"
                new_value = dialog_choice.get_contract_data()  # Получаем новое значение из диалога
                if new_value == 'is_visible_set_false':
                    teacher_id = get_selected_id(self.tableWidget_LessonsInfo, self.lessons_view_model, 1)
                    update_visibility(lesson_id, teacher_id)
                elif new_value not in [None, '']:
                    dialog_choice.update_data(lesson_id)
                self.table_view()

    def delete_item(self, data_type: str, table_widget, view_model, id_column: int, name_columns: list):
        item_id = get_selected_id(table_widget, view_model, id_column)
        if not item_id:
            show_error(f"Не выбран {data_type}!")
            return

        item_name_parts = [get_selected_id(table_widget, view_model, col) for col in name_columns]
        full_name = ' '.join(filter(None, item_name_parts))  # Удаляем пустые элементы

        delete_dialog = DeleteDialog(f'Внимание! {data_type}', full_name, 'Будет', 'УДАЛЕН !!!')
        if delete_dialog.exec() == qtw.QDialog.DialogCode.Accepted:
            self.execute_update_query(data_type + 's', 'is_visible', False, f'{data_type}_id', item_id)
            if data_type == 'teacher':
                self.execute_update_query('teachers_lessons', 'is_visible', False, 'teacher_id', item_id)
            self.table_view() if data_type == 'teacher' else None
            logging.debug(f"{data_type.capitalize()} удален!")

    def delete_lesson(self):
        self.delete_item('lesson', self.tableWidget_LessonsInfo, self.lessons_view_model, 0, [2, 3])

    def delete_teacher(self):
        self.delete_item('teacher', self.tableWidget_Teachers, self.teachers_view_model, 0, [1, 2, 3])

    def insert_teacher(self):
        insert_new_record(AddNewTeacherDialog, insert_new_teacher, self.table_teachers_view)

    def insert_lesson(self):
        insert_new_record(AddNewLessonDialog, insert_new_lesson, self.table_view)
