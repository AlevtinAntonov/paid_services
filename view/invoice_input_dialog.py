# Form implementation generated from reading ui file 'invoice_input_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InvoiceInputDialog(object):
    def setupUi(self, InvoiceInputDialog):
        InvoiceInputDialog.setObjectName("InvoiceInputDialog")
        InvoiceInputDialog.resize(463, 248)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        InvoiceInputDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(InvoiceInputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_InvoiceMonth = QtWidgets.QComboBox(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox_InvoiceMonth.setFont(font)
        self.comboBox_InvoiceMonth.setObjectName("comboBox_InvoiceMonth")
        self.horizontalLayout.addWidget(self.comboBox_InvoiceMonth)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_NumberOfLessons = QtWidgets.QLineEdit(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_NumberOfLessons.setFont(font)
        self.lineEdit_NumberOfLessons.setObjectName("lineEdit_NumberOfLessons")
        self.horizontalLayout_2.addWidget(self.lineEdit_NumberOfLessons)
        spacerItem = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_InvoiceRemarks = QtWidgets.QLineEdit(parent=InvoiceInputDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_InvoiceRemarks.setFont(font)
        self.lineEdit_InvoiceRemarks.setObjectName("lineEdit_InvoiceRemarks")
        self.horizontalLayout_3.addWidget(self.lineEdit_InvoiceRemarks)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=InvoiceInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InvoiceInputDialog)
        self.buttonBox.accepted.connect(InvoiceInputDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(InvoiceInputDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(InvoiceInputDialog)

    def retranslateUi(self, InvoiceInputDialog):
        _translate = QtCore.QCoreApplication.translate
        InvoiceInputDialog.setWindowTitle(_translate("InvoiceInputDialog", "Введите новую квитанцию"))
        self.label.setText(_translate("InvoiceInputDialog", "Выберите месяц*"))
        self.label_2.setText(_translate("InvoiceInputDialog", "Введите количество занятий*"))
        self.label_3.setText(_translate("InvoiceInputDialog", "Примечание (не обязательно)"))
