# Form implementation generated from reading ui file 'add_new_lesson_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddNewLesson(object):
    def setupUi(self, AddNewLesson):
        AddNewLesson.setObjectName("AddNewLesson")
        AddNewLesson.resize(454, 235)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        AddNewLesson.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AddNewLesson)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=AddNewLesson)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_LessonName = QtWidgets.QLineEdit(parent=AddNewLesson)
        self.lineEdit_LessonName.setObjectName("lineEdit_LessonName")
        self.horizontalLayout.addWidget(self.lineEdit_LessonName)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=AddNewLesson)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox_BuildingNumber = QtWidgets.QComboBox(parent=AddNewLesson)
        self.comboBox_BuildingNumber.setObjectName("comboBox_BuildingNumber")
        self.horizontalLayout_2.addWidget(self.comboBox_BuildingNumber)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=AddNewLesson)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_LessonRate = QtWidgets.QLineEdit(parent=AddNewLesson)
        self.lineEdit_LessonRate.setObjectName("lineEdit_LessonRate")
        self.horizontalLayout_3.addWidget(self.lineEdit_LessonRate)
        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=AddNewLesson)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_LessonPerYear = QtWidgets.QLineEdit(parent=AddNewLesson)
        self.lineEdit_LessonPerYear.setObjectName("lineEdit_LessonPerYear")
        self.horizontalLayout_4.addWidget(self.lineEdit_LessonPerYear)
        self.horizontalLayout_4.setStretch(0, 4)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.button_box = QtWidgets.QDialogButtonBox(parent=AddNewLesson)
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AddNewLesson)
        self.button_box.accepted.connect(AddNewLesson.accept) # type: ignore
        self.button_box.rejected.connect(AddNewLesson.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddNewLesson)

    def retranslateUi(self, AddNewLesson):
        _translate = QtCore.QCoreApplication.translate
        AddNewLesson.setWindowTitle(_translate("AddNewLesson", "Новый кружок"))
        self.label_2.setText(_translate("AddNewLesson", "Ведите название кружка"))
        self.label.setText(_translate("AddNewLesson", "Выберите номер здания"))
        self.label_3.setText(_translate("AddNewLesson", "Введите стоимость одного занятия в рублях"))
        self.label_4.setText(_translate("AddNewLesson", "Введите количесвто занятий в год"))
