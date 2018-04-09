# -*- coding: utf-8 -*-

import sys
sys.path = ['..'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

import fileHandling
from validation import validate
from datetime import date

class customer():

    def __init__(self, ui_class):
        #  starts an object of the filehandling class
        self.file = fileHandling.fileHandling('database/customers.json')

        #  staffSort is what field the table
        #  is sorted by on double click
        self.sortValue = 'id'

        self.fileContent = self.file.readFile()['data']

        self.tableData = self.file.readFile()['data']

        #  sets column titles
        self.columnTitles = ['ID',
                             'Name',
                             'Surname',
                             'DOB',
                             'Sex',
                             'Phone',
                             'Email',
                             'Primary-contact-info',
                             'Address',
                             'Postcode',
                             'Allergies']

        #  assigning the ui to a variable for use
        self.ui = ui_class

        #  threaded method to fill the table
        self.makeTable = self.fillTable(self.fileContent, self.file.readFile(), self.ui)

        #  set true on double click
        self.filter = False

        self.startTable()

    def fillFields(self, rowNum):
        self.ui.txtCustomerID.setText(str(list(self.tableData[rowNum].keys())[0]))

        self.ui.txtCustomerFirstname.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['name'])

        self.ui.txtCustomerSurname.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['surname']))

        text = str(self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['sex'])

        index = self.ui.cmbCustomerSex.findText(text, QtCore.Qt.MatchFixedString)

        self.ui.cmbCustomerSex.setCurrentIndex(index)

        self.ui.txtCustomerPhoneNumber.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['phone']))

        self.ui.txtCustomerEmail.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['email']))

        text = str(self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['primary-contact-info'])

        index = self.ui.cmbCustomerContact.findText(text, QtCore.Qt.MatchFixedString)

        self.ui.cmbCustomerContact.setCurrentIndex(index)

        self.ui.txtCustomerAddress.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['address']))

        self.ui.txtCustomerPostcode.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['postcode']))

        self.ui.txtCustomerAllergies.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['allergies']))

        #  DOB is in this format: 1980-01-01
        #  YYYY-MM-DD
        #  therefore must be altered for the dateEdit
        dob = self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['dob']
        #  dob[0:4] is year YYYY
        #  dob[5:7] is month MM
        #  dob[8:10] is day DD
        self.ui.dateCustomerDOB.setDate(QtCore.QDate(int(dob[0:4]), int(dob[5:7]), int(dob[8:])))

    def search(self):
        if self.filter:
            try:
                searchIndex = self.file.binSearch(
                    self.tableData, self.ui.txtCustomerSearch.text(), self.searchTerm)

                self.fillFields(int(searchIndex))

            except TypeError:
                QMessageBox.about(self.ui, "Error", 'Field not found')

        else:
            QMessageBox.about(self.ui, "Error", 'Must double click on a field first to sort by')

    def checkFields(self, newField):
        #  interfacing with validation class

        #  primary contact info validation
        if self.ui.cmbCustomerContact.currentText() == 'Phone number':
            val = validate.checkPresence(self.ui.txtCustomerPhoneNumber.text(), 'Phone number')
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

            #  length validation
            val = validate.checkLength(self.ui.txtCustomerPhoneNumber.text(), 11, 12)
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        else:
            val = validate.checkPresence(self.ui.txtCustomerEmail.text(), 'Email')
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

            #  email validation
            val = validate.isEmail(self.ui.txtCustomerEmail.text())
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  address related validation
        addr = self.ui.txtCustomerAddress.text()

        if validate.checkPresence(addr, 'Address') is True:
            val = validate.isInt(addr.split(' ')[0])
            val2 = validate.isAlphaNumeric(addr)

            if (val and val2) is not True: QMessageBox.about(self.ui, "Error", 'Address is incorrect format'); return False

            #  postcode presence check
            val = validate.checkPresence(self.ui.txtCustomerPostcode.text(), 'Postcode')
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

            #  postcode validation
            val = validate.checkPostcode(self.ui.txtCustomerPostcode.text())
            if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.checkPresence(self.ui.txtCustomerFirstname.text(), 'First name')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.checkPresence(self.ui.txtCustomerSurname.text(), 'Surname')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  if the data is new then the date can be checked
        #  relies on the fact that dob and appointment dates
        #  will never or will rarely change
        if newField is True:
            #  date range 80 years ago to 16 years ago
            dob = self.ui.dateCustomerDOB.date().toPyDate().strftime('%Y-%m-%d')

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

        self.makeTable.file = self.file.readFile()
        self.startTable()
        self.cancel()

    def save(self):
        #  activates when save button is pressed

        ID = int(self.ui.txtCustomerID.text())

        if ID != int(self.file.newID()):
            newUser = False
        else:
            newUser = True

        if self.checkFields(newUser) is True:
            #  creates a dictionary of the user for the file

            arrUser = {
                ID: {
                    'name': self.ui.txtCustomerFirstname.text(),
                    'surname': self.ui.txtCustomerSurname.text(),
                    'dob': self.ui.dateCustomerDOB.date().toPyDate().strftime('%Y-%m-%d'),
                    'sex': self.ui.cmbCustomerSex.currentText(),
                    'phone': self.ui.txtCustomerPhoneNumber.text(),
                    'email': self.ui.txtCustomerEmail.text(),
                    'primary-contact-info': self.ui.cmbCustomerContact.currentText(),
                    'address': self.ui.txtCustomerAddress.text(),
                    'postcode': self.ui.txtCustomerPostcode.text(),
                    'allergies': self.ui.txtCustomerAllergies.text()
                }}

            #  if its an old ID thats updated
            #  otherwise it's added to the end
            if newUser is False:
                self.file.editOneField(arrUser, ID)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been updated')

            else:
                self.file.writeToFile(arrUser)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been added')

            self.ui.valueChange.emit(1)

    def startTable(self):
        self.ui.listCustomers.update()

        #  put the file into a variable
        customerFile = self.file.readFile()

        #  row amount
        rowNum = len(customerFile['data'])

        #  sets row and column amounts
        self.ui.listCustomers.setRowCount(rowNum)
        self.ui.listCustomers.setColumnCount(len(self.columnTitles))
        self.ui.listCustomers.setHorizontalHeaderLabels(self.columnTitles)

        self.makeTable.start()

    def click(self):
        #  function allows user to pre fill boxes based on a selected row
        rows = sorted(set(index.row() for index in self.ui.listCustomers.selectedIndexes()))
        for row in rows:
            rowNum = int(row)
        self.fillFields(rowNum)

    def doubleClick(self):
        #  allows a column to be selected for sorting and searching
        columns = sorted(set(index.column() for index in self.ui.listCustomers.selectedIndexes()))

        for column in columns:
            self.sortValue = column

        if self.columnTitles[self.sortValue] == 'ID':
            #  sets to default
            self.tableData = self.file.readFile()['data']
            self.filter = False
            self.makeTable.setTableContent([], tableFilter=self.filter)
            self.makeTable.customerFile = self.file.readFile()

        else:
            #  sorts data and displays
            sortedData = self.file.quicksort(self.columnTitles[self.sortValue].lower())
            self.searchTerm = self.columnTitles[self.sortValue].lower()

            self.tableData = sortedData
            self.filter = True
            self.makeTable.setTableContent(sortedData)

        self.startTable()

    class fillTable(QThread):
        def __init__(self, content, file, ui):
            QThread.__init__(self)
            self.fileContent = content
            self.file = file
            self.tableContent = []
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

            self.ui.listCustomers.setItem(i, 0, QtWidgets.QTableWidgetItem(str(list(self.tableContent[i].keys())[0])))

            self.ui.listCustomers.setItem(i, 1, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['name']))

            self.ui.listCustomers.setItem(i, 2, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['surname']))

            self.ui.listCustomers.setItem(i, 3, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['dob']))

            self.ui.listCustomers.setItem(i, 4, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['sex']))

            self.ui.listCustomers.setItem(i, 5, QtWidgets.QTableWidgetItem(
                str(self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['phone'])))

            self.ui.listCustomers.setItem(i, 6, QtWidgets.QTableWidgetItem(
                str(self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['email'])))

            self.ui.listCustomers.setItem(i, 7, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['primary-contact-info']))

            self.ui.listCustomers.setItem(i, 8, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['address']))

            self.ui.listCustomers.setItem(i, 9, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['postcode']))

            self.ui.listCustomers.setItem(i, 10, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['allergies']))

        def run(self):
            #  row amount
            rowNum = len(self.file['data'])
            for i in range(rowNum):
                self.fillTable(self.file['data'][i], i)

            self.ui.listCustomers.update()

    def cancel(self):
        #  clears significant fields and assigns new ID
        self.ui.txtCustomerID.setText(str(self.file.newID()))
        self.ui.txtCustomerFirstname.setText('')
        self.ui.txtCustomerSurname.setText('')
        self.ui.txtCustomerPhoneNumber.setText('')
        self.ui.txtCustomerEmail.setText('')
        self.ui.txtCustomerAddress.setText('')
        self.ui.txtCustomerPostcode.setText('')
        self.ui.txtCustomerAllergies.setText('')

