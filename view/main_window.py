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
        MainWindow.resize(924, 699)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_ContractsView = QtWidgets.QWidget()
        self.tab_ContractsView.setObjectName("tab_ContractsView")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_ContractsView)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget_Contracts = QtWidgets.QTableWidget(parent=self.tab_ContractsView)
        self.tableWidget_Contracts.setObjectName("tableWidget_Contracts")
        self.tableWidget_Contracts.setColumnCount(0)
        self.tableWidget_Contracts.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tableWidget_Contracts)
        self.tableView_ContractInfo = QtWidgets.QTableView(parent=self.tab_ContractsView)
        self.tableView_ContractInfo.setObjectName("tableView_ContractInfo")
        self.horizontalLayout_4.addWidget(self.tableView_ContractInfo)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
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
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.tab_ContractsView)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
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
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 26))
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
        icon = QtGui.QIcon.fromTheme("applications-office")
        self.action.setIcon(icon)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/viewmembers.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_2.setIcon(icon)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/aboutqt.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_3.setIcon(icon1)
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
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
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
