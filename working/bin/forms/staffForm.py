# -*- coding: utf-8 -*-

import sys
sys.path = ['..'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

import fileHandling
from validation import validate
from datetime import date

class staff():

    def __init__(self, ui_class):
        #  starts an object of the filehandling class

        self.file = fileHandling.fileHandling('database/staff.json')

        #  staffSort is what field the table
        #  is sorted by on double click
        self.sortValue = 'id'

        self.fileContent = self.file.readFile()['data']

        self.tableData = self.file.readFile()['data']

        #  sets column titles
        self.columnTitles = ['ID',
                             'Name',
                             'Surname',
                             'Sex',
                             'Username',
                             'Password',
                             'Admin',
                             'DOB']

        #  assigning the ui to a variable for use
        self.ui = ui_class

        #  threaded method to fill the table
        self.makeTable = self.fillTable(self.fileContent, '0', self.file.readFile(), self.ui)

        #  set true on double click
        self.filter = False

        self.startTable()

    def fillFields(self, rowNum):

        self.ui.txtStaffID.setText(str(list(self.tableData[rowNum].keys())[0]))

        self.ui.txtStaffUsername.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['username'])

        self.ui.txtStaffPassword.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['password'][
                'password']))

        self.ui.checkBoxAdmin.setChecked(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['password']['admin'])

        self.ui.txtStaffFirstName.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['name'])

        self.ui.checkBoxStaffSex.setChecked(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['sex'])

        self.ui.txtStaffLastName.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['surname'])

        #  DOB is in this format: 1980-01-01
        #  therefore must be altered for the dateEdit
        dob = self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['dob']
        #  dob[0:4] is year YYYY
        #  dob[5:7] is month MM
        #  dob[8:10] is day DD
        self.ui.dateStaffDOB.setDate(QtCore.QDate(int(dob[0:4])), int(dob[5:7], int(dob[8:10])))

    def search(self):
        if self.filter:
            try:
                searchIndex = self.file.binSearch(
                    self.tableData, self.ui.txtStaffSearch.text(), self.searchTerm)

                self.fillFields(int(searchIndex))

            except TypeError:
                QMessageBox.about(self.ui, "Error", 'Field not found')

        else:
            QMessageBox.about(self.ui, "Error", 'Must double click on a field first to sort by')

    def checkFields(self, newField):
        #  interfacing with validation class

        #  staff name
        val = validate.checkPresence(self.ui.txtStaffFirstName.text(), 'Staff name')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  staff surname
        val = validate.checkPresence(self.ui.txtStaffLastName.text(), 'Staff surname')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  username
        val = validate.checkPresence(self.ui.txtStaffUsername.text(), 'Staff username')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  if the data is new then the date can be checked
        #  relies on the fact that dob and appointment dates
        #  will never or will rarely change
        #  uses the default also since this needs to be changed
        dob = self.ui.dateStaffDOB.date().toPyDate().strftime('%Y-%m-%d')
        if dob == '2000-01-01': QMessageBox.about(self.ui, "Error", 'DOB must be changed'); return False

        if newField is True:
            #  date range 80 years ago to 16 years ago

            low = date.today().strftime('%Y-%m-%d')
            low = str(int(low[:4]) - 80) + low[4:]

            high = date.today().strftime('%Y-%m-%d')
            high = str(int(high[:4]) - 16) + high[4:]

            val = validate.checkRange(dob, low, high)
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        return True

    def saveFunc(self):
        self.fileContent = self.file.readFile()['data']

        if self.filter is True:
            sortedData = self.file.bubblesort(self.columnTitles[self.sortValue].lower())
            self.tableData = sortedData
            self.makeTable.tableContent = sortedData
        else:
            self.fileContent = self.file.readFile()['data']
            self.tableData = self.fileContent
            self.makeTable.tableContent = self.fileContent

        self.makeTable.staffFile = self.file.readFile()
        self.startTable()
        self.staffCancel()

    def saveStaff(self):
        #  activates when save button is pressed
        if self.ui.checkBoxAdmin.isChecked():
            admin = True
        else:
            admin = False

        if self.ui.checkBoxStaffSex.isChecked():
            sex = True
        else:
            sex = False

        ID = int(self.ui.txtStaffID.text())

        if ID != int(self.file.newID()):
            newField = False
        else:
            newField = True

        if self.checkFields(newField) is True:
            #  creates a dictionary of the user for the file
            arrUser = {
                ID: {
                    'name': self.ui.txtStaffFirstName.text(),
                    'surname': self.ui.txtStaffLastName.text(),
                    'sex': sex,
                    'username': self.ui.txtStaffUsername.text(),
                    'password': {
                        'password': self.ui.txtStaffPassword.text(),
                        'admin': admin
                    },
                    'dob': self.ui.dateStaffDOB.date().toPyDate().strftime('%Y-%m-%d')
                }}

            #  if its an old ID thats updated
            #  otherwise it's added to the end
            if ID != int(self.file.newID()):
                self.file.editOneField(arrUser, ID)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been updated')

            else:
                #  will never execute but left as an error catch
                self.file.writeToFile(arrUser)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been added')

            self.ui.valueChange.emit(2)

    def startTable(self):
        self.ui.listStaff.update()

        #  put the file into a variable
        staffFile = self.file.readFile()

        #  row amount
        rowNum = len(staffFile['data'])

        #  sets row and column amounts
        self.ui.listStaff.setRowCount(rowNum)
        self.ui.listStaff.setColumnCount(len(self.columnTitles))
        self.ui.listStaff.setHorizontalHeaderLabels(self.columnTitles)

        self.makeTable.start()

    def staffClick(self):
        #  function allows user to pre fill boxes based on a selected row
        rows = sorted(set(index.row() for index in self.ui.listStaff.selectedIndexes()))

        for row in rows:
            rowNum = int(row)
            self.ui.txtStaffID.setText(str(list(self.tableData[rowNum].keys())[0]))

            self.ui.txtStaffUsername.setText(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['username'])

            self.ui.txtStaffPassword.setText(str(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['password'][
                    'password']))

            self.ui.checkBoxAdmin.setChecked(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['password']['admin'])

            self.ui.txtStaffFirstName.setText(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['name'])

            self.ui.checkBoxStaffSex.setChecked(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['sex'])

            self.ui.txtStaffLastName.setText(
                self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['surname'])

            #  DOB is in this format: 1980-01-01
            #  therefore must be altered for the dateEdit
            dob = self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['dob']
            #  dob[0:4] is year YYYY
            #  dob[5:7] is month MM
            #  dob[8:10] is day DD
            self.ui.dateStaffDOB.setDate(QtCore.QDate(int(dob[0:4]), int(dob[5:7]), int(dob[8:])))

    def staffDoubleClick(self):
        #  allows a column to be selected for sorting and searching
        columns = sorted(set(index.column() for index in self.ui.listStaff.selectedIndexes()))

        for column in columns:
            self.staffColumn = column

        if self.columnTitles[self.staffColumn] == 'ID':
            #  sets to default
            self.tableData = self.file.readFile()['data']
            self.makeTable.setTableContent([], tableFilter=False)
            self.makeTable.staffFile = self.file.readFile()
            self.filter = False

        elif self.columnTitles[self.staffColumn] == 'Password' or self.columnTitles[self.staffColumn] == 'Admin':
            #  sets to default
            self.tableData = self.file.readFile()['data']
            self.makeTable.setTableContent([], tableFilter=False)
            self.makeTable.staffFile = self.file.readFile()
            self.filter = False

        else:
            #  sorts data and displays
            sortedData = self.file.quicksort(self.columnTitles[self.staffColumn].lower())

            self.searchTerm = self.columnTitles[self.staffColumn].lower()
            self.tableData = sortedData
            self.makeTable.setTableContent(sortedData)

            self.filter = True

        self.startTable()

    class fillTable(QThread):
        def __init__(self, content, index, file, ui):
            QThread.__init__(self)
            self.fileContent = content
            self.sortBy = index
            self.tableContent = []
            self.staffFile = file
            self.ui = ui
            self.contentChange = False

        def setTableContent(self, data, tableFilter=True):
            #  changed on double click
            self.tableContent = data
            self.contentChange = tableFilter

        def fillTable(self, data, i):
            #  if table has been double clicked
            if self.contentChange:
                pass
            else:
                #  if it's the first field
                if i == 0:
                    self.tableContent = []
                #  fills the table with data
                self.tableContent.append(data)
            self.ui.listStaff.setItem(i, 0, QtWidgets.QTableWidgetItem(str(list(self.tableContent[i].keys())[0])))

            self.ui.listStaff.setItem(i, 1, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['name']))

            self.ui.listStaff.setItem(i, 2, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['surname']))

            #  converts bool to male or female
            if self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['sex']:
                self.ui.listStaff.setItem(i, 3, QtWidgets.QTableWidgetItem('Female'))

            else:
                self.ui.listStaff.setItem(i, 3, QtWidgets.QTableWidgetItem('Male'))

            self.ui.listStaff.setItem(i, 4, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['username']))

            self.ui.listStaff.setItem(i, 5, QtWidgets.QTableWidgetItem(
                str(self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['password']['password'])))

            self.ui.listStaff.setItem(i, 6, QtWidgets.QTableWidgetItem(
                str(self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['password']['admin'])))

            self.ui.listStaff.setItem(i, 7, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['dob']))

        def run(self):
            #  row amount
            rowNum = len(self.staffFile['data'])
            for i in range(rowNum):
                self.fillTable(self.staffFile['data'][i], i)

            self.ui.listStaff.update()

    def staffCancel(self):
        #  clears significant fields and assigns new ID
        self.ui.txtStaffID.setText(str(self.file.newID()))
        self.ui.txtStaffFirstName.setText('')
        self.ui.txtStaffLastName.setText('')
        self.ui.txtStaffUsername.setText('')
        self.ui.txtStaffPassword.setText('')

