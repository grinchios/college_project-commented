#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QMainWindow

import sys
import os

from bin import encryption
from bin import fileHandling
from bin import validation

import qdarkstyle
'''
S1
A secure and encrypted login system will be used before viewing the system. This includes hashing passwords on input and checking against the correct ones.
S2
All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
I4
ID will be automatically entered to avoid errors
P2
When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
P9
On sign in the passwords will be hashed and checked against the correct ones.
'''


class Ui_login(QMainWindow):
    def __init__(self, login, parent=None):
        super(Ui_login, self).__init__(parent)
        self.setupUi(login)
        self.staffFile = fileHandling.fileHandling('database/staff.json')

    def onSigninClick(self):
        #  encrypting password
		'''
		S1
		A secure and encrypted login system will be used before viewing the system. This includes hashing passwords on input and checking against the correct ones.
		'''
        self.encrypt = encryption.msws(self.txtPassword.text())
		
		'''
		P9
		On sign in the passwords will be hashed and checked against the correct ones.
		'''
		
        for i in range(len(self.txtPassword.text())):
            password = str(self.encrypt.msws())
            
        #  initialisation of variables
        username = self.txtUsername.text()
        staffFile = self.staffFile.readFile()
        signin = False
        
        #  linear search the file for matching username and password
        i = 0
        while i < len(staffFile['data']):
            if username == staffFile['data'][i][str(list(staffFile['data'][i].keys())[0])]['username']:
                if password == staffFile['data'][i][str(list(staffFile['data'][i].keys())[0])]['password']['password']:
                    signin = True
                    accessLevel = staffFile['data'][i][str(list(staffFile['data'][i].keys())[0])]['password']['admin']
                    
            i += 1
            
        #  looks for the mainmenu and executes it
        #  can pass information via command line
        if signin is True:
            username = self.txtUsername.text()
            os.system('./bin/forms/mainMenu.py ' + username + ' ' + str(accessLevel))
        else:
            QMessageBox.about(self, "Error", "Incorrect username or password")
                
    def onCancelClick(self):
        self.txtUsername.setText('')
        self.txtPassword.setText('')
        
        QMessageBox.about(self, "Cancel", "Sign in cancelled")
        
    def onCreateUserClick(self):
        #  error if the username already exists
        passResponse = validation.validate.checkPresence(self.txtNewUsername.text(), self.staffFile.readFile())
        if passResponse is not True: QMessageBox.about(self, "Error", passResponse); return None

        #  password validation
        passResponse = validation.validate.valPassword(self.txtNewPassword.text(), self.txtNewCheckPassword.text())
        if passResponse is not True: QMessageBox.about(self, "Error", passResponse); return None

        passResponse = validation.validate.checkPresence(self.txtNewUsername.text(), 'Username')
        if passResponse is not True: QMessageBox.about(self, "Error", passResponse); return None

        #  ran if password is valid
        #  reinitalises the encryption class with the seed
        self.encrypt = encryption.msws(self.txtNewPassword.text())

        #  generates a hash len amount of times
        #  this is for security and consistency
		'''
		S1
		A secure and encrypted login system will be used before viewing the system. This includes hashing passwords on input and checking against the correct ones.
		'''
        for i in range(len(self.txtNewPassword.text())):
            passEncrypted = str(self.encrypt.msws())

        #  creates dictionary for json file
		'''
		S2
		All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
		'''
		'''
		I4
		ID will be automatically entered to avoid errors
		'''
		'''
		P2
		When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
		'''
        arrUser = {
            self.staffFile.newID(): {
                'name': '',
                'surname': '',
                'sex': True,
                'username': self.txtNewUsername.text(),
                'password': {
                    'password': passEncrypted,
                    'admin': False
                },
                'dob': '2000-01-01'
            }}

        #  moving the file contents to main memory
        self.staffFile.openFile()

        #  then write to the file (append)
        self.staffFile.writeToFile(arrUser)

        #  pretty print debugging
        #            self.staffFile.printFile()

        #  msgbox to say new user made
        QMessageBox.about(self, "New user", "Added new user")

    def moderator(self):
        os.system('./bin/forms/mainMenu.py Moderator True')
        self.destroy()

    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(645, 244)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login.sizePolicy().hasHeightForWidth())
        login.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        login.setFont(font)
        
        self.centralWidget = QtWidgets.QWidget(login)
        self.centralWidget.setObjectName("centralWidget")
        
        self.btnLogin = QtWidgets.QPushButton(self.centralWidget)
        self.btnLogin.setGeometry(QtCore.QRect(23, 160, 101, 29))
        self.btnLogin.setObjectName("btnLogin")
        
        self.btnLoginCancel = QtWidgets.QPushButton(self.centralWidget)
        self.btnLoginCancel.setGeometry(QtCore.QRect(130, 160, 101, 29))
        self.btnLoginCancel.setObjectName("btnLoginCancel")

        self.btnLoginSkip = QtWidgets.QPushButton(self.centralWidget)
        self.btnLoginSkip.setGeometry(QtCore.QRect(23, 120, 101, 29))
        self.btnLoginSkip.setObjectName("btnLoginSkip")
        
        self.btnCreateUser = QtWidgets.QPushButton(self.centralWidget)
        self.btnCreateUser.setGeometry(QtCore.QRect(310, 160, 101, 29))
        self.btnCreateUser.setObjectName("btnCreateUser")
        
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 81, 30))
        self.label_4.setObjectName("label_4")
        
        self.txtUsername = QtWidgets.QLineEdit(self.centralWidget)
        self.txtUsername.setGeometry(QtCore.QRect(110, 30, 152, 29))
        self.txtUsername.setObjectName("txtUsername")
        
        self.txtPassword = QtWidgets.QLineEdit(self.centralWidget)
        self.txtPassword.setGeometry(QtCore.QRect(110, 70, 152, 29))
        self.txtPassword.setObjectName("txtPassword")
        
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 81, 30))
        self.label_5.setObjectName("label_5")
        
        self.txtNewPassword = QtWidgets.QLineEdit(self.centralWidget)
        self.txtNewPassword.setGeometry(QtCore.QRect(400, 70, 152, 29))
        self.txtNewPassword.setObjectName("txtNewPassword")
        
        self.txtNewUsername = QtWidgets.QLineEdit(self.centralWidget)
        self.txtNewUsername.setGeometry(QtCore.QRect(400, 30, 152, 29))
        self.txtNewUsername.setObjectName("txtNewUsername")
        
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(310, 30, 81, 30))
        self.label_6.setObjectName("label_6")
        
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(310, 70, 81, 30))
        self.label_7.setObjectName("label_7")
        
        self.txtNewCheckPassword = QtWidgets.QLineEdit(self.centralWidget)
        self.txtNewCheckPassword.setGeometry(QtCore.QRect(400, 110, 152, 29))
        self.txtNewCheckPassword.setObjectName("txtNewCheckPassword")
        
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(310, 110, 81, 30))
        self.label_8.setObjectName("label_8")
        
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(310, 10, 131, 17))
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 171, 17))
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        login.setCentralWidget(self.centralWidget)
        
        self.menuBar = QtWidgets.QMenuBar(login)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 645, 23))
        self.menuBar.setObjectName("menuBar")
        
        self.menuLogin = QtWidgets.QMenu(self.menuBar)
        self.menuLogin.setObjectName("menuLogin")
        
        login.setMenuBar(self.menuBar)
        
        self.mainToolBar = QtWidgets.QToolBar(login)
        self.mainToolBar.setObjectName("mainToolBar")
        
        login.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        
        self.statusBar = QtWidgets.QStatusBar(login)
        self.statusBar.setObjectName("statusBar")
        
        login.setStatusBar(self.statusBar)
        
        self.menuBar.addAction(self.menuLogin.menuAction())
        
        self.btnLogin.clicked.connect(self.onSigninClick)
        self.btnLoginCancel.clicked.connect(self.onCancelClick)
        self.btnCreateUser.clicked.connect(self.onCreateUserClick)
        self.btnLoginSkip.clicked.connect(self.moderator)
        
        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "login"))
        self.btnLogin.setText(_translate("login", "Login"))
        self.btnLoginCancel.setText(_translate("login", "Cancel"))
        self.btnCreateUser.setText(_translate("login", "Create"))
        self.label_4.setText(_translate("login", "Username"))
        self.label_5.setText(_translate("login", "Password"))
        self.label_6.setText(_translate("login", "Username"))
        self.label_7.setText(_translate("login", "Password"))
        self.label_8.setText(_translate("login", "Password"))
        self.label.setText(_translate("login", "Make new user"))
        self.label_2.setText(_translate("login", "Current user sign in"))
        self.menuLogin.setTitle(_translate("login", "Login"))
        self.btnLoginSkip.setText(_translate('login', 'Moderator'))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    login = QtWidgets.QMainWindow()
    ui = Ui_login(login)
    icon = QtGui.QIcon('database/company.png')
    login.setWindowIcon(QtGui.QIcon(icon))
    login.show()
    sys.exit(app.exec_())
