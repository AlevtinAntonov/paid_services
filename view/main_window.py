# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1307, 806)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_ContractsView = QtWidgets.QWidget()
        self.tab_ContractsView.setObjectName("tab_ContractsView")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_ContractsView)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_9 = QtWidgets.QLabel(parent=self.tab_ContractsView)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_11.addWidget(self.label_9)
        self.lineEdit_FilterChild = QtWidgets.QLineEdit(parent=self.tab_ContractsView)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.lineEdit_FilterChild.setFont(font)
        self.lineEdit_FilterChild.setObjectName("lineEdit_FilterChild")
        self.horizontalLayout_11.addWidget(self.lineEdit_FilterChild)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.tableWidget_Contracts = QtWidgets.QTableWidget(parent=self.tab_ContractsView)
        self.tableWidget_Contracts.setObjectName("tableWidget_Contracts")
        self.tableWidget_Contracts.setColumnCount(0)
        self.tableWidget_Contracts.setRowCount(0)
        self.horizontalLayout_10.addWidget(self.tableWidget_Contracts)
        self.widget_ContractInfo = QtWidgets.QWidget(parent=self.tab_ContractsView)
        self.widget_ContractInfo.setObjectName("widget_ContractInfo")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_ContractInfo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_ContractNumber = QtWidgets.QLineEdit(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_ContractNumber.setFont(font)
        self.lineEdit_ContractNumber.setObjectName("lineEdit_ContractNumber")
        self.horizontalLayout.addWidget(self.lineEdit_ContractNumber)
        self.label_2 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_ContractDate = QtWidgets.QLineEdit(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_ContractDate.setFont(font)
        self.lineEdit_ContractDate.setObjectName("lineEdit_ContractDate")
        self.horizontalLayout.addWidget(self.lineEdit_ContractDate)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_ContractDateStart = QtWidgets.QLineEdit(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_ContractDateStart.setFont(font)
        self.lineEdit_ContractDateStart.setObjectName("lineEdit_ContractDateStart")
        self.horizontalLayout_2.addWidget(self.lineEdit_ContractDateStart)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_ContractDateEnd = QtWidgets.QLineEdit(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_ContractDateEnd.setFont(font)
        self.lineEdit_ContractDateEnd.setObjectName("lineEdit_ContractDateEnd")
        self.horizontalLayout_4.addWidget(self.lineEdit_ContractDateEnd)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.comboBox_ContractApplicant = QtWidgets.QComboBox(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox_ContractApplicant.setFont(font)
        self.comboBox_ContractApplicant.setObjectName("comboBox_ContractApplicant")
        self.horizontalLayout_6.addWidget(self.comboBox_ContractApplicant)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.comboBox_ContractChild = QtWidgets.QComboBox(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox_ContractChild.setFont(font)
        self.comboBox_ContractChild.setObjectName("comboBox_ContractChild")
        self.horizontalLayout_7.addWidget(self.comboBox_ContractChild)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.comboBox_ContractLessons = QtWidgets.QComboBox(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox_ContractLessons.setFont(font)
        self.comboBox_ContractLessons.setObjectName("comboBox_ContractLessons")
        self.horizontalLayout_8.addWidget(self.comboBox_ContractLessons)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.lineEdit_ContractRemaks = QtWidgets.QLineEdit(parent=self.widget_ContractInfo)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_ContractRemaks.setFont(font)
        self.lineEdit_ContractRemaks.setObjectName("lineEdit_ContractRemaks")
        self.horizontalLayout_9.addWidget(self.lineEdit_ContractRemaks)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.pushButton_SaveContactInfo = QtWidgets.QPushButton(parent=self.widget_ContractInfo)
        self.pushButton_SaveContactInfo.setStyleSheet("")
        self.pushButton_SaveContactInfo.setObjectName("pushButton_SaveContactInfo")
        self.verticalLayout.addWidget(self.pushButton_SaveContactInfo)
        self.horizontalLayout_10.addWidget(self.widget_ContractInfo)
        self.horizontalLayout_10.setStretch(0, 5)
        self.horizontalLayout_10.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_NewContract = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton_NewContract.setObjectName("pushButton_NewContract")
        self.horizontalLayout_3.addWidget(self.pushButton_NewContract)
        self.pushButton_PrintContract = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton_PrintContract.setObjectName("pushButton_PrintContract")
        self.horizontalLayout_3.addWidget(self.pushButton_PrintContract)
        self.pushButton_Close = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.horizontalLayout_3.addWidget(self.pushButton_Close)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget_Payments = QtWidgets.QTableWidget(parent=self.tab_ContractsView)
        self.tableWidget_Payments.setObjectName("tableWidget_Payments")
        self.tableWidget_Payments.setColumnCount(0)
        self.tableWidget_Payments.setRowCount(0)
        self.horizontalLayout_5.addWidget(self.tableWidget_Payments)
        self.tableView_ChildInfo = QtWidgets.QTableView(parent=self.tab_ContractsView)
        self.tableView_ChildInfo.setObjectName("tableView_ChildInfo")
        self.horizontalLayout_5.addWidget(self.tableView_ChildInfo)
        self.horizontalLayout_5.setStretch(0, 3)
        self.horizontalLayout_5.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_ContractsView, "")
        self.tab_Payment = QtWidgets.QWidget()
        self.tab_Payment.setObjectName("tab_Payment")
        self.tabWidget.addTab(self.tab_Payment, "")
        self.tab_Lessons = QtWidgets.QWidget()
        self.tab_Lessons.setObjectName("tab_Lessons")
        self.tabWidget.addTab(self.tab_Lessons, "")
        self.tab_Children = QtWidgets.QWidget()
        self.tab_Children.setObjectName("tab_Children")
        self.tabWidget.addTab(self.tab_Children, "")
        self.tab_Family = QtWidgets.QWidget()
        self.tab_Family.setObjectName("tab_Family")
        self.tabWidget.addTab(self.tab_Family, "")
        self.tab_Parents = QtWidgets.QWidget()
        self.tab_Parents.setObjectName("tab_Parents")
        self.tabWidget.addTab(self.tab_Parents, "")
        self.tab_Teams = QtWidgets.QWidget()
        self.tab_Teams.setObjectName("tab_Teams")
        self.tabWidget.addTab(self.tab_Teams, "")
        self.tab_Dictionary = QtWidgets.QWidget()
        self.tab_Dictionary.setObjectName("tab_Dictionary")
        self.tabWidget.addTab(self.tab_Dictionary, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1307, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_MainWindow = QtWidgets.QToolBar(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar_MainWindow.sizePolicy().hasHeightForWidth())
        self.toolBar_MainWindow.setSizePolicy(sizePolicy)
        self.toolBar_MainWindow.setObjectName("toolBar_MainWindow")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar_MainWindow)
        self.action = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.action.setIcon(icon)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.action_2.setIcon(icon)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.action_3.setIcon(icon)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action)
        self.menu_2.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.toolBar_MainWindow.addSeparator()
        self.toolBar_MainWindow.addAction(self.action)
        self.toolBar_MainWindow.addAction(self.action_2)
        self.toolBar_MainWindow.addAction(self.action_3)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Платные Услуги"))
        self.label_9.setText(_translate("MainWindow", "Фильтр по ФИО ребенка"))
        self.label.setText(_translate("MainWindow", "Договор №"))
        self.label_2.setText(_translate("MainWindow", "от"))
        self.label_3.setText(_translate("MainWindow", "дата начала"))
        self.label_4.setText(_translate("MainWindow", "дата завершения"))
        self.label_5.setText(_translate("MainWindow", "Заказчик"))
        self.label_6.setText(_translate("MainWindow", "Ребенок"))
        self.label_7.setText(_translate("MainWindow", "Кружок"))
        self.label_8.setText(_translate("MainWindow", "Примечание"))
        self.pushButton_SaveContactInfo.setText(_translate("MainWindow", "Сохранить изменения"))
        self.pushButton_NewContract.setText(_translate("MainWindow", "Новый договор"))
        self.pushButton_PrintContract.setText(_translate("MainWindow", "Печать"))
        self.pushButton_Close.setText(_translate("MainWindow", "Выход"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ContractsView), _translate("MainWindow", "Договоры ДУ"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Payment), _translate("MainWindow", "Оплата"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Lessons), _translate("MainWindow", "Кружки"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Children), _translate("MainWindow", "Дети"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Family), _translate("MainWindow", "Семьи"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Parents), _translate("MainWindow", "Родители"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Teams), _translate("MainWindow", "Группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Dictionary), _translate("MainWindow", "Справочники"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Помощь"))
        self.toolBar_MainWindow.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action.setText(_translate("MainWindow", "Открыть"))
        self.action_2.setText(_translate("MainWindow", "Создать"))
        self.action_3.setText(_translate("MainWindow", "О программе"))
