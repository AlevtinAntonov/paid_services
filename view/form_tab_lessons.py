# Form implementation generated from reading ui file 'form_tab_lessons.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form_TabLessons(object):
    def setupUi(self, Form_TabLessons):
        Form_TabLessons.setObjectName("Form_TabLessons")
        Form_TabLessons.resize(1204, 832)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form_TabLessons)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_1 = QtWidgets.QFrame(parent=Form_TabLessons)
        self.frame_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.label_15 = QtWidgets.QLabel(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_7.addWidget(self.label_15)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.tableWidget_LessonsInfo = QtWidgets.QTableWidget(parent=self.frame_1)
        self.tableWidget_LessonsInfo.setObjectName("tableWidget_LessonsInfo")
        self.tableWidget_LessonsInfo.setColumnCount(0)
        self.tableWidget_LessonsInfo.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_LessonsInfo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_DeleteLessonInfo = QtWidgets.QPushButton(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_DeleteLessonInfo.setFont(font)
        self.pushButton_DeleteLessonInfo.setObjectName("pushButton_DeleteLessonInfo")
        self.horizontalLayout.addWidget(self.pushButton_DeleteLessonInfo)
        self.pushButton_InsertLessonInfo = QtWidgets.QPushButton(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_InsertLessonInfo.setFont(font)
        self.pushButton_InsertLessonInfo.setObjectName("pushButton_InsertLessonInfo")
        self.horizontalLayout.addWidget(self.pushButton_InsertLessonInfo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.label_19 = QtWidgets.QLabel(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_9.addWidget(self.label_19)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.tableWidget_Teachers = QtWidgets.QTableWidget(parent=self.frame_1)
        self.tableWidget_Teachers.setObjectName("tableWidget_Teachers")
        self.tableWidget_Teachers.setColumnCount(0)
        self.tableWidget_Teachers.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_Teachers)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_DeleteTeacher = QtWidgets.QPushButton(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_DeleteTeacher.setFont(font)
        self.pushButton_DeleteTeacher.setObjectName("pushButton_DeleteTeacher")
        self.horizontalLayout_3.addWidget(self.pushButton_DeleteTeacher)
        self.pushButton_InsertTeacher = QtWidgets.QPushButton(parent=self.frame_1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_InsertTeacher.setFont(font)
        self.pushButton_InsertTeacher.setObjectName("pushButton_InsertTeacher")
        self.horizontalLayout_3.addWidget(self.pushButton_InsertTeacher)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addWidget(self.frame_1)

        self.retranslateUi(Form_TabLessons)
        QtCore.QMetaObject.connectSlotsByName(Form_TabLessons)

    def retranslateUi(self, Form_TabLessons):
        _translate = QtCore.QCoreApplication.translate
        Form_TabLessons.setWindowTitle(_translate("Form_TabLessons", "Form Lessons"))
        self.label_15.setText(_translate("Form_TabLessons", "Кружки"))
        self.pushButton_DeleteLessonInfo.setText(_translate("Form_TabLessons", "Удалить запись"))
        self.pushButton_InsertLessonInfo.setText(_translate("Form_TabLessons", "Добавить запись"))
        self.label_19.setText(_translate("Form_TabLessons", "Преподаватели"))
        self.pushButton_DeleteTeacher.setText(_translate("Form_TabLessons", "Удалить преподавателя"))
        self.pushButton_InsertTeacher.setText(_translate("Form_TabLessons", "Добавить преподавателя"))
