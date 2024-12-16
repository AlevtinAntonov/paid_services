from datetime import datetime

from PyQt6 import QtWidgets as qtw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

from controller.datas.variables import CONTRACT_END_DATE
from controller.functions import get_data_from_db, get_next_contract_number, validate_and_convert_date
from view.new_contract_dialog import Ui_DialogAddNewContract


class ContractDialog(qtw.QDialog, Ui_DialogAddNewContract):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data_load_new_contract()

        # Подключаем событие для проверки ввода в lineEdit_ContractNumberDialog
        self.lineEdit_ContractNumberDialog.setValidator(QIntValidator(0, 999999, self))  # Проверка на ввод только чисел

        # Список комбобоксов для простоты доступа
        self.combo_boxes = [
            self.lineEdit_ContractNumberDialog,
            self.lineEdit_ContractDateDialog,
            self.lineEdit_ContractDateStartDialog,
            self.lineEdit_ContractDateEndDialog,
            self.comboBox_ContractApplicantDialog,
            self.comboBox_ContractChildDialog,
            self.comboBox_ContractLessonsDialog,
            self.lineEdit_ContractRemaksDialog,
        ]
        self.current_index = 0  # Индекс текущего комбобокса

    def keyPressEvent(self, event):
        """ Обрабатывает нажатия клавиш. """
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.on_enter_pressed()

    def on_enter_pressed(self):
        """ Обрабатывает переход к следующему комбобоксу при нажатии 'Enter'. """
        if self.current_index < len(self.combo_boxes) - 1:
            # Переходим к следующему комбобоксу
            self.current_index += 1
            self.combo_boxes[self.current_index].setFocus()  # Устанавливаем фокус на следующий комбобокс


    def data_load_new_contract(self):
        """ Загружает данные выбранного контракта и обновляет соответствующие поля. """
        self.lineEdit_ContractNumberDialog.setText(str(get_next_contract_number()))
        self.lineEdit_ContractDateDialog.setText(validate_and_convert_date(str(datetime.now().strftime('%d.%m.%Y'))))
        self.lineEdit_ContractDateStartDialog.setText(validate_and_convert_date(str(datetime.now().strftime('%d.%m.%Y'))))
        self.lineEdit_ContractDateEndDialog.setText(validate_and_convert_date(CONTRACT_END_DATE))

        # Получаем данные из базы
        parents_fio = get_data_from_db('parents')
        child_fio = get_data_from_db('children')
        lesson_names = get_data_from_db('lessons')

        # Заполняем комбобоксы
        self.comboBox_ContractApplicantDialog.addItem("")  # Заполняем комбобокс списка родителей
        self.comboBox_ContractApplicantDialog.addItems(parents_fio)  # Заполняем комбобокс списка родителей
        self.comboBox_ContractChildDialog.addItem("")  # Заполняем комбобокс списка детей
        self.comboBox_ContractChildDialog.addItems(child_fio)  # Заполняем комбобокс списка детей
        self.comboBox_ContractLessonsDialog.addItem("")  # Заполняем комбобокс списка уроков
        self.comboBox_ContractLessonsDialog.addItems(lesson_names)  # Заполняем комбобокс списка уроков

        # Делаем комбобоксы редактируемыми
        self.comboBox_ContractApplicantDialog.setEditable(True)
        self.comboBox_ContractChildDialog.setEditable(True)
        self.comboBox_ContractLessonsDialog.setEditable(True)


    def get_contract_data(self):
        # данные из полей ввода
        return {
            'contract_number': self.lineEdit_ContractNumberDialog.text(),
            'contract_date': validate_and_convert_date(self.lineEdit_ContractDateDialog.text()),
            'contract_start_date': validate_and_convert_date(self.lineEdit_ContractDateStartDialog.text()),
            'contract_end_date': validate_and_convert_date(self.lineEdit_ContractDateEndDialog.text()),
            'contract_applicant': self.comboBox_ContractApplicantDialog.currentText(),
            'contract_child': self.comboBox_ContractChildDialog.currentText(),
            'contract_lesson': self.comboBox_ContractLessonsDialog.currentText(),
            'contract_remarks':self.lineEdit_ContractRemaksDialog.text()
        }