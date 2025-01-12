from PyQt6 import QtWidgets as qtw
from PyQt6.QtGui import QIntValidator

from controller.functions import get_data_id_from_db, get_data_from_db, save_cancel_translate
from view.add_new_lesson_dialog import Ui_AddNewLesson


class AddNewLessonDialog(qtw.QDialog, Ui_AddNewLesson):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

        self.lineEdit_LessonRate.setValidator(QIntValidator(0, 9999, self))
        self.lineEdit_LessonPerYear.setValidator(QIntValidator(0, 365, self))

        save_cancel_translate(self)

    def load_data(self):
        building_numbers = get_data_from_db('buildings')

        # Заполняем комбобоксы
        self.comboBox_BuildingNumber.addItems(building_numbers)

    def get_data(self):
        building_id = get_data_id_from_db('buildings',self.comboBox_BuildingNumber.currentText())
        return (self.lineEdit_LessonName.text(), building_id, self.lineEdit_LessonRate.text(),
                self.lineEdit_LessonPerYear.text())