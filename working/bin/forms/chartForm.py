# -*- coding: utf-8 -*-

import sys

sys.path = ['..'] + sys.path

from PyQt5 import QtCore, QtGui, QtWidgets
from charts import MplWidget as chartClass
from charts import createCharts

from fileHandling import fileHandling

class graphCreation():
    def __init__(self, ui):
        self.ui = ui
        #  staff and stock aren't used in this class
        #  but left here for future developers
        self.staffFile = fileHandling('database/staff.json').readFile()['data']
        self.appointmentFile = fileHandling('database/appointments.json').readFile()['data']
        self.stockFile = fileHandling('database/stock.json').readFile()['data']
        self.treatmentFile = fileHandling('database/priceList.json').readFile()['data']

        self.fromDate = self.ui.dateChartFrom.date().toPyDate().strftime('%Y-%m-%d')
        self.toDate = self.ui.dateChartTo.date().toPyDate().strftime('%Y-%m-%d')

    def redoData(self):
        #  restarts the variables for file changes
        self.__init__(self.ui)

    def create(self):
        self.redoData()
        creater = createCharts(self.fromDate, self.toDate)

        graphType = self.ui.cmbChartType.currentText()

        if graphType == 'Most popular treatment':
            graphContent = creater.mostPopTreatment(self.appointmentFile, self.treatmentFile)
        elif graphType == 'Income':
            graphContent = creater.income(self.appointmentFile)
        elif graphType == 'Outgoing per stock type':
            graphContent = creater.outgoings(self.appointmentFile, self.treatmentFile)

        self.ui.widgetCharts.update_graph(graphContent, 40, 'right')

#  chart form
def createChartForm(self):
    self.pageCharts = QtWidgets.QWidget()
    self.pageCharts.setObjectName("pageCharts")
    
    self.label_4 = QtWidgets.QLabel(self.pageCharts)
    self.label_4.setGeometry(QtCore.QRect(20, 136, 17, 17))
    self.label_4.setObjectName("label_4")
    
    self.label_2 = QtWidgets.QLabel(self.pageCharts)
    self.label_2.setGeometry(QtCore.QRect(20, 26, 74, 17))
    self.label_2.setObjectName("label_2")

    self.cmbChartType = QtWidgets.QComboBox(self.pageCharts)
    self.cmbChartType.setGeometry(QtCore.QRect(20, 49, 191, 25))
    self.cmbChartType.setObjectName("cmbChartType")
    self.cmbChartType.addItem("")
    self.cmbChartType.addItem("")
    self.cmbChartType.addItem("")
    
    self.dateChartFrom = QtWidgets.QDateEdit(self.pageCharts)
    self.dateChartFrom.setGeometry(QtCore.QRect(20, 103, 191, 27))
    self.dateChartFrom.setCalendarPopup(True)
    self.dateChartFrom.setDate(QtCore.QDate(2018, 1, 1))
    self.dateChartFrom.setObjectName("dateChartFrom")
    
    self.dateChartTo = QtWidgets.QDateEdit(self.pageCharts)
    self.dateChartTo.setGeometry(QtCore.QRect(20, 159, 191, 27))
    self.dateChartTo.setCalendarPopup(True)
    self.dateChartTo.setDate(QtCore.QDate(2018, 1, 1))
    self.dateChartTo.setObjectName("dateChartTo")
    
    self.label_3 = QtWidgets.QLabel(self.pageCharts)
    self.label_3.setGeometry(QtCore.QRect(20, 80, 36, 17))
    self.label_3.setObjectName("label_3")
    
    self.btnChartCreate = QtWidgets.QPushButton(self.pageCharts)
    self.btnChartCreate.setGeometry(QtCore.QRect(20, 200, 191, 29))
    self.btnChartCreate.setObjectName("btnChartCreate")
    
    self.label_31 = QtWidgets.QLabel(self.pageCharts)
    self.label_31.setGeometry(QtCore.QRect(20, 0, 67, 17))
    
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    
    self.label_31.setFont(font)
    self.label_31.setObjectName("label_31")
    
    self.widgetCharts = chartClass(self.pageCharts)
    self.widgetCharts.setGeometry(QtCore.QRect(230, 10, 891, 671))
    self.widgetCharts.setObjectName("widgetCharts")
    
    self.stackedWidget.addWidget(self.pageCharts)

    createGraph = graphCreation(self)

    self.btnChartCreate.clicked.connect(lambda: createGraph.create())

    #  update the date values
    self.dateChartFrom.dateChanged.connect(lambda: createGraph.redoData())
    self.dateChartTo.dateChanged.connect(lambda: createGraph.redoData())
