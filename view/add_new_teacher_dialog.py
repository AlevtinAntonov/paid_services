# Form implementation generated from reading ui file 'add_new_teacher_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddNewTeacher(object):
    def setupUi(self, AddNewTeacher):
        AddNewTeacher.setObjectName("AddNewTeacher")
        AddNewTeacher.resize(454, 296)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        AddNewTeacher.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AddNewTeacher)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_TeacherLastName = QtWidgets.QLineEdit(parent=AddNewTeacher)
        self.lineEdit_TeacherLastName.setObjectName("lineEdit_TeacherLastName")
        self.horizontalLayout.addWidget(self.lineEdit_TeacherLastName)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.lineEdit_TeacherFirstName = QtWidgets.QLineEdit(parent=AddNewTeacher)
        self.lineEdit_TeacherFirstName.setObjectName("lineEdit_TeacherFirstName")
        self.horizontalLayout_5.addWidget(self.lineEdit_TeacherFirstName)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.lineEdit_TeacherPatronymic = QtWidgets.QLineEdit(parent=AddNewTeacher)
        self.lineEdit_TeacherPatronymic.setObjectName("lineEdit_TeacherPatronymic")
        self.horizontalLayout_6.addWidget(self.lineEdit_TeacherPatronymic)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox_Gender = QtWidgets.QComboBox(parent=AddNewTeacher)
        self.comboBox_Gender.setObjectName("comboBox_Gender")
        self.horizontalLayout_2.addWidget(self.comboBox_Gender)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_TeacherPhone = QtWidgets.QLineEdit(parent=AddNewTeacher)
        self.lineEdit_TeacherPhone.setObjectName("lineEdit_TeacherPhone")
        self.horizontalLayout_4.addWidget(self.lineEdit_TeacherPhone)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(parent=AddNewTeacher)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.lineEdit_TeacherEmail = QtWidgets.QLineEdit(parent=AddNewTeacher)
        self.lineEdit_TeacherEmail.setObjectName("lineEdit_TeacherEmail")
        self.horizontalLayout_3.addWidget(self.lineEdit_TeacherEmail)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=AddNewTeacher)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AddNewTeacher)
        self.buttonBox.accepted.connect(AddNewTeacher.accept) # type: ignore
        self.buttonBox.rejected.connect(AddNewTeacher.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddNewTeacher)

    def retranslateUi(self, AddNewTeacher):
        _translate = QtCore.QCoreApplication.translate
        AddNewTeacher.setWindowTitle(_translate("AddNewTeacher", "Новый преподаватель"))
        self.label_2.setText(_translate("AddNewTeacher", "Фамилия"))
        self.label_5.setText(_translate("AddNewTeacher", "Имя"))
        self.label_6.setText(_translate("AddNewTeacher", "Отчество"))
        self.label.setText(_translate("AddNewTeacher", "Пол"))
        self.label_4.setText(_translate("AddNewTeacher", "Телефон"))
        self.label_7.setText(_translate("AddNewTeacher", "Электронная почта"))
