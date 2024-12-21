from PyQt6 import QtWidgets as qtw, QtSql

from controller.functions import get_data_from_db, get_data_id_from_db, show_error, execute_query
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
        teacher_id = get_data_id_from_db('teachers', self.comboBox_TeacherChoice.currentText())
        if not teacher_id:
            return show_error("Таких ФИО нет в базе\n проверьте ввод:")
        return teacher_id

    def update_data(self, lesson_id):
        teacher_id = self.get_contract_data()
        query = QtSql.QSqlQuery()
        query.prepare("""UPDATE teachers_lessons SET teacher_id = :teacher_id, lesson_id= :lesson_id WHERE lesson_id = :lesson_id""")

        query.bindValue(":lesson_id", lesson_id)
        query.bindValue(":teacher_id", teacher_id)

        return execute_query(query)


