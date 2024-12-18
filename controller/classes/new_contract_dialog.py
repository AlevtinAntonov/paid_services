import logging
from datetime import datetime

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox

from controller.datas.variables import CONTRACT_END_DATE
from controller.functions import get_data_from_db, get_next_contract_number, validate_and_convert_date, execute_query, \
    get_data_id_from_db
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

    def accept(self):
        """ Переопределяем метод accept для проверки обязательных полей. """
        contract_data = self.get_contract_data()

        # Проверка обязательных полей
        if not contract_data['applicant_id'] or not contract_data['child_id'] or not contract_data['lesson_id']:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля.")
            return  # Не закрываем диалог, если обязательные поля не заполнены

        # Если все проверки пройдены, продолжаем с обычным поведением
        super().accept()

    def get_contract_data(self):
        # данные из полей ввода
        applicant_id = get_data_id_from_db('parents', self.comboBox_ContractApplicantDialog.currentText())
        child_id = get_data_id_from_db('children', self.comboBox_ContractChildDialog.currentText())
        lesson_id = get_data_id_from_db('lessons', self.comboBox_ContractLessonsDialog.currentText())
        return {
            'contract_number': int(self.lineEdit_ContractNumberDialog.text()),
            'contract_date': validate_and_convert_date(self.lineEdit_ContractDateDialog.text()),
            'contract_start_date': validate_and_convert_date(self.lineEdit_ContractDateStartDialog.text()),
            'contract_end_date': validate_and_convert_date(self.lineEdit_ContractDateEndDialog.text()),
            'applicant_id': applicant_id,
            'child_id': child_id,
            'lesson_id': lesson_id,
            'contract_remarks':self.lineEdit_ContractRemaksDialog.text()
        }

    def save_new_contract(self):
        """ Обновляет запись контракта в базе данных. """
        contract_data = self.get_contract_data()
        query = QtSql.QSqlQuery()
        query.prepare("""
            INSERT INTO contracts(contract_number, contract_date, contract_start_date, contract_end_date, parent_id, 
            child_id, lesson_id, remarks)
            VALUES (:c_number, :c_date, :c_start_date, :c_end_date, :applicant_id, :child_id, :lesson_id, :remarks);
        """)
        # Привязка значений
        query.bindValue(":c_number", contract_data['contract_number'])
        query.bindValue(":c_date", contract_data['contract_date'])
        query.bindValue(":c_start_date", contract_data['contract_start_date'])
        query.bindValue(":c_end_date", contract_data['contract_end_date'])
        query.bindValue(":applicant_id", contract_data['applicant_id'])
        query.bindValue(":child_id", contract_data['child_id'])
        query.bindValue(":lesson_id", contract_data['lesson_id'])
        query.bindValue(":remarks", contract_data['contract_remarks'])

        # Выполнение запроса и обработка результата
        if not query.exec():
            logging.error(f"Failed to insert record: {query.lastError().text()}")
            QMessageBox.critical(None, "Ошибка", "Не удалось вставить запись:\n" + query.lastError().text())
            return False

        logging.debug("Record insert successfully.")