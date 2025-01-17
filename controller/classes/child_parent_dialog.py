import logging

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtWidgets import QMessageBox

from controller.classes.person_datas_dialog import PersonDatasDialog
from controller.functions import get_value_with_default, get_document_details, save_cancel_translate
from view.add_child_parent_dialog import Ui_Dialog_ChildParents


class ChildParentDialog(qtw.QDialog, Ui_Dialog_ChildParents):
    def __init__(self, child_person_id=None, selected_child_model=None, selected_parents_model=None):
        super().__init__()
        self.selected_parents_model = selected_parents_model
        self.child_person_id = child_person_id
        self.selected_child_model = selected_child_model
        self.setupUi(self)

        self.setup_connections()
        self.data_load_child_parents()
        save_cancel_translate(self)
        self.create_temp_table()

    def setup_connections(self):
        try:
            if self.child_person_id is not None:
                self.comboBox_ParentStatusName.currentIndexChanged.connect(self.load_parent_document)
            self.pushButton_AddUpdateChildFIO.clicked.connect(self.add_update_child_fio)
        except Exception as e:
            print(f"Error connecting signal: {e}")


    def data_load_child_parents(self):
        if self.child_person_id:
            self.label_ChildFullName.setText(get_value_with_default(self.selected_child_model, 1))
            self.label_ChildDateOfBirth.setText(get_value_with_default(self.selected_child_model, 2))
            self.label_ChildGenderName.setText(get_value_with_default(self.selected_child_model, 3))
            self.label_ChildDocumentData.setText(get_document_details(self.selected_child_model, 10))
            self.label_ChildAgeYears.setText(get_value_with_default(self.selected_child_model, 4))
            self.label_ChildTeamName.setText(get_value_with_default(self.selected_child_model, 8))
            self.label_GroupAgeName.setText(get_value_with_default(self.selected_child_model, 9))
            self.label_ChildRemarks.setText(get_value_with_default(self.selected_child_model, 6))
            self.label_ChildNumberInFamily.setText(get_value_with_default(self.selected_child_model, 18))
            self.label_NumberOfChildren.setText(get_value_with_default(self.selected_child_model, 19))
            self.label_ChildRegAddress.setText(get_value_with_default(self.selected_child_model, 16))
            self.label_ChildFactAddress.setText(get_value_with_default(self.selected_child_model, 17))


            if self.selected_parents_model and self.selected_parents_model.rowCount() > 0:
                for row in range(self.selected_parents_model.rowCount()):
                    parent_status = self.selected_parents_model.data(self.selected_parents_model.index(row, 1))
                    parent_full_name = self.selected_parents_model.data(self.selected_parents_model.index(row, 2))

                    print(f"Parent status: {parent_status}, Parent full name: {parent_full_name}")

                    match parent_status:
                        case 'отец':
                            self.label_FatherFullName.setText(parent_full_name)
                        case 'мать':
                            self.label_MotherFullName.setText(parent_full_name)
                        case _:
                            self.label_RepresentativerFullName.setText(parent_full_name)
            else:
                print("No parents data available")
        else:
            print("No child person selected")

    def load_parent_document(self):
        selected_parents_status_name = self.comboBox_ParentStatusName.currentText()
        print(f"Selected parent status name: {selected_parents_status_name}")


        match selected_parents_status_name:
            case 'отец':
                parent_full_name = self.label_FatherFullName.text()
            case 'мать':
                parent_full_name = self.label_MotherFullName.text()
            case 'законный представитель':
                parent_full_name = self.label_RepresentativerFullName.text()
            case _:
                print("Не выбран статус родителя")
                parent_full_name = '-'
        print(f"Parent full name->  {parent_full_name}")
        self.selected_parents_model.setFilter(f"parent_fio = '{parent_full_name}'")
        self.selected_parents_model.select()
        self.fill_parent_document()
        self.fill_parent_contacts()

    def fill_parent_document(self):
        # Очистка старых данных
        self.label_ParentDocumentData.setText('')

        if self.selected_parents_model.rowCount() > 0:
            document_details = get_document_details(self.selected_parents_model)
            if document_details:
                self.label_ParentDocumentData.setText(document_details)
            else:
                self.label_ParentDocumentData.setText("Документы не найдены")

    def fill_parent_contacts(self):
        self.label_ParentPhone.setText('-')
        self.label_ParentEmail.setText('-')
        self.label_ParentPhone.setText(get_value_with_default(self.selected_parents_model, 5))
        self.label_ParentEmail.setText(get_value_with_default(self.selected_parents_model, 6))
        self.label_ParentRegAddress.setText(get_value_with_default(self.selected_parents_model, 15))
        self.label_ParentFactAddress.setText(get_value_with_default(self.selected_parents_model, 16))
        self.label_ParentRemarks.setText(get_value_with_default(self.selected_parents_model, 7))
        self.label_ParentEducationLevel.setText(get_value_with_default(self.selected_parents_model, 18))
        self.label_ParentPosition.setText(get_value_with_default(self.selected_parents_model, 19))
        self.label_ParentPlaceOfWork.setText(get_value_with_default(self.selected_parents_model, 20))

    def add_update_child_fio(self):
        person_datas = PersonDatasDialog()
        if person_datas.exec() == qtw.QDialog.DialogCode.Accepted:
            logging.debug(f"PersonDatasDialog accepted")
            try:
                self.save_child_parent_data()

            except Exception as e:
                logging.error(f"Failed to save PersonDatasDialog: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить нового воспитанника: {str(e)}")




    def save_child_parent_data(self):
        print("save_child_parent_data")


    def create_temp_table(self):
        print("create_temp_table")
        query = QtSql.QSqlQuery()
        # Удаляем таблицу, если она существует
        if not query.exec("DROP TABLE IF EXISTS temp_table_child_parents;"):
            print(f"Error dropping table: {query.lastError().text()}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления таблицы: {query.lastError().text()}")
            return

        # Создаем новую таблицу
        if not query.exec("""
                CREATE TEMP TABLE temp_table_child_parents (
                    temp_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
                    person_type character varying(4)
                );
            """):
            print(f"Error creating table: {query.lastError().text()}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания таблицы: {query.lastError().text()}")
        else:
            print("Table created successfully")
            QMessageBox.information(self, "Успех", "Таблица создана успешно.")
            if not query.exec("""INSERT INTO temp_table_child_parent_data (person_type) VALUES ('22');"""):
                print(f"Error inserting data into temp table: {query.lastError().text()}")
            else:
                query.exec("""SELECT * FROM temp_table_child_parent_data WHERE person_type = '22';""")
                if query.next():  # Переход к первой записи
                    child_d = query.value(0)  # Получаем значение первого столбца (temp_id)
                    print(f"Data inserted successfully: {child_d=}")
                    return child_d
                else:
                    print("No data found")
                    return None

