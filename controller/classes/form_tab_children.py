import logging

from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtWidgets import QMessageBox

from controller.functions import setup_table_view, get_selected_id, get_data, get_value_with_default, show_error, \
    update_column_visibility, get_document_details
from controller.setup_tbl_views import setup_tables_views
from view.form_tab_children import Ui_Form_TabChildren


class FormTabChildren(qtw.QWidget, Ui_Form_TabChildren):
    def __init__(self):
        super().__init__()
        self.child_person_id = None
        self.parent_person_id = None
        self.selected_child_model = None
        self.selected_parents_model = None
        self.setupUi(self)

        self.setup_connections()
        self.table_children_data_view()
        self.setup_table_children_data_view()

    def setup_connections(self):
        self.tableWidget_ChildrenData.itemChanged.connect(self.on_item_changed)
        self.tableWidget_ChildrenData.itemSelectionChanged.connect(self.on_child_selected)
        self.tableWidget_ParentsData.itemChanged.connect(self.on_item_changed)
        self.tableWidget_ParentsData.itemSelectionChanged.connect(self.on_parent_selected)

        self.pushButton_InsertChild.clicked.connect(self.add_new_child)
        self.pushButton_DeleteChild.clicked.connect(self.delete_child)
        self.pushButton_DeleteParentData.clicked.connect(self.delete_parent)
        self.pushButton_InsertParentData.clicked.connect(self.add_new_parent)


    def on_item_changed(self, item):
        pass

    def setup_table_children_data_view(self):
        logging.debug('setup_table_children_data_view')
        column_widths = [280, 80, 80, 80, 150, 0, 0, 150, 150, 0, 0, 0, 0, 0, 0,0,0]
        headers = ['ID', 'ФИО\n воспитанника', 'Дата\nрождения', 'Пол', 'Полных\nлет', 'СНИЛС', '', '',
                   'Группа\nназвание', 'Группа\nпо возрасту']
        setup_table_view(self.tableWidget_ChildrenData, column_widths, headers)

    def table_children_data_view(self):
        logging.debug('table_children_data_view')
        self.children_data_view_model = QtSql.QSqlTableModel()
        self.children_data_view_model.setTable('children_data_view')
        setup_tables_views(self.children_data_view_model, self.tableWidget_ChildrenData, columns=[0, 1, 4],
                           slot=self.on_item_changed)

    def on_child_selected(self):
        self.child_person_id = get_selected_id(self.tableWidget_ChildrenData, self.children_data_view_model, 0)

        self.selected_child_model = QtSql.QSqlTableModel(self)
        self.selected_child_model.setTable('children_data_view')
        self.selected_child_model.setFilter(f"person_id = {self.child_person_id}")
        self.selected_child_model.select()
        # print(f'{self.selected_child_model.rowCount()=}')

        if self.selected_child_model.rowCount() > 0:
            logging.debug(f'{self.selected_child_model.rowCount()=}')
            self.load_child_data()
            self.load_parents_data(self.child_person_id)

    def load_child_data(self):
        self.label_ChildDocData.setText(get_document_details(self.selected_child_model, 10))
        self.label_ChildrenRemarks.setText(get_value_with_default(self.selected_child_model, 6))
        self.label_ChildAddressReg.setText(get_value_with_default(self.selected_child_model, 16))
        self.label_ChildAddressFact.setText(get_value_with_default(self.selected_child_model, 17))

    def load_parents_data(self,child_id):
        self.selected_parents_model = QtSql.QSqlTableModel()
        self.selected_parents_model.setTable('parents_data_view')
        self.selected_parents_model.setFilter(f"child_id = {child_id}")
        self.selected_parents_model.select()

        if self.selected_parents_model.rowCount() > 0:
            logging.debug(f'{self.selected_parents_model.rowCount()=}')
            self.table_parents_data_view()
            self.setup_table_parents_data_view()
            self.parent_document()
            self.label_ParentAddressReg.setText(get_value_with_default(self.selected_parents_model, 15))
            self.label_ParentAddressFact.setText(get_value_with_default(self.selected_parents_model, 16))
        else:
            # Очистка старых данных
            self.table_parents_data_view()
            self.setup_table_parents_data_view()
            self.label_ParentPassportData.setText('')
            self.label_ParentAddressReg.setText('')
            self.label_ParentAddressFact.setText('')

    def setup_table_parents_data_view(self):
        logging.debug('setup_table_parents_data_view')
        column_widths = [60, 200, 80, 70, 90, 90, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        headers = ['ID', 'Степень\nродства', 'ФИО\nродителя', 'Дата\nрождения', 'Пол', 'Телефон', 'Email', 'Примечание']
        setup_table_view(self.tableWidget_ParentsData, column_widths, headers)

    def table_parents_data_view(self):
        logging.debug('table_parents_data_view')
        setup_tables_views(self.selected_parents_model, self.tableWidget_ParentsData, columns=[0, 1, 2],
                           slot=self.on_parent_selected)

    def on_parent_selected(self):
        selected_items = self.tableWidget_ParentsData.selectedItems()
        if selected_items:
            self.parent_person_id = get_selected_id(self.tableWidget_ParentsData, self.selected_parents_model, 0)
            print(f'on_parent_selected {self.parent_person_id=}')
        else:
            print('Нет выделенных элементов в таблице родителей')

    def parent_document(self):
        # Очистка старых данных
        self.label_ParentPassportData.setText('')
        self.label_ParentPassportData.setText(get_document_details(self.selected_parents_model))

    def add_new_child(self):
        pass
        # if not self.child_person_id:
        #     show_error('Не выбран ребенок для удаления')
        #     # QMessageBox.warning(None, "Предупреждение", "Сначала выберите воспитанника.")
        #     return

    def delete_person(self, is_child=True):
        person_type = "Ребенок" if is_child else "Родитель"
        person_id = self.child_person_id if is_child else self.parent_person_id
        model = self.selected_child_model if is_child else self.selected_parents_model
        if not person_id:
            show_error(f'{person_type} не выбран для удаления')
            return

        person_name = get_value_with_default(model, 1 if is_child else 2)  # Получаем ФИО в зависимости от типа
        msg_box = QMessageBox(None)
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText(f"{person_type} -> Удалить {person_name}?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Устанавливаем текст кнопок
        msg_box.button(QMessageBox.StandardButton.Yes).setText("Да")
        msg_box.button(QMessageBox.StandardButton.No).setText("Нет")

        # Показать диалог
        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            # Логика удаления
            person_type_name = "воспитанника" if is_child else "родителя"
            print(f'Удаление {person_type_name} {person_name}')
            update_column_visibility("persons", "person_id", person_id)

            # Очистка идентификатора и обновление соответствующего вида
            if is_child:
                self.child_person_id = None
                self.table_children_data_view()
            else:
                self.parent_person_id = None
                self.table_parents_data_view()

    # Вызываем delete_person в соответствующих методах
    def delete_child(self):
        self.delete_person(is_child=True)

    def delete_parent(self):
        self.delete_person(is_child=False)

    def add_new_parent(self):
        pass


