# -*- coding: utf-8 -*-
import sys

#  needed for connecting to shared
#  routines and the files
sys.path = ['..'] + sys.path
sys.path = ['bin'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from autoComboBox import FilteringComboBox

import fileHandling
from validation import validate
from datetime import date

'''
S1
All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
S3
Any details should be editable by the manager only except for changing comments. 
S4
Staff should be able to add comments that show up on the manager's main homepage. Adding to the appointment when it’s made or edited to be completed.
I1
To ensure all dates are the same they’ll be selected using PyQt5’s calendar function.
I2
To check all numeric inputs against a validation class. (data type, range check, length check)
I3
Presence checks will be done on all required fields such as name and any other needed values (see design section)
I4
ID will be automatically entered to avoid errors
I7
To avoid unnecessary errors most data will be selected from list boxes so it’s automatically entered
P2
When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
P4
Using table view boxes to store data that can be selected for use. This was mentioned in #9 of input validation, they’ll be used for efficiency of data inputs, and improving the user interface. These will be filled with the use of threads.
P5
When an appointment is made there will be an approximate price generated from the appointment type and the member of staff who will be doing the appointment.
P7
Staff members can add comments to appointments that the manager can view but they can’t unless they made the appointment.
P8
The processing of data for inputting into the files will be done as a Class system that can be easily called since each file is similar in layout.
O2
Only the member of staff and the manager should be able to edit the comments attached to an appointment.
O4
Data will be shown in tables, all the graphs on the manager panel will load with the page but any on the main chart form will have buttons to generate them.
'''

class appointment():
    def __init__(self, ui_class):
        #  starts an object of the filehandling class
        self.file = fileHandling.fileHandling('database/appointments.json')

        self.staffFile  = fileHandling.fileHandling('database/staff.json').readFile()['data']
        self.treatmentFile = fileHandling.fileHandling('database/priceList.json').readFile()['data']
        self.customerFile = fileHandling.fileHandling('database/customers.json').readFile()['data']

        #  staffSort is what field the table
        #  is sorted by on double click
        self.sortValue = 'id'

        self.fileContent = self.file.readFile()['data']

        self.tableData = self.file.readFile()['data']

        #  sets column titles
        self.columnTitles = ['ID',
                             'Staff',
                             'Customer',
                             'Treatment',
                             'Date',
                             'Time',
                             'Cost',
                             'Amount-Paid',
                             'Comments']

        #  assigning the ui to a variable for use
        self.ui = ui_class

        #  threaded method to fill the table
        self.makeTable = self.fillTable(self.fileContent, self.file.readFile(), self.ui)

        #  set true on double click
        self.filter = False

        self.startTable()
        self.fillComboBoxes()

    def fillComboBoxes(self):
		'''
		I7
		To avoid unnecessary errors most data will be selected from list boxes so it’s automatically entered
		'''
        #  fills the combo box for stock selection
        #  tmparr is used to fill the combo box
        tmparr = []

        #  staff combo box
        for i in range(len(self.staffFile)):
            id = int(list(self.staffFile[i].keys())[0])

            #  fill the combo box
            tmparr.append(str(id) + '    ' + str(self.staffFile[id][str(id)]['name']))

        self.ui.cmbStaffSelect.clear()
        self.ui.cmbStaffSelect.addItems(tmparr)
        tmparr = []

        #  treatments combo box
        for i in range(len(self.treatmentFile)):
            id = int(list(self.treatmentFile[i].keys())[0])

            #  fill the combo box
            tmparr.append(str(id) + '    ' + str(self.treatmentFile[id][str(id)]['name']))

        self.ui.cmbTreatmentSelect.clear()
        self.ui.cmbTreatmentSelect.addItems(tmparr)
        tmparr = []

        #  customers combo box
        for i in range(len(self.customerFile)):
            id = int(list(self.customerFile[i].keys())[0])

            #  fill the combo box
            tmparr.append(str(id) + '    ' + str(self.customerFile[id][str(id)]['name']))

        self.ui.cmbCustomerSelect.clear()
        self.ui.cmbCustomerSelect.addItems(tmparr)

    def findTimes(self, date):
        #  clears the combo box for time
        self.ui.cmbAppointmentTime.clear()

        timeSlots = ['09:00',
                     '10:00',
                     '11:00',
                     '13:00',
                     '14:00',
                     '15:00',
                     '16:00']
        try:
            for field in range(len(self.tableData)):
                id = str(list(self.tableData[field].keys())[0])

                if self.tableData[field][id]['date'] == date:
                    timeSlots.remove(self.tableData[field][id]['time'])

        except ValueError:
            #  if time isn't in timeSlots
            pass

        self.ui.cmbAppointmentTime.addItems(timeSlots)

    def fillFields(self, rowNum):
        id = str(list(self.tableData[rowNum].keys())[0])
        self.ui.txtAppointmentID.setText(id)

        #  opens the file
        staffFile = fileHandling.fileHandling('database/staff.json').readFile()['data']

        #  gets the id of the field from the local file
        staffID = str(self.tableData[rowNum][id]['staff'])

        #  sets the field for the combo box and selects it
        text = staffID + '    ' + staffFile[int(staffID)][staffID]['name']
        index = self.ui.cmbStaffSelect.findText(text, QtCore.Qt.MatchFixedString)
        self.ui.cmbStaffSelect.setCurrentIndex(index)

        #  opens the file
        customerFile = fileHandling.fileHandling('database/customers.json').readFile()['data']

        #  gets the id of the field from the local file
        customerID = str(self.tableData[rowNum][id]['customer'])

        #  sets the field for the combo box and selects it
        text = customerID + '    ' + customerFile[int(customerID)][customerID]['name']
        index = self.ui.cmbCustomerSelect.findText(text, QtCore.Qt.MatchFixedString)
        self.ui.cmbCustomerSelect.setCurrentIndex(index)

        #  opens the file
        treatmentFile = fileHandling.fileHandling('database/priceList.json').readFile()['data']

        #  gets the id of the field from the local file
        treatmentID = str(self.tableData[rowNum][id]['treatment'])

        #  sets the field for the combo box and selects it
        text = treatmentID + '    ' + treatmentFile[int(treatmentID)][treatmentID]['name']
        index = self.ui.cmbTreatmentSelect.findText(text, QtCore.Qt.MatchFixedString)
        self.ui.cmbTreatmentSelect.setCurrentIndex(index)
		
		'''
		I1
		To ensure all dates are the same they’ll be selected using PyQt5’s calendar function.
		'''
        #  date is in this format: 1980-01-01
        #  YYYY-MM-DD
        #  therefore must be altered for the dateEdit
        date = self.tableData[rowNum][id]['date']
        #  date[0:4] is year YYYY
        #  date[5:7] is month MM
        #  date[8:10] is day DD
        self.ui.dateAppointment.setDate(QtCore.QDate(int(date[0:4]), int(date[5:7]), int(date[8:])))

        self.findTimes(date)

        self.setAppCost()

        self.ui.dsbAppointmentAmountPaid.setValue(float(
            self.tableData[rowNum][id]['amount-paid']))

        self.ui.txtAppointmentComment.setText(str(
            self.tableData[rowNum][id]['comments']))
		
		'''
		P7
		Staff members can add comments to appointments that the manager can view but they can’t unless they made the appointment.
		'''
		'''
		O2
		Only the member of staff and the manager should be able to edit the comments attached to an appointment.
		'''
        #  only the person who made the appointment or an admin can edit the comment
        if self.ui.userLoggedIn == self.staffFile[int(staffID)][str(staffID)]['username'] or self.ui.accessLevel is True:
            self.ui.txtAppointmentComment.setReadOnly(False)
        else:
            self.ui.txtAppointmentComment.setReadOnly(True)

    def setAppCost(self):
		'''
		P5
		When an appointment is made there will be an approximate price generated from the appointment type and the member of staff who will be doing the appointment.
		'''
        #  opens the file
        treatmentFile = fileHandling.fileHandling('database/priceList.json').readFile()['data']

        #  gets the id of the field from the local file
        treatmentID = self.ui.cmbTreatmentSelect.currentText().split(' ')[0]

        treatmentCost = treatmentFile[int(treatmentID)][treatmentID]['price']

        #  sets the appointment cost range to a minimum
        #  of the actual cost and a maximum of 10% extra
        self.ui.dsbAppointmentAmount.setRange(float(treatmentCost), float(treatmentCost * 1.1))
        self.ui.dsbAppointmentAmount.setValue(float(
            treatmentCost))

    def search(self):
        if self.filter:
            try:
                searchIndex = self.file.binSearch(
                    self.tableData, self.ui.txtAppointmentSearch.text(), self.searchTerm)

                self.fillFields(int(searchIndex))

            except TypeError:
                QMessageBox.about(self.ui, "Error", 'Field not found')

        else:
            QMessageBox.about(self.ui, "Error", 'Must double click on a field first to sort by')

    def checkFields(self, newField):
        #  interfacing with validation class
		'''
		I2
		To check all numeric inputs against a validation class. (data type, range check, length check)
		'''
		'''
		I3
		Presence checks will be done on all required fields such as name and any other needed values (see design section)
		'''
        if newField is True:
            #  date range now to 1 years ahead
            appDate = self.ui.dateAppointment.date().toPyDate().strftime('%Y-%m-%d')

            low = date.today().strftime('%Y-%m-%d')

            high = date.today().strftime('%Y-%m-%d')
            high = str(int(high[:4]) + 1) + high[4:]

            val = validate.checkRange(appDate, low, high)
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

        ID = int(self.ui.txtAppointmentID.text())

        if ID != int(self.file.newID()):
            newField = False
        else:
            newField = True

        if self.checkFields(newField):
            #  creates a dictionary of the user for the file
			'''
			S1
			All customers details should be saved together (names, phone number, email address, DoB) Customer ID will be the key and then the details will be attached as subheadings in the file.
			'''
			'''
			S4
			Staff should be able to add comments that show up on the manager's main homepage. Adding to the appointment when it’s made or edited to be completed.
			'''
			'''
			I1
			To ensure all dates are the same they’ll be selected using PyQt5’s calendar function.
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
                ID: {
                    'staff': self.ui.cmbStaffSelect.currentText().split(' ')[0],
                    'customer': self.ui.cmbCustomerSelect.currentText().split(' ')[0],
                    'treatment': self.ui.cmbTreatmentSelect.currentText().split(' ')[0],
                    'date': self.ui.dateAppointment.date().toPyDate().strftime('%Y-%m-%d'),
                    'time': self.ui.cmbAppointmentTime.currentText(),
                    'cost': self.ui.dsbAppointmentAmount.value(),
                    'amount-paid': self.ui.dsbAppointmentAmountPaid.value(),
                    'comments': self.ui.txtAppointmentComment.text()
                }}

            date = self.ui.dateAppointment.date().toPyDate().strftime('%Y-%m-%d')

            self.ui.dateAppointment.setDate(QtCore.QDate(int(date[0:4]), int(date[5:7]), int(date[8:10])))

            self.findTimes(date)

            #  if its an old ID thats updated
            #  otherwise it's added to the end
			'''
			S3
			Any details should be editable by the manager only except for changing comments. 
			'''
            if newField is False:
                self.file.editOneField(arrUser, ID)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been updated')

            else:
                self.file.writeToFile(arrUser)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been added')

            self.newTime()

    def startTable(self):
        self.ui.listAppointments.update()

        #  put the file into a variable
        file = self.file.readFile()

        #  row amount
        rowNum = len(file['data'])

        #  sets row and column amounts
        self.ui.listAppointments.setRowCount(rowNum)
        self.ui.listAppointments.setColumnCount(len(self.columnTitles))
        self.ui.listAppointments.setHorizontalHeaderLabels(self.columnTitles)

        self.makeTable.start()

    def click(self):
		'''
		S3
		Any details should be editable by the manager only except for changing comments. 
		'''
		'''
		I7
		To avoid unnecessary errors most data will be selected from list boxes so it’s automatically entered
		'''
        #  function allows user to pre fill boxes based on a selected row
        rows = sorted(set(index.row() for index in self.ui.listAppointments.selectedIndexes()))
        for row in rows:
            rowNum = int(row)
        self.fillFields(rowNum)

    def doubleClick(self):
        #  allows a column to be selected for sorting and searching
        columns = sorted(set(index.column() for index in self.ui.listAppointments.selectedIndexes()))

        for column in columns:
            self.sortValue = column

        if self.columnTitles[self.sortValue] == 'ID':
            #  sets to default
            self.tableData = self.file.readFile()['data']
            self.filter = False
            self.makeTable.setTableContent([], tableFilter=self.filter)
            self.makeTable.file = self.file.readFile()

        else:
            #  sorts data and displays
            sortedData = self.file.quicksort(self.columnTitles[self.sortValue].lower())
            self.searchTerm = self.columnTitles[self.sortValue].lower()

            self.tableData = sortedData
            self.filter = True
            self.makeTable.setTableContent(sortedData)

        self.startTable()

    class fillTable(QThread):
		'''
		I7
		To avoid unnecessary errors most data will be selected from list boxes so it’s automatically entered
		'''
		'''
		P4
		Using table view boxes to store data that can be selected for use. This was mentioned in #9 of input validation, they’ll be used for efficiency of data inputs, and improving the user interface. These will be filled with the use of threads.
		'''
		'''
		P8
		The processing of data for inputting into the files will be done as a Class system that can be easily called since each file is similar in layout.
		'''
		'''
		O4
		Data will be shown in tables, all the graphs on the manager panel will load with the page but any on the main chart form will have buttons to generate them.
		'''
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

            id = str(list(self.tableContent[i].keys())[0])

            self.ui.listAppointments.setItem(
                i, 0, QtWidgets.QTableWidgetItem(id))

            #  gets the name from the file for the table
            staffFile = fileHandling.fileHandling('database/staff.json').readFile()['data']
            staffID = self.tableContent[i][id]['staff']

            self.ui.listAppointments.setItem(i, 1, QtWidgets.QTableWidgetItem(
                staffFile[int(staffID)][staffID]['name']))

            #  gets the name from the file for the table
            customerFile = fileHandling.fileHandling('database/customers.json').readFile()['data']
            customerID = self.tableContent[i][id]['customer']
            customerName = customerFile[int(customerID)][customerID]['name']

            self.ui.listAppointments.setItem(i, 2, QtWidgets.QTableWidgetItem(
                customerName))

            #  gets the name from the file for the table
            treatmentFile = fileHandling.fileHandling('database/priceList.json').readFile()['data']
            treatmentID = self.tableContent[i][id]['treatment']

            self.ui.listAppointments.setItem(i, 3, QtWidgets.QTableWidgetItem(
                treatmentFile[int(treatmentID)][treatmentID]['name']))

            self.ui.listAppointments.setItem(i, 4, QtWidgets.QTableWidgetItem(
                self.tableContent[i][id]['date']))

            self.ui.listAppointments.setItem(i, 5, QtWidgets.QTableWidgetItem(
                self.tableContent[i][id]['time']))

            appCost = str(self.tableContent[i][id]['cost'])

            self.ui.listAppointments.setItem(i, 6, QtWidgets.QTableWidgetItem(
                appCost))

            amountPaid = str(self.tableContent[i][id]['amount-paid'])

            self.ui.listAppointments.setItem(i, 7, QtWidgets.QTableWidgetItem(
                amountPaid))

            comment = self.tableContent[i][id]['comments']

            self.ui.listAppointments.setItem(i, 8, QtWidgets.QTableWidgetItem(
                comment))
            
            #  adds comment to manager menu for if appointment isn't paid for
			
            if amountPaid < appCost:
                message = 'Appointment: {0} hasn\'t been paid fully by {1}'.format(id, customerName)
                exist = False

                #  checks if the message is already in the list

                for i in range(len(self.ui.notifications)):
                    if self.ui.notifications[i] == message:
                        exist = True

                if exist is False:
                    self.ui.notifications.append(message)
                    self.ui.addNotifications(self.ui, self.ui.notifications)
			'''
			S4
			Staff should be able to add comments that show up on the manager's main homepage. Adding to the appointment when it’s made or edited to be completed.
			'''
            #  adds comment to manager menu as objectives say
            if len(comment) > 0:
                commentMessage = 'Comment left on appointment: ' + id + '    ' + comment
                exist = False

                #  checks if the message is already in the list

                for i in range(len(self.ui.notifications)):
                    if self.ui.notifications[i] == commentMessage:
                        exist = True

                if exist is False:
                    self.ui.notifications.append(commentMessage)
                    self.ui.addNotifications(self.ui, self.ui.notifications)

        def run(self):
            #  row amount
            rowNum = len(self.file['data'])
            for i in range(rowNum):
                self.fillTable(self.file['data'][i], i)

            self.ui.listAppointments.update()

    def newTime(self):
        date = self.ui.dateAppointment.date().toPyDate().strftime('%Y-%d-%m')
        self.findTimes(date)

    def cancel(self):
		'''
		I4
		ID will be automatically entered to avoid errors
		'''
		'''
		P2
		When adding anything to files it will be given a new ID if it doesn't have one already. This will involve adding one to the current maximum ID and then this being added to the JSON files.
		'''
        #  clears significant fields and assigns new ID
        self.ui.txtAppointmentID.setText(str(self.file.newID()))
        self.ui.txtAppointmentComment.setText('')
        self.newTime()

#  appointments form
def createAppointmentForm(self):

    #  decorator
    #  signaling
    @pyqtSlot(int)
    def handleSignal(val):
        #  re-assigns the files and
        #  restarts the combo boxes
        if val == 1:
            appointmentClass.customerFile = fileHandling.fileHandling('database/customers.json').readFile()['data']

        elif val == 2:
            appointmentClass.staffFile = fileHandling.fileHandling('database/staff.json').readFile()['data']

        elif val == 4:
            appointmentClass.treatmentFile = fileHandling.fileHandling('database/priceList.json').readFile()['data']

        appointmentClass.fillComboBoxes()

    self.pageAppointments = QtWidgets.QWidget()
    self.pageAppointments.setObjectName("pageAppointments")
    
    self.label_62 = QtWidgets.QLabel(self.pageAppointments)
    self.label_62.setGeometry(QtCore.QRect(660, 390, 67, 31))
    self.label_62.setObjectName("label_62")
    
    self.label_63 = QtWidgets.QLabel(self.pageAppointments)
    self.label_63.setGeometry(QtCore.QRect(220, 460, 151, 17))
    self.label_63.setObjectName("label_63")
    
    self.txtAppointmentID = QtWidgets.QLineEdit(self.pageAppointments)
    self.txtAppointmentID.setGeometry(QtCore.QRect(110, 420, 71, 29))
    self.txtAppointmentID.setToolTipDuration(-1)
    self.txtAppointmentID.setReadOnly(True)
    self.txtAppointmentID.setObjectName("txtAppointmentID")
    
    self.label_65 = QtWidgets.QLabel(self.pageAppointments)
    self.label_65.setGeometry(QtCore.QRect(0, 430, 101, 17))
    self.label_65.setObjectName("label_65")
    
    self.label_66 = QtWidgets.QLabel(self.pageAppointments)
    self.label_66.setGeometry(QtCore.QRect(0, 520, 151, 17))
    self.label_66.setObjectName("label_66")
    
    self.label_67 = QtWidgets.QLabel(self.pageAppointments)
    self.label_67.setGeometry(QtCore.QRect(0, 390, 161, 17))
    self.label_67.setObjectName("label_67")
    
    self.label_68 = QtWidgets.QLabel(self.pageAppointments)
    self.label_68.setGeometry(QtCore.QRect(430, 520, 121, 17))
    self.label_68.setObjectName("label_68")
    
    self.label_70 = QtWidgets.QLabel(self.pageAppointments)
    self.label_70.setGeometry(QtCore.QRect(220, 520, 151, 17))
    self.label_70.setObjectName("label_70")
    
    self.btnSaveAppointment = QtWidgets.QPushButton(self.pageAppointments)
    self.btnSaveAppointment.setGeometry(QtCore.QRect(0, 640, 101, 29))
    self.btnSaveAppointment.setObjectName("btnSaveAppointment")
    
    self.listAppointments = QtWidgets.QTableWidget(self.pageAppointments)
    self.listAppointments.setGeometry(QtCore.QRect(0, 30, 1111, 351))
    self.listAppointments.setObjectName("listAppointments")
    self.listAppointments.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    self.label_72 = QtWidgets.QLabel(self.pageAppointments)
    self.label_72.setGeometry(QtCore.QRect(0, 580, 101, 17))
    self.label_72.setObjectName("label_72")
    
    self.label_73 = QtWidgets.QLabel(self.pageAppointments)
    self.label_73.setGeometry(QtCore.QRect(0, 460, 151, 17))
    self.label_73.setObjectName("label_73")
    
    self.txtAppointmentSearch = QtWidgets.QLineEdit(self.pageAppointments)
    self.txtAppointmentSearch.setGeometry(QtCore.QRect(740, 390, 371, 29))
    self.txtAppointmentSearch.setObjectName("txtAppointmentSearch")
    
    self.label_74 = QtWidgets.QLabel(self.pageAppointments)
    self.label_74.setGeometry(QtCore.QRect(0, 0, 121, 17))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_74.setFont(font)
    self.label_74.setObjectName("label_74")
    
    self.cmbStaffSelect = FilteringComboBox(self.pageAppointments)
    self.cmbStaffSelect.setGeometry(QtCore.QRect(0, 490, 181, 25))
    self.cmbStaffSelect.setObjectName("cmbStaffSelect")
    
    self.cmbCustomerSelect = FilteringComboBox(self.pageAppointments)
    self.cmbCustomerSelect.setGeometry(QtCore.QRect(0, 550, 181, 25))
    self.cmbCustomerSelect.setObjectName("cmbCustomerSelect")
    
    self.cmbTreatmentSelect = FilteringComboBox(self.pageAppointments)
    self.cmbTreatmentSelect.setGeometry(QtCore.QRect(0, 610, 181, 25))
    self.cmbTreatmentSelect.setObjectName("cmbTreatmentSelect")
    
    self.dateAppointment = QtWidgets.QDateEdit(self.pageAppointments)
    self.dateAppointment.setGeometry(QtCore.QRect(220, 490, 181, 27))
    self.dateAppointment.setCalendarPopup(True)
    self.dateAppointment.setObjectName("dateAppointment")
    
    self.cmbAppointmentTime = FilteringComboBox(self.pageAppointments)
    self.cmbAppointmentTime.setGeometry(QtCore.QRect(220, 550, 181, 25))
    self.cmbAppointmentTime.setObjectName("cmbAppointmentTime")
    
    self.dsbAppointmentAmountPaid = QtWidgets.QDoubleSpinBox(self.pageAppointments)
    self.dsbAppointmentAmountPaid.setGeometry(QtCore.QRect(450, 550, 151, 27))
    self.dsbAppointmentAmountPaid.setObjectName("dsbAppointmentAmountPaid")
    
    self.label_64 = QtWidgets.QLabel(self.pageAppointments)
    self.label_64.setGeometry(QtCore.QRect(435, 550, 21, 21))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_64.setFont(font)
    self.label_64.setObjectName("label_64")
    
    self.dsbAppointmentAmount = QtWidgets.QDoubleSpinBox(self.pageAppointments)
    self.dsbAppointmentAmount.setGeometry(QtCore.QRect(450, 490, 151, 27))
    self.dsbAppointmentAmount.setObjectName("dsbAppointmentAmount")
    
    self.label_69 = QtWidgets.QLabel(self.pageAppointments)
    self.label_69.setGeometry(QtCore.QRect(435, 490, 21, 21))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_69.setFont(font)
    self.label_69.setObjectName("label_69")
    
    self.label_71 = QtWidgets.QLabel(self.pageAppointments)
    self.label_71.setGeometry(QtCore.QRect(430, 460, 121, 17))
    self.label_71.setObjectName("label_71")
    
    self.btnAppointmentCancel = QtWidgets.QPushButton(self.pageAppointments)
    self.btnAppointmentCancel.setGeometry(QtCore.QRect(110, 640, 101, 29))
    self.btnAppointmentCancel.setObjectName("btnAppointmentCancel")
    
    self.label_76 = QtWidgets.QLabel(self.pageAppointments)
    self.label_76.setGeometry(QtCore.QRect(220, 580, 81, 17))
    self.label_76.setObjectName("label_76")
    
    self.txtAppointmentComment = QtWidgets.QLineEdit(self.pageAppointments)
    self.txtAppointmentComment.setGeometry(QtCore.QRect(220, 610, 381, 29))
    self.txtAppointmentComment.setObjectName("txtAppointmentComment")
    
    self.stackedWidget.addWidget(self.pageAppointments)

    appointmentClass = appointment(self)

    #  restarts form
    appointmentClass.cancel()

    #  connects a click on the table to the select the row
    self.listAppointments.clicked.connect(lambda: appointmentClass.click())
    self.listAppointments.doubleClicked.connect(lambda: appointmentClass.doubleClick())

    #  connecting the buttons
    self.btnAppointmentCancel.clicked.connect(lambda: appointmentClass.cancel())
    self.btnSaveAppointment.clicked.connect(lambda: appointmentClass.save())
    self.txtAppointmentSearch.textChanged.connect(lambda: appointmentClass.search())
    self.dateAppointment.dateChanged.connect(lambda: appointmentClass.newTime())

    self.cmbTreatmentSelect.activated.connect(lambda: appointmentClass.setAppCost())

    #  signals
    self.valueChange.connect(handleSignal)
