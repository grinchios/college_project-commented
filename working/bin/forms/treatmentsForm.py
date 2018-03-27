# -*- coding: utf-8 -*-
#todo add  new table from add button and then add to file
import sys

sys.path = ['..'] + sys.path
sys.path = ['bin'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from autoComboBox import FilteringComboBox

import fileHandling
from validation import validate

class treatments():
    def __init__(self, ui_class):
        self.firstRun = True
        #  starts an object of the filehandling class
        self.file = fileHandling.fileHandling('database/priceList.json')
        self.stockFile = fileHandling.fileHandling('database/stock.json')

        #  sortValue is what field the table
        #  is sorted by on double click
        self.sortValue = 'id'

        self.fileContent = self.file.readFile()['data']

        self.tableData = self.file.readFile()['data']

        self.stockFile = self.stockFile.readFile()['data']

        self.stockTableData = []

        #  sets column titles
        self.columnTitles = ['ID',
                             'Name',
                             'Price']

        #  assigning the ui to a variable for use
        self.ui = ui_class

        #  threaded method to fill the table
        self.makeTable = self.fillTable(self.fileContent, self.file.readFile(), self.ui)

        #  set true on double click
        self.filter = False

        self.startTable()
        self.fillStockTable(fill=False)
        self.fillComboBox()

        self.firstRun = False

        #  signaling
        self.ui.btnSaveStock.clicked.connect(lambda: self.ui.valueChange)

    def fillStockTable(self, fill=True):
        #  fills the secondary table
        #  with the selected stock

        #  adds the new data into the treatmentstock list

        if self.firstRun is False and fill:
            #  initialising variables
            id = int(self.ui.txtTreatmentStockName.currentText().split(' ')[0])
            stockPrice = self.stockFile[id][str(id)]['price']
            price = float(self.ui.dsbTreatmentPrice.value() + (stockPrice * self.ui.dsbTreatmentStockAmount.value()))

            #  sets the price to the old price plus the new stock
            self.ui.dsbTreatmentPrice.setValue(price)

            #  appending without a new variable
            #  to avoid a pointer allocation error

            self.stockTableData.append([id,
                        self.stockFile[id][str(id)]['name'],
                        stockPrice,
                        str(self.ui.dsbTreatmentStockAmount.value())])

        #  creates the secondary table
        columnTitles = ['ID',
                        'Name',
                        'Price',
                        'Stock-to-use']

        #  row amount
        length = len(self.stockTableData)

        #  sets row and column amounts
        self.ui.listTreatmentStock.setRowCount(length)
        self.ui.listTreatmentStock.setColumnCount(len(columnTitles))
        self.ui.listTreatmentStock.setHorizontalHeaderLabels(columnTitles)

        for i in range(length):
            self.ui.listTreatmentStock.setItem(i, 0, QtWidgets.QTableWidgetItem(str(
                self.stockTableData[i][0])))

            self.ui.listTreatmentStock.setItem(i, 1, QtWidgets.QTableWidgetItem(
                self.stockTableData[i][1]))

            self.ui.listTreatmentStock.setItem(i, 2, QtWidgets.QTableWidgetItem(str(
                self.stockTableData[i][2])))

            self.ui.listTreatmentStock.setItem(i, 3, QtWidgets.QTableWidgetItem(
                self.stockTableData[i][3]))

    def fillComboBox(self):
        #  fills the combo box for stock selection
        #  tmparr is used to fill the combo box
        tmparr = []
        file = self.stockFile
        for i in range(len(self.stockFile)):

            id = int(list(file[i].keys())[0])

            #  fill the combo box
            tmparr.append(str(id)+'    '+str(file[id][str(id)]['name']))

        self.ui.txtTreatmentStockName.addItems(tmparr)

    def fillFields(self, rowNum):
        self.ui.txtTreatmentID.setText(str(list(self.tableData[rowNum].keys())[0]))

        self.ui.txtTreatmentName.setText(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['name'])

        self.ui.dsbTreatmentPrice.setValue(float(
            self.tableData[rowNum][str(list(self.tableData[rowNum].keys())[0])]['price']))

    def search(self):
        if self.filter:
            try:
                searchIndex = self.file.binSearch(
                    self.tableData, self.ui.txtTreatmentSearch.text(), self.searchTerm)

                self.fillFields(int(searchIndex))

            except TypeError:
                QMessageBox.about(self.ui, "Error", 'Field not found')

        else:
            QMessageBox.about(self.ui, "Error", 'Must double click on a field first to sort by')

    def checkFields(self, newField):
        #  interfacing with validation class

        #  treatment name
        val = validate.checkPresence(self.ui.txtTreatmentName.text(), 'Treatment name')
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  treatment price
        val = validate.checkRange(self.ui.dsbTreatmentPrice.value(), 0.00, 1000.00)
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.isFloat(self.ui.dsbTreatmentPrice.value())
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        #  treatment stock amounts
        val = validate.checkRange(self.ui.dsbTreatmentStockAmount.value(), 0.00, 1000.00)
        if val is not True: QMessageBox.about(self.ui, "Error", val); return False

        val = validate.isFloat(self.ui.dsbTreatmentStockAmount.value())
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

        ID = int(self.ui.txtTreatmentID.text())

        if ID != int(self.file.newID()):
            newField = False
        else:
            newField = True

        if self.checkFields(newField) is True:
            stockList = self.stockTableData

            #  creates a dictionary of the user for the file
            arrUser = {
                ID: {
                    'name': self.ui.txtTreatmentName.text(),
                    'price': self.ui.dsbTreatmentPrice.value(),
                    'stock': stockList
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

            self.stockTableData = []
            self.fillStockTable(fill=False)
            self.ui.valueChange.emit(4)

    def startTable(self):
        self.ui.listTreatments.update()

        #  put the file into a variable
        file = self.file.readFile()

        #  row amount
        rowNum = len(file['data'])

        #  sets row and column amounts
        self.ui.listTreatments.setRowCount(rowNum)
        self.ui.listTreatments.setColumnCount(len(self.columnTitles))
        self.ui.listTreatments.setHorizontalHeaderLabels(self.columnTitles)

        self.makeTable.start()

    def click(self):
        #  function allows user to pre fill boxes based on a selected row
        rows = sorted(set(index.row() for index in self.ui.listTreatments.selectedIndexes()))
        for row in rows:
            rowNum = int(row)
        self.fillFields(rowNum)

        #  empty the stock table
        self.stockTableData = []

        self.fillStockTable(fill=False)

        #  fill the file with the actual treatment stock
        id = str(list(self.tableData[rowNum].keys())[0])

        self.stockTableData = self.tableData[rowNum][id]['stock']

        self.fillStockTable(fill=False)

    def doubleClick(self):
        #  allows a column to be selected for sorting and searching
        columns = sorted(set(index.column() for index in self.ui.listTreatments.selectedIndexes()))

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

            self.ui.listTreatments.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(list(self.tableContent[i].keys())[0])))

            self.ui.listTreatments.setItem(i, 1, QtWidgets.QTableWidgetItem(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['name']))

            self.ui.listTreatments.setItem(i, 2, QtWidgets.QTableWidgetItem(str(
                self.tableContent[i][str(list(self.tableContent[i].keys())[0])]['price'])))

        def run(self):
            #  row amount
            rowNum = len(self.file['data'])
            for i in range(rowNum):
                self.fillTable(self.file['data'][i], i)

            self.ui.listTreatments.update()

    def cancel(self):
        #  clears significant fields and assigns new ID
        self.ui.txtTreatmentID.setText(str(self.file.newID()))
        self.ui.txtTreatmentName.setText('')
        self.ui.dsbTreatmentPrice.setValue(float(0))

        self.stockTableData = []
        self.fillStockTable(fill=False)

#  stock form
def createTreatmentsForm(self):

    #  decorator
    #  signaling
    @pyqtSlot(int)
    def handleSignal(val):
        if val == 3:
            treatmentClass.stockFile = fileHandling.fileHandling('database/stock.json')
            treatmentClass.stockFile = treatmentClass.stockFile.readFile()['data']
            treatmentClass.fillComboBox()

    self.pageTreatments = QtWidgets.QWidget()
    self.pageTreatments.setObjectName("pageStock")

    self.label_90 = QtWidgets.QLabel(self.pageTreatments)
    self.label_90.setGeometry(QtCore.QRect(0, 550, 21, 21))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_90.setFont(font)
    self.label_90.setObjectName("label_90") #£

    self.label_91 = QtWidgets.QLabel(self.pageTreatments)
    self.label_91.setGeometry(QtCore.QRect(680, 390, 67, 21))
    self.label_91.setObjectName("label_91") #search

    self.label_92 = QtWidgets.QLabel(self.pageTreatments)
    self.label_92.setGeometry(QtCore.QRect(0, 520, 121, 17))
    self.label_92.setObjectName("label_92") #price

    self.label_79 = QtWidgets.QLabel(self.pageTreatments)
    self.label_79.setGeometry(QtCore.QRect(210, 520, 151, 17))
    self.label_79.setObjectName("label_79") #stock amount to use

    self.label_80 = QtWidgets.QLabel(self.pageTreatments)
    self.label_80.setGeometry(QtCore.QRect(0, 390, 161, 17))
    self.label_80.setObjectName("label_80") #add new treatments

    self.label_85 = QtWidgets.QLabel(self.pageTreatments)
    self.label_85.setGeometry(QtCore.QRect(0, 455, 151, 17))
    self.label_85.setObjectName("label_85") #name

    self.label_82 = QtWidgets.QLabel(self.pageTreatments)
    self.label_82.setGeometry(QtCore.QRect(0, 420, 101, 17))
    self.label_82.setObjectName("label_82") #treatmentid

    self.label_93 = QtWidgets.QLabel(self.pageTreatments)
    self.label_93.setGeometry(QtCore.QRect(210, 455, 101, 17))
    self.label_93.setObjectName("label_93") #stock name

    self.btnTreatmentCancel = QtWidgets.QPushButton(self.pageTreatments)
    self.btnTreatmentCancel.setGeometry(QtCore.QRect(120, 590, 101, 29))
    self.btnTreatmentCancel.setObjectName("btnTreatmentCancel")
    self.btnTreatmentCancel.setEnabled(self.accessLevel)

    self.txtTreatmentID = QtWidgets.QLineEdit(self.pageTreatments)
    self.txtTreatmentID.setGeometry(QtCore.QRect(110, 420, 121, 29))
    self.txtTreatmentID.setToolTipDuration(-1)
    self.txtTreatmentID.setReadOnly(True)
    self.txtTreatmentID.setObjectName("txtTreatmentID")

    self.txtTreatmentSearch = QtWidgets.QLineEdit(self.pageTreatments)
    self.txtTreatmentSearch.setGeometry(QtCore.QRect(750, 390, 371, 29))
    self.txtTreatmentSearch.setObjectName("txtTreatmentSearch")

    self.btnSaveTreatment = QtWidgets.QPushButton(self.pageTreatments)
    self.btnSaveTreatment.setGeometry(QtCore.QRect(10, 590, 101, 29))
    self.btnSaveTreatment.setObjectName("btnSaveTreatment")
    self.btnSaveTreatment.setEnabled(self.accessLevel)

    self.dsbTreatmentPrice = QtWidgets.QDoubleSpinBox(self.pageTreatments)
    self.dsbTreatmentPrice.setGeometry(QtCore.QRect(23, 550, 151, 27))
    self.dsbTreatmentPrice.setReadOnly(True)
    self.dsbTreatmentPrice.setObjectName("dsbTreatmentPrice")

    self.listTreatments = QtWidgets.QTableWidget(self.pageTreatments)
    self.listTreatments.setGeometry(QtCore.QRect(0, 30, 1111, 351))
    self.listTreatments.setObjectName("listTreatments")
    self.listTreatments.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    self.txtTreatmentName = QtWidgets.QLineEdit(self.pageTreatments)
    self.txtTreatmentName.setGeometry(QtCore.QRect(0, 480, 181, 29))
    self.txtTreatmentName.setObjectName("txtTreatmentName")

    self.btnTreatmentAddStock = QtWidgets.QPushButton(self.pageTreatments)
    self.btnTreatmentAddStock.setGeometry(QtCore.QRect(230, 590, 101, 29))
    self.btnTreatmentAddStock.setObjectName("btnTreatmentAddStock")
    self.btnTreatmentAddStock.setEnabled(self.accessLevel)

    self.txtTreatmentStockName = FilteringComboBox(self.pageTreatments)
    self.txtTreatmentStockName.setGeometry(QtCore.QRect(210, 480, 181, 29))
    self.txtTreatmentStockName.setObjectName("txtTreatmentStockName")

    self.label_94 = QtWidgets.QLabel(self.pageTreatments)
    self.label_94.setGeometry(QtCore.QRect(400, 420, 181, 17))
    self.label_94.setObjectName("label_94") #stock to use

    self.listTreatmentStock = QtWidgets.QTableWidget(self.pageTreatments)
    self.listTreatmentStock.setGeometry(QtCore.QRect(400, 440, 711, 180))
    self.listTreatmentStock.setObjectName("listTreatmentStock")
    self.listTreatmentStock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    self.dsbTreatmentStockAmount = QtWidgets.QDoubleSpinBox(self.pageTreatments)
    self.dsbTreatmentStockAmount.setGeometry(QtCore.QRect(210, 550, 181, 29))
    self.dsbTreatmentStockAmount.setReadOnly(False)
    self.dsbTreatmentStockAmount.setObjectName("dsbTreatmentStockAmount")

    self.label_95 = QtWidgets.QLabel(self.pageTreatments)
    self.label_95.setGeometry(QtCore.QRect(0, 0, 121, 17))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_95.setFont(font)
    self.label_95.setObjectName("label_95") #treatments

    self.stackedWidget.addWidget(self.pageTreatments)

    treatmentClass = treatments(self)

    #  restarts form
    treatmentClass.cancel()

    #  connects a click on the table to the select the row
    self.listTreatments.clicked.connect(lambda: treatmentClass.click())
    self.listTreatments.doubleClicked.connect(lambda: treatmentClass.doubleClick())

    #  connecting the buttons
    self.btnTreatmentCancel.clicked.connect(lambda: treatmentClass.cancel())
    self.btnSaveTreatment.clicked.connect(lambda: treatmentClass.save())
    self.txtTreatmentSearch.textChanged.connect(lambda: treatmentClass.search())

    self.btnTreatmentAddStock.clicked.connect(lambda: treatmentClass.fillStockTable())

    #  signals
    self.valueChange.connect(handleSignal)
