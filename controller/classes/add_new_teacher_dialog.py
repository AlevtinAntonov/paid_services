from PyQt6 import QtWidgets as qtw
from PyQt6.QtGui import QIntValidator

from controller.functions import get_data_id_from_db, get_data_from_db, show_error, is_valid_email
from view.add_new_teacher_dialog import Ui_AddNewTeacher


class AddNewTeacherDialog(qtw.QDialog, Ui_AddNewTeacher):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()


    def load_data(self):
        gender_name = get_data_from_db('genders')

        # Заполняем комбобоксы
        self.comboBox_Gender.addItems(gender_name)

    def get_data(self):
        self.last_name = self.lineEdit_TeacherLastName.text()
        self.first_name = self.lineEdit_TeacherFirstName.text()
        self.patronymic = self.lineEdit_TeacherPatronymic.text()
        self.gender_id = get_data_id_from_db('genders',self.comboBox_Gender.currentText())
        self.phone = self.lineEdit_TeacherPhone.text()
        self.email = self.lineEdit_TeacherEmail.text()
        return self.last_name, self.first_name, self.patronymic, self.gender_id, self.phone, self.email

    def accept(self):
        phone = self.lineEdit_TeacherPhone.text()
        email = self.lineEdit_TeacherEmail.text()
        """ Переопределяем метод accept для проверки обязательных полей. """
        if phone not in [None, ''] and not (phone.isdigit() and len(phone) == 10):
            show_error("Телефон - должны быть только цифры и их должно быть 10\nНе удалось вставить запись:\n")
            return
        if email not in [None, ''] and not is_valid_email(email):
            show_error("Введён некорректный адрес электронной почты.")
            return

        # Если все проверки пройдены, продолжаем с обычным поведением
        super().accept()