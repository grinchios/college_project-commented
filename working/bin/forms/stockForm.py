# -*- coding: utf-8 -*-

import sys

sys.path = ['..'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

import fileHandling
from validation import validate

class stock():
    def __init__(self, ui_class):
        #  starts an object of the filehandling class
        self.file = fileHandling.fileHandling('database/stock.json')

        #  staffSort is what field the table
        #  is sorted by on double click
        self.sortValue = 'id'

        self.fileContent = self.file.readFile()['data']

        self.tableData = self.file.readFile()['data']

        #  sets column titles
        self.columnTitles = ['ID',
                             'Name',
                             'Price',
                             'Stock-Level',
                             'Alert-Level']

        #  assigning the ui to a variable for use
        self.ui = ui_class

        #  threaded method to fill the table
        self.makeTable = self.fillTable(self.fileContent, self.file.readFile(), self.ui)

        #  set true on double click
        self.filter = False

        self.startTable()

    def fillFields(self, rowNum):
        self.ui.txtStockID.setText(str(list(self.tableData[rowNum].keys())[0]))

        self.ui.txtStockName.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['name'])

        self.ui.dsbStockPrice.setValue(float(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['price']))

        self.ui.txtStockAmount.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['stock-level']))

        self.ui.txtStockAlert.setText(str(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['alert-level']))

    def search(self):
        if self.filter:
            try:
                searchIndex = self.file.binSearch(
                    self.tableData, self.ui.txtStockSearch.text(), self.searchTerm)

                self.fillFields(int(searchIndex))

            except TypeError:
                QMessageBox.about(self.ui, "Error", 'Field not found')

        else:
            QMessageBox.about(self.ui, "Error", 'Must double click on a field first to sort by')

    def checkFields(self):
        #  interfacing with validation class

        #  stock name presence
        val = validate.checkPresence(self.ui.txtStockName.text(), 'Stock name')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  stock price validation
        val = validate.checkRange(self.ui.dsbStockPrice.value(), 0.01, 1000.00)
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.isFloat(self.ui.dsbStockPrice.value())
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  stock level
        val = validate.checkPresence(self.ui.txtStockAmount.text(), 'Stock level')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.isAlphaNumeric(self.ui.txtStockAmount.text())
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  alert level
        val = validate.checkPresence(self.ui.txtStockAlert.text(), 'Alert level')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.isAlphaNumeric(self.ui.txtStockAlert.text())
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

        ID = int(self.ui.txtStockID.text())

        if ID != int(self.file.newID()):
            newField = False
        else:
            newField = True

        if self.checkFields() is True:
            #  creates a dictionary of the user for the file
            arrUser = {
                ID: {
                    'name': self.ui.txtStockName.text(),
                    'price': self.ui.dsbStockPrice.value(),
                    'stock-level': self.ui.txtStockAmount.text(),
                    'alert-level': self.ui.txtStockAlert.text()
                }}

            #  if its an old ID thats updated
            #  otherwise it's added to the end
            if newField is False:
                self.file.editOneField(arrUser, ID)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been updated')

            else:
                self.file.writeToFile(arrUser)
                self.saveFunc()
                QMessageBox.about(self.ui, "Field edited", 'Field has been added')

            self.ui.valueChange.emit(3)

    def startTable(self):
        #  put the file into a variable
        file = self.file.readFile()['data']

        #  row amount
        rowNum = len(file)

        #  sets row and column amounts
        self.ui.listStock.setRowCount(rowNum)
        self.ui.listStock.setColumnCount(len(self.columnTitles))
        self.ui.listStock.setHorizontalHeaderLabels(self.columnTitles)

        self.ui.listStock.update()

        self.makeTable.start()

    def click(self):
        #  function allows user to pre fill boxes based on a selected row
        rows = sorted(set(index.row() for index in self.ui.listStock.selectedIndexes()))
        for row in rows:
            rowNum = int(row)
        self.fillFields(rowNum)

    def doubleClick(self):
        #  allows a column to be selected for sorting and searching
        columns = sorted(set(index.column() for index in self.ui.listStock.selectedIndexes()))

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

            self.ui.listStock.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(list(self.tableContent[i].keys())[0])))

            stockName = self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['name']
            self.ui.listStock.setItem(i, 1, QtWidgets.QTableWidgetItem(
                stockName))

            self.ui.listStock.setItem(i, 2, QtWidgets.QTableWidgetItem(str(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['price'])))

            stockLevel = self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['stock-level']
            self.ui.listStock.setItem(i, 3, QtWidgets.QTableWidgetItem(
                stockLevel))

            alertLevel = self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['alert-level']
            self.ui.listStock.setItem(i, 4, QtWidgets.QTableWidgetItem(
                alertLevel))

            if int(stockLevel.split(' ')[0]) < int(alertLevel.split(' ')[0]):
                stockMessage = 'Stock level for {0} is {1}'.format(stockName, stockLevel)
                exist = False

                #  checks if the message is already in the list
                for i in range(len(self.ui.notifications)):
                    if self.ui.notifications[i] == stockMessage:
                        exist = True

                if exist is False:
                    self.ui.notifications.append(stockMessage)
                    self.ui.addNotifications(self.ui, self.ui.notifications)

        def run(self):
            #  row amount
            rowNum = len(self.file['data'])
            for i in range(rowNum):
                self.fillTable(self.file['data'][i], i)
            self.ui.listStock.update()

    def cancel(self):
        #  clears significant fields and assigns new ID
        self.ui.txtStockID.setText(str(self.file.newID()))
        self.ui.txtStockName.setText('')
        self.ui.dsbStockPrice.setValue(float(0))
        self.ui.txtStockAmount.setText('')
        self.ui.txtStockAlert.setText('')

#  stock form
def createStockForm(self):

    self.pageStock = QtWidgets.QWidget()
    self.pageStock.setObjectName("pageStock")
    
    self.listStock = QtWidgets.QTableWidget(self.pageStock)
    self.listStock.setGeometry(QtCore.QRect(0, 30, 1111, 351))
    self.listStock.setObjectName("listStock")
    self.listStock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    self.label_77 = QtWidgets.QLabel(self.pageStock)
    self.label_77.setGeometry(QtCore.QRect(210, 520, 151, 17))
    self.label_77.setObjectName("label_77")
    
    self.label_78 = QtWidgets.QLabel(self.pageStock)
    self.label_78.setGeometry(QtCore.QRect(0, 390, 161, 17))
    self.label_78.setObjectName("label_78")
    
    self.txtStockAmount = QtWidgets.QLineEdit(self.pageStock)
    self.txtStockAmount.setGeometry(QtCore.QRect(210, 480, 181, 29))
    self.txtStockAmount.setObjectName("txtStockAmount")
    
    self.txtStockSearch = QtWidgets.QLineEdit(self.pageStock)
    self.txtStockSearch.setGeometry(QtCore.QRect(750, 390, 371, 29))
    self.txtStockSearch.setObjectName("txtStockSearch")
    
    self.label_81 = QtWidgets.QLabel(self.pageStock)
    self.label_81.setGeometry(QtCore.QRect(0, 430, 101, 17))
    self.label_81.setObjectName("label_81")
    
    self.dsbStockPrice = QtWidgets.QDoubleSpinBox(self.pageStock)
    self.dsbStockPrice.setGeometry(QtCore.QRect(23, 550, 151, 27))
    self.dsbStockPrice.setReadOnly(False)
    self.dsbStockPrice.setObjectName("dsbStockPrice")
    
    self.btnSaveStock = QtWidgets.QPushButton(self.pageStock)
    self.btnSaveStock.setGeometry(QtCore.QRect(0, 600, 101, 29))
    self.btnSaveStock.setObjectName("btnSaveStock")
    self.btnSaveStock.setEnabled(self.accessLevel)
    
    self.label_83 = QtWidgets.QLabel(self.pageStock)
    self.label_83.setGeometry(QtCore.QRect(210, 460, 101, 17))
    self.label_83.setObjectName("label_83")
    
    self.label_84 = QtWidgets.QLabel(self.pageStock)
    self.label_84.setGeometry(QtCore.QRect(0, 460, 151, 17))
    self.label_84.setObjectName("label_84")
    
    self.label_86 = QtWidgets.QLabel(self.pageStock)
    self.label_86.setGeometry(QtCore.QRect(670, 400, 67, 17))
    self.label_86.setObjectName("label_86")
    
    self.btnStockCancel = QtWidgets.QPushButton(self.pageStock)
    self.btnStockCancel.setGeometry(QtCore.QRect(110, 600, 101, 29))
    self.btnStockCancel.setObjectName("btnStockCancel")
    self.btnStockCancel.setEnabled(self.accessLevel)
    
    self.txtStockID = QtWidgets.QLineEdit(self.pageStock)
    self.txtStockID.setGeometry(QtCore.QRect(70, 420, 121, 29))
    self.txtStockID.setReadOnly(True)
    self.txtStockID.setObjectName("txtStockID")
    
    self.label_87 = QtWidgets.QLabel(self.pageStock)
    self.label_87.setGeometry(QtCore.QRect(5, 550, 17, 21))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_87.setFont(font)
    self.label_87.setObjectName("label_87")
    
    self.label_88 = QtWidgets.QLabel(self.pageStock)
    self.label_88.setGeometry(QtCore.QRect(0, 520, 121, 17))
    self.label_88.setObjectName("label_88")
    
    self.label_89 = QtWidgets.QLabel(self.pageStock)
    self.label_89.setGeometry(QtCore.QRect(0, 0, 121, 17))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_89.setFont(font)
    self.label_89.setObjectName("label_89")
    
    self.txtStockAlert = QtWidgets.QLineEdit(self.pageStock)
    self.txtStockAlert.setGeometry(QtCore.QRect(210, 550, 181, 29))
    self.txtStockAlert.setObjectName("txtStockAlert")
    
    self.txtStockName = QtWidgets.QLineEdit(self.pageStock)
    self.txtStockName.setGeometry(QtCore.QRect(10, 480, 181, 29))
    self.txtStockName.setObjectName("txtStockName")
    
    self.label_95 = QtWidgets.QLabel(self.pageStock)
    self.label_95.setGeometry(QtCore.QRect(610, 0, 121, 17))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_95.setFont(font)
    self.label_95.setObjectName("label_95")
    
    self.stackedWidget.addWidget(self.pageStock)

    stockClass = stock(self)

    #  restarts form
    stockClass.cancel()

    #  connects a click on the table to the select the row
    self.listStock.clicked.connect(lambda: stockClass.click())
    self.listStock.doubleClicked.connect(lambda: stockClass.doubleClick())

    #  connecting the buttons
    self.btnStockCancel.clicked.connect(lambda: stockClass.cancel())
    self.btnSaveStock.clicked.connect(lambda: stockClass.save())
    self.txtStockSearch.textChanged.connect(lambda: stockClass.search())
