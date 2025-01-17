from PyQt6 import QtWidgets as qtw
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QMessageBox

from controller.functions import save_cancel_translate, validate_and_convert_date, get_data_id_from_db, format_snils, \
    get_data_from_db
from view.add_person_dialog import Ui_Dialog_PersonDatas


class PersonDatasDialog(qtw.QDialog, Ui_Dialog_PersonDatas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        save_cancel_translate(self)
        # Настроим валидатор для lineEdit_PersonSnils
        regex = QRegularExpression(r"^\d{0,11}$")  # Регулярное выражение для 0-11 цифр
        validator = QRegularExpressionValidator(regex, self.lineEdit_PersonSnils)
        self.lineEdit_PersonSnils.setValidator(validator)
        self.load_combobox()

    def load_combobox(self):
        genders_list = get_data_from_db('genders')
        self.comboBox_PersonGenderName.addItem("")
        self.comboBox_PersonGenderName.addItems(genders_list)

    def accept(self):
        """ Переопределяем метод accept для проверки обязательных полей. """
        person_data = self.get_entered_data()
        print(person_data)

        # Проверка обязательных полей
        if person_data['last_name'] in ['', None] or person_data['first_name'] in ['', None] or person_data[
            'date_of_birth'] in ['', None] or person_data['gender_name'] in ['', None]:

            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля.")
            return  # Не закрываем диалог, если обязательные поля не заполнены

        # Если все проверки пройдены, продолжаем с обычным поведением
        super().accept()

    def get_entered_data(self):
        # данные из полей ввода
        gender_id = get_data_id_from_db('genders', self.comboBox_PersonGenderName.currentText())
        return {
            'last_name': self.lineEdit_PersonLastName.text(),
            'first_name': self.lineEdit_PersonFirstName.text(),
            'patronymic': self.lineEdit_PersonPatronymic.text(),
            'date_of_birth': validate_and_convert_date(self.lineEdit_PersonDateOfBirth.text()),
            'gender_name': self.comboBox_PersonGenderName.currentText(),
            'gender_id': gender_id,
            'snils': self.lineEdit_PersonSnils.text(),
            'remarks': self.lineEdit_PersonRemarks.text(),
        }


