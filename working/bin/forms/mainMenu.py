#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  theme and sys for linking signals
import sys

#  other forms
import managerMenu as managermenu
import staffForm as staffform
import stockForm as stockform
import treatmentsForm as treatmentsform
import appointmentForm as appointmentform
import chartForm as chartform
import customerForm as customerform


#  GUI libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, QObject

# Theme
import qdarkstyle

class Ui_MainMenu(QMainWindow, QObject):

    valueChange = pyqtSignal(int)

    def setupUi(self, MainMenu):
        #  'global' information
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainMenu.sizePolicy().hasHeightForWidth())
        MainMenu.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainMenu)
        self.centralWidget.setObjectName("centralWidget")

        #  True is manager
        #  False is staff
        if sys.argv[2] == 'True':
            self.accessLevel = True
        else:
            self.accessLevel = False

        self.userLoggedIn = sys.argv[1]

        #  creating navigation buttons
        def navButtons(self):
            self.navManagerMenu = QtWidgets.QPushButton(self.centralWidget)
            self.navManagerMenu.setGeometry(QtCore.QRect(11, 40, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navManagerMenu.setFont(font)
            self.navManagerMenu.setObjectName("navManagerMenu")
            self.navManagerMenu.setEnabled(self.accessLevel)
        
            self.navCharts = QtWidgets.QPushButton(self.centralWidget)
            self.navCharts.setGeometry(QtCore.QRect(10, 240, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navCharts.setFont(font)
            self.navCharts.setObjectName("navCharts")
        
            self.navAppointments = QtWidgets.QPushButton(self.centralWidget)
            self.navAppointments.setGeometry(QtCore.QRect(10, 160, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navAppointments.setFont(font)
            self.navAppointments.setObjectName("navAppointments")
        
            self.navCustomers = QtWidgets.QPushButton(self.centralWidget)
            self.navCustomers.setGeometry(QtCore.QRect(10, 120, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navCustomers.setFont(font)
            self.navCustomers.setObjectName("navCustomers")

            self.navStaff = QtWidgets.QPushButton(self.centralWidget)
            self.navStaff.setGeometry(QtCore.QRect(10, 80, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navStaff.setFont(font)
            self.navStaff.setObjectName("navStaff")
            self.navStaff.setEnabled(self.accessLevel)
        
            self.navStock = QtWidgets.QPushButton(self.centralWidget)
            self.navStock.setGeometry(QtCore.QRect(10, 200, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navStock.setFont(font)
            self.navStock.setObjectName("navStock")

            self.navTreatments = QtWidgets.QPushButton(self.centralWidget)
            self.navTreatments.setGeometry(QtCore.QRect(10, 280, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.navTreatments.setFont(font)
            self.navTreatments.setObjectName("navTreatments")

            #  whos logged in
            self.user = QtWidgets.QLabel(self.centralWidget)
            self.user.setGeometry(QtCore.QRect(10, 320, 121, 29))
            font = QtGui.QFont()
            font.setFamily("Arial Black")
            self.user.setFont(font)
            self.user.setObjectName("user")
        
            self.label = QtWidgets.QLabel(self.centralWidget)
            self.label.setGeometry(QtCore.QRect(10, 11, 101, 17))
            font = QtGui.QFont()
            font.setFamily("Arial Black")
            self.label.setFont(font)
            self.label.setObjectName("label")
        
            self.stackedWidget = QtWidgets.QStackedWidget(self.centralWidget)
            self.stackedWidget.setGeometry(QtCore.QRect(140, 10, 1141, 691))
            font = QtGui.QFont()
            font.setFamily("Arial")
            self.stackedWidget.setFont(font)
            self.stackedWidget.setObjectName("stackedWidget")

        #  creation code
        navButtons(self)
        
        managermenu.createManagerMenu(self)
        chartform.createChartForm(self)
        staffform.createStaffForm(self)
        customerform.createCustomerForm(self)
        appointmentform.createAppointmentForm(self)
        stockform.createStockForm(self)
        treatmentsform.createTreatmentsForm(self)
        
        #  main window config
        MainMenu.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainMenu)
        self.mainToolBar.setObjectName("mainToolBar")
        MainMenu.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainMenu)
        self.statusBar.setObjectName("statusBar")
        MainMenu.setStatusBar(self.statusBar)
                
        self.retranslateUi(MainMenu)
        if self.accessLevel is True:
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.stackedWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def navigation(self):
        #  connecting the navigation buttons to the stacked widget
        self.navManagerMenu.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.navCharts.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.navStaff.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        self.navCustomers.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(3))
        self.navAppointments.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))
        self.navStock.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(5))
        self.navTreatments.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(6))
    
    def retranslateUi(self, MainMenu):
        #  adding text to all the labels
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "MainMenu"))
        self.navManagerMenu.setText(_translate("MainMenu", "ManagerMenu"))
        self.navCharts.setText(_translate("MainMenu", "Charts"))
        self.navAppointments.setText(_translate("MainMenu", "Appointments"))
        self.navCustomers.setText(_translate("MainMenu", "Customers"))
        self.navStaff.setText(_translate("MainMenu", "Staff"))
        self.navStock.setText(_translate("MainMenu", "Stock"))
        self.navTreatments.setText(_translate("MainMenu", "Treatments"))
        self.label.setText(_translate("MainMenu", "Navigation"))
        self.label_5.setText(_translate("MainMenu", "Manager Menu"))
        self.label_notifications.setText(_translate("MainMenu", "Notifications"))
        self.label_7.setText(_translate("MainMenu", "Backup"))
        self.btnBackup.setText(_translate("MainMenu", "Backup"))
        self.user.setText(_translate("MainMenu", sys.argv[1]))
        self.user.setAlignment(QtCore.Qt.AlignCenter)

        self.label_4.setText(_translate("MainMenu", "To"))
        self.label_2.setText(_translate("MainMenu", "Chart Type"))
        self.cmbChartType.setItemText(0, _translate("MainMenu", "Most popular treatment"))
        self.cmbChartType.setItemText(1, _translate("MainMenu", "Income"))
        self.cmbChartType.setItemText(2, _translate("MainMenu", "Outgoing per stock type"))
        self.label_3.setText(_translate("MainMenu", "From"))
        self.btnChartCreate.setText(_translate("MainMenu", "Create"))
        self.label_31.setText(_translate("MainMenu", "Charts"))
        self.label_8.setText(_translate("MainMenu", "Staff Menu"))
        self.label_9.setText(_translate("MainMenu", "Add new staff member"))
        self.label_10.setText(_translate("MainMenu", "First name"))
        self.label_staffsex.setText(_translate("MainMenu", "Staff sex"))
        self.label_11.setText(_translate("MainMenu", "Surname"))
        self.label_12.setText(_translate("MainMenu", "Username"))
        self.label_13.setText(_translate("MainMenu", "Password"))
        self.label_14.setText(_translate("MainMenu", "Is this user a manager?"))
        self.checkBoxAdmin.setText(_translate("MainMenu", "Yes"))
        self.label_15.setText(_translate("MainMenu", "Date of birth"))
        self.label_16.setText(_translate("MainMenu", "StaffID"))
        self.btnSaveStaff.setText(_translate("MainMenu", "Save"))
        self.label_17.setText(_translate("MainMenu", "Search"))
        self.btnStaffCancel.setText(_translate("MainMenu", "Cancel"))
        self.label_18.setText(_translate("MainMenu", "Add new Customer"))
        self.label_19.setText(_translate("MainMenu", "Email"))
        self.label_20.setText(_translate("MainMenu", "Surname"))
        self.label_21.setText(_translate("MainMenu", "Search"))
        self.label_22.setText(_translate("MainMenu", "CustomerID"))
        self.btnSaveCustomer.setText(_translate("MainMenu", "Save"))
        self.label_23.setText(_translate("MainMenu", "Date of birth"))
        self.label_24.setText(_translate("MainMenu", "Primary Contact info"))
        self.label_25.setText(_translate("MainMenu", "Phone Number"))
        self.label_26.setText(_translate("MainMenu", "First name"))
        self.cmbCustomerContact.setItemText(0, _translate("MainMenu", "Phone number"))
        self.cmbCustomerContact.setItemText(1, _translate("MainMenu", "Email address"))
        self.label_27.setText(_translate("MainMenu", "Address"))
        self.label_28.setText(_translate("MainMenu", "Postcode"))
        self.label_29.setText(_translate("MainMenu", "Allergies"))
        self.label_30.setText(_translate("MainMenu", "Customers"))
        self.cmbCustomerSex.setItemText(0, _translate("MainMenu", "Male"))
        self.cmbCustomerSex.setItemText(1, _translate("MainMenu", "Female"))
        self.label_75.setText(_translate("MainMenu", "Sex"))
        self.btnCustomerCancel.setText(_translate("MainMenu", "Cancel"))
        self.label_62.setText(_translate("MainMenu", "Search"))
        self.label_63.setText(_translate("MainMenu", "Date"))
        self.label_65.setText(_translate("MainMenu", "AppointmentID"))
        self.label_66.setText(_translate("MainMenu", "Customer"))
        self.label_67.setText(_translate("MainMenu", "Add new Appointment"))
        self.label_68.setText(_translate("MainMenu", "Amount Paid"))
        self.label_70.setText(_translate("MainMenu", "Time"))
        self.btnSaveAppointment.setText(_translate("MainMenu", "Save"))
        self.label_72.setText(_translate("MainMenu", "Treatment"))
        self.label_73.setText(_translate("MainMenu", "Staff"))
        self.label_74.setText(_translate("MainMenu", "Appointments"))
        self.label_64.setText(_translate("MainMenu", "£"))
        self.label_69.setText(_translate("MainMenu", "£"))
        self.label_71.setText(_translate("MainMenu", "Amount Due"))
        self.btnAppointmentCancel.setText(_translate("MainMenu", "Cancel"))
        self.label_76.setText(_translate("MainMenu", "Comment"))
        self.label_77.setText(_translate("MainMenu", "Stock alert level"))
        self.label_78.setText(_translate("MainMenu", "Add new Stock"))
        self.label_81.setText(_translate("MainMenu", "StockID"))
        self.btnSaveStock.setText(_translate("MainMenu", "Save"))
        self.label_83.setText(_translate("MainMenu", "Amount left"))
        self.label_84.setText(_translate("MainMenu", "Name"))
        self.label_86.setText(_translate("MainMenu", "Search"))
        self.btnStockCancel.setText(_translate("MainMenu", "Cancel"))
        self.label_87.setText(_translate("MainMenu", "£"))
        self.label_88.setText(_translate("MainMenu", "Price"))
        self.label_89.setText(_translate("MainMenu", "Stock"))

        #  labels for treatmentsform
        self.label_90.setText(_translate("MainMenu", "£"))
        self.label_91.setText(_translate("MainMenu", "Search"))
        self.label_92.setText(_translate("MainMenu", "Price"))
        self.label_79.setText(_translate("MainMenu", "Stock amount to use"))
        self.label_80.setText(_translate("MainMenu", "Add new Treatments"))
        self.label_85.setText(_translate("MainMenu", "Name"))
        self.label_82.setText(_translate("MainMenu", "TreatmentID"))
        self.label_93.setText(_translate("MainMenu", "Stock name"))
        self.btnTreatmentCancel.setText(_translate("MainMenu", "Cancel"))
        self.btnSaveTreatment.setText(_translate("MainMenu", "Save"))
        self.btnTreatmentAddStock.setText(_translate("MainMenu", "Add"))
        self.label_94.setText(_translate("MainMenu", "Stock to use"))
        self.label_95.setText(_translate("MainMenu", "Treatments"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    MainMenu = QtWidgets.QMainWindow()

    ui = Ui_MainMenu()
    ui.setupUi(MainMenu)
    ui.navigation()

    icon = QtGui.QIcon('database/company.png')
    MainMenu.setWindowIcon(QtGui.QIcon(icon))
    MainMenu.show()
    sys.exit(app.exec_())