#  staff form
def createStaffForm(self):
    
    self.pageStaff = QtWidgets.QWidget()
    self.pageStaff.setObjectName("pageStaff")
    
    self.label_8 = QtWidgets.QLabel(self.pageStaff)
    self.label_8.setGeometry(QtCore.QRect(10, 0, 91, 17))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_8.setFont(font)
    self.label_8.setObjectName("label_8")
    
    self.listStaff = QtWidgets.QTableWidget(self.pageStaff)
    self.listStaff.setGeometry(QtCore.QRect(10, 30, 1111, 351))
    self.listStaff.setObjectName("listStaff")
    self.listStaff.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    self.label_9 = QtWidgets.QLabel(self.pageStaff)
    self.label_9.setGeometry(QtCore.QRect(10, 390, 161, 17))
    self.label_9.setObjectName("label_9")
    
    self.label_10 = QtWidgets.QLabel(self.pageStaff)
    self.label_10.setGeometry(QtCore.QRect(10, 460, 151, 17))
    self.label_10.setObjectName("label_10")
    
    self.txtStaffFirstName = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffFirstName.setGeometry(QtCore.QRect(10, 480, 181, 29))
    self.txtStaffFirstName.setObjectName("txtStaffFirstName")
    
    self.txtStaffLastName = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffLastName.setGeometry(QtCore.QRect(10, 540, 181, 29))
    self.txtStaffLastName.setObjectName("txtStaffLastName")
    
    self.label_11 = QtWidgets.QLabel(self.pageStaff)
    self.label_11.setGeometry(QtCore.QRect(10, 520, 151, 17))
    self.label_11.setObjectName("label_11")
    
    self.txtStaffPassword = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffPassword.setGeometry(QtCore.QRect(230, 540, 181, 29))
    self.txtStaffPassword.setObjectName("txtStaffPassword")
    self.txtStaffPassword.setReadOnly(True)

    self.txtStaffUsername = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffUsername.setGeometry(QtCore.QRect(230, 480, 181, 29))
    self.txtStaffUsername.setObjectName("txtStaffUsername")
    self.txtStaffUsername.setReadOnly(True)
    
    self.label_12 = QtWidgets.QLabel(self.pageStaff)
    self.label_12.setGeometry(QtCore.QRect(230, 460, 151, 17))
    self.label_12.setObjectName("label_12")
    
    self.label_13 = QtWidgets.QLabel(self.pageStaff)
    self.label_13.setGeometry(QtCore.QRect(230, 520, 151, 17))
    self.label_13.setObjectName("label_13")
    
    self.label_14 = QtWidgets.QLabel(self.pageStaff)
    self.label_14.setGeometry(QtCore.QRect(450, 460, 161, 17))
    self.label_14.setObjectName("label_14")
    
    self.checkBoxAdmin = QtWidgets.QCheckBox(self.pageStaff)
    self.checkBoxAdmin.setGeometry(QtCore.QRect(450, 480, 96, 22))
    self.checkBoxAdmin.setObjectName("checkBoxAdmin")
    
    self.dateStaffDOB = QtWidgets.QDateEdit(self.pageStaff)
    self.dateStaffDOB.setGeometry(QtCore.QRect(450, 540, 111, 27))
    self.dateStaffDOB.setCalendarPopup(True)
    self.dateStaffDOB.setObjectName("dateStaffDOB")
    
    self.label_15 = QtWidgets.QLabel(self.pageStaff)
    self.label_15.setGeometry(QtCore.QRect(450, 520, 161, 17))
    self.label_15.setObjectName("label_15")
    
    self.label_16 = QtWidgets.QLabel(self.pageStaff)
    self.label_16.setGeometry(QtCore.QRect(10, 430, 67, 17))
    self.label_16.setObjectName("label_16")
    
    self.txtStaffID = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffID.setGeometry(QtCore.QRect(70, 420, 121, 29))
    self.txtStaffID.setReadOnly(True)
    self.txtStaffID.setObjectName("txtStaffID")

    self.label_staffsex = QtWidgets.QLabel(self.pageStaff)
    self.label_staffsex.setGeometry(QtCore.QRect(230, 420, 161, 17))
    self.label_staffsex.setObjectName("label_staffsex")

    self.checkBoxStaffSex = QtWidgets.QCheckBox(self.pageStaff)
    self.checkBoxStaffSex.setGeometry(QtCore.QRect(300, 420, 96, 22))
    self.checkBoxStaffSex.setObjectName("checkBoxStaffSex")
    self.checkBoxStaffSex.setToolTip("Select for female, leave unselected for male")

    self.btnSaveStaff = QtWidgets.QPushButton(self.pageStaff)
    self.btnSaveStaff.setGeometry(QtCore.QRect(10, 590, 101, 29))
    self.btnSaveStaff.setObjectName("btnSaveStaff")
    
    self.label_17 = QtWidgets.QLabel(self.pageStaff)
    self.label_17.setGeometry(QtCore.QRect(670, 400, 67, 17))
    self.label_17.setObjectName("label_17")
    
    self.txtStaffSearch = QtWidgets.QLineEdit(self.pageStaff)
    self.txtStaffSearch.setGeometry(QtCore.QRect(750, 390, 371, 29))
    self.txtStaffSearch.setObjectName("txtStaffSearch")
    
    self.btnStaffCancel = QtWidgets.QPushButton(self.pageStaff)
    self.btnStaffCancel.setGeometry(QtCore.QRect(120, 590, 101, 29))
    self.btnStaffCancel.setObjectName("btnStaffCancel")
    
    self.stackedWidget.addWidget(self.pageStaff)

    #  starts an object of the staff class for less globals
    staffClass = staff(self)
    
    #  restarts form
    staffClass.staffCancel()
    
    #  connects a click on the table to the select the row
    self.listStaff.clicked.connect(lambda : staffClass.staffClick())
    self.listStaff.doubleClicked.connect(lambda : staffClass.staffDoubleClick())

    #  connecting the buttons
    self.btnStaffCancel.clicked.connect(lambda : staffClass.staffCancel())
    self.btnSaveStaff.clicked.connect(lambda : staffClass.saveStaff())
    self.txtStaffSearch.textChanged.connect(lambda : staffClass.search())