# """child_last_name TEXT,
#                 child_first_name TEXT,
#                 child_patronymic TEXT,
#                 child_gender_id INTEGER,
#                 child_date_of_birth DATE,
#                 child_snils INTEGER,
#                 person_remarks TEXT,
#                 child_document_type_id INTEGER,
#                 child_citizenship_id INTEGER,
#                 child_place_of_birth TEXT,
#                 child_assembly_record TEXT,
#                 child_document_issued_by TEXT,
#                 child_document_issued_date DATE,
#                 child_document_serie TEXT,
#                 child_document_number TEXT,
#                 child_document_remarks TEXT,
#                 team_id INTEGER,
#                 group_age_id INTEGER,
#                 number_in_family INTEGER,
#                 number_of_children INTEGER"""

        # if not query.exec():
        #     print(f"Error creating temp table: {query.lastError().text()}")
        #     QMessageBox.critical(self, "Ошибка", f"Ошибка создания временной таблицы: {query.lastError().text()}")
        # else:
        #     print("Temp table created successfully")
        #     QMessageBox.information(self, "Успех", "Временная таблица создана успешно.")
        #
            query.prepare("""INSERT INTO temp_table_child_parent_data (person_type) VALUES ('2');""")
            if not query.exec():
                print(f"Error inserting data into temp table: {query.lastError().text()}")
            else:
                print("Data inserted successfully")




    def save_child_data(self):
        print("save_child_data")

    def save_parent_data(self):
        print("save_parent_data")

    def save_child_parent_data(self):
        print("save_child_parent_data")

    def save_child_parent_data(self):
        print("save_child_parent_data")

    def save_child_parent_data(self):
        print("save_child_parent_data")