#  customer form
def createCustomerForm(self):
    self.pageCustomers = QtWidgets.QWidget()
    self.pageCustomers.setObjectName("pageCustomers")
    
    self.label_18 = QtWidgets.QLabel(self.pageCustomers)
    self.label_18.setGeometry(QtCore.QRect(10, 390, 161, 17))
    self.label_18.setObjectName("label_18")
    
    self.label_19 = QtWidgets.QLabel(self.pageCustomers)
    self.label_19.setGeometry(QtCore.QRect(230, 520, 151, 17))
    self.label_19.setObjectName("label_19")
    
    self.txtCustomerFirstname = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerFirstname.setGeometry(QtCore.QRect(10, 480, 181, 29))
    self.txtCustomerFirstname.setObjectName("txtCustomerFirstname")
    
    self.label_20 = QtWidgets.QLabel(self.pageCustomers)
    self.label_20.setGeometry(QtCore.QRect(10, 520, 151, 17))
    self.label_20.setObjectName("label_20")
    
    self.txtCustomerID = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerID.setGeometry(QtCore.QRect(100, 420, 91, 29))
    self.txtCustomerID.setToolTipDuration(-1)
    self.txtCustomerID.setReadOnly(True)
    self.txtCustomerID.setObjectName("txtCustomerID")
    
    self.label_21 = QtWidgets.QLabel(self.pageCustomers)
    self.label_21.setGeometry(QtCore.QRect(670, 390, 67, 31))
    self.label_21.setObjectName("label_21")
    
    self.txtCustomerSurname = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerSurname.setGeometry(QtCore.QRect(10, 540, 181, 29))
    self.txtCustomerSurname.setObjectName("txtCustomerSurname")
    
    self.listCustomers = QtWidgets.QTableWidget(self.pageCustomers)
    self.listCustomers.setGeometry(QtCore.QRect(10, 30, 1111, 351))
    self.listCustomers.setObjectName("listCustomers")
    self.listCustomers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    self.label_22 = QtWidgets.QLabel(self.pageCustomers)
    self.label_22.setGeometry(QtCore.QRect(10, 430, 81, 17))
    self.label_22.setObjectName("label_22")
    
    self.txtCustomerPhoneNumber = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerPhoneNumber.setGeometry(QtCore.QRect(230, 480, 181, 29))
    self.txtCustomerPhoneNumber.setObjectName("txtCustomerPhoneNumber")
    
    self.btnSaveCustomer = QtWidgets.QPushButton(self.pageCustomers)
    self.btnSaveCustomer.setGeometry(QtCore.QRect(10, 640, 101, 29))
    self.btnSaveCustomer.setObjectName("btnSaveCustomer")
    
    self.label_23 = QtWidgets.QLabel(self.pageCustomers)
    self.label_23.setGeometry(QtCore.QRect(450, 520, 161, 17))
    self.label_23.setObjectName("label_23")
    
    self.dateCustomerDOB = QtWidgets.QDateEdit(self.pageCustomers)
    self.dateCustomerDOB.setGeometry(QtCore.QRect(450, 540, 141, 27))
    self.dateCustomerDOB.setCalendarPopup(True)
    self.dateCustomerDOB.setObjectName("dateCustomerDOB")
    
    self.txtCustomerEmail = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerEmail.setGeometry(QtCore.QRect(230, 540, 181, 29))
    self.txtCustomerEmail.setObjectName("txtCustomerEmail")
    
    self.label_24 = QtWidgets.QLabel(self.pageCustomers)
    self.label_24.setGeometry(QtCore.QRect(450, 460, 161, 17))
    self.label_24.setObjectName("label_24")
    
    self.label_25 = QtWidgets.QLabel(self.pageCustomers)
    self.label_25.setGeometry(QtCore.QRect(230, 460, 151, 17))
    self.label_25.setObjectName("label_25")
    
    self.txtCustomerSearch = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerSearch.setGeometry(QtCore.QRect(750, 390, 371, 29))
    self.txtCustomerSearch.setObjectName("txtCustomerSearch")
    
    self.label_26 = QtWidgets.QLabel(self.pageCustomers)
    self.label_26.setGeometry(QtCore.QRect(10, 460, 151, 17))
    self.label_26.setObjectName("label_26")
    
    self.cmbCustomerContact = QtWidgets.QComboBox(self.pageCustomers)
    self.cmbCustomerContact.setGeometry(QtCore.QRect(450, 480, 141, 25))
    self.cmbCustomerContact.setObjectName("cmbCustomerContact")
    self.cmbCustomerContact.addItem("")
    self.cmbCustomerContact.addItem("")
    
    self.label_27 = QtWidgets.QLabel(self.pageCustomers)
    self.label_27.setGeometry(QtCore.QRect(10, 580, 67, 17))
    self.label_27.setObjectName("label_27")
    
    self.txtCustomerAddress = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerAddress.setGeometry(QtCore.QRect(10, 600, 211, 29))
    self.txtCustomerAddress.setObjectName("txtCustomerAddress")
    
    self.label_28 = QtWidgets.QLabel(self.pageCustomers)
    self.label_28.setGeometry(QtCore.QRect(230, 580, 121, 17))
    self.label_28.setObjectName("label_28")
    
    self.txtCustomerPostcode = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerPostcode.setGeometry(QtCore.QRect(230, 600, 181, 29))
    self.txtCustomerPostcode.setObjectName("txtCustomerPostcode")
    
    self.label_29 = QtWidgets.QLabel(self.pageCustomers)
    self.label_29.setGeometry(QtCore.QRect(230, 430, 67, 17))
    self.label_29.setObjectName("label_29")
    
    self.txtCustomerAllergies = QtWidgets.QLineEdit(self.pageCustomers)
    self.txtCustomerAllergies.setGeometry(QtCore.QRect(300, 420, 291, 29))
    self.txtCustomerAllergies.setObjectName("txtCustomerAllergies")
    
    self.label_30 = QtWidgets.QLabel(self.pageCustomers)
    self.label_30.setGeometry(QtCore.QRect(10, 0, 91, 17))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_30.setFont(font)
    self.label_30.setObjectName("label_30")
    
    self.cmbCustomerSex = QtWidgets.QComboBox(self.pageCustomers)
    self.cmbCustomerSex.setGeometry(QtCore.QRect(450, 600, 141, 25))
    self.cmbCustomerSex.setObjectName("cmbCustomerSex")
    self.cmbCustomerSex.addItem("")
    self.cmbCustomerSex.addItem("")
    
    self.label_75 = QtWidgets.QLabel(self.pageCustomers)
    self.label_75.setGeometry(QtCore.QRect(450, 579, 161, 17))
    self.label_75.setObjectName("label_75")
    
    self.btnCustomerCancel = QtWidgets.QPushButton(self.pageCustomers)
    self.btnCustomerCancel.setGeometry(QtCore.QRect(130, 640, 101, 29))
    self.btnCustomerCancel.setObjectName("btnCustomerCancel")

    self.stackedWidget.addWidget(self.pageCustomers)

    customerClass = customer(self)

    #  restarts form
    customerClass.cancel()

    #  connects a click on the table to the select the row
    self.listCustomers.clicked.connect(lambda: customerClass.click())
    self.listCustomers.doubleClicked.connect(lambda: customerClass.doubleClick())

    #  connecting the buttons
    self.btnCustomerCancel.clicked.connect(lambda: customerClass.cancel())
    self.btnSaveCustomer.clicked.connect(lambda: customerClass.save())
    self.txtCustomerSearch.textChanged.connect(lambda: customerClass.search())
