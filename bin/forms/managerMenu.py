# -*- coding: utf-8 -*-

import os
import sys

#  allows referencing of other forms
sys.path = ['..'] + sys.path
sys.path = ['bin'] + sys.path

#  used for calculating one week ago
from datetime import date, timedelta, datetime

#  gui libs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QHeaderView

#  backing up library
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#  used for the tables only
from charts import MplWidget as chartClass
from charts import createCharts
from fileHandling import fileHandling

'''
S4
Staff should be able to add comments that show up on the manager's main homepage. Adding to the appointment when it’s made or edited to be completed.
S5
The main tables need to be stored online. Storing the files in a dated folder to backup online.
P1
Creating graphs for key data. The graphs on the managers panel will be the weeks intake and a bar chart for stock which will load with the page. There will be graphs for the most common treatment, income for a time period and outgoings per stock type these will be on a separate page with buttons to generate them.
P3
Backing up data. The manager will have the option to create a backup from their panel to cloud storage.
P4
Using table view boxes to store data that can be selected for use. This was mentioned in #9 of input validation, they’ll be used for efficiency of data inputs, and improving the user interface. These will be filled with the use of threads.
P6
Creating stock alerts to show on the managers panel, so if stock is too low then the manager is informed.
P7
Staff members can add comments to appointments that the manager can view but they can’t unless they made the appointment.
O1
The managers panel will include items from processing objectives #1, #3, #6, #7 for rapid observation of data.
O3
The backups will be of all the data files and it must be put into a file that’s dated for ease of data lookup.
O4
Data will be shown in tables, all the graphs on the manager panel will load with the page but any on the main chart form will have buttons to generate them.
'''

def backupFiles(self):
	'''
	S5
	The main tables need to be stored online. Storing the files in a dated folder to backup online.
	'''
	'''
	P3
	Backing up data. The manager will have the option to create a backup from their panel to cloud storage.
	'''
    zipFiles = ''
    zipName = datetime.now().strftime("%Y-%m-%d") + '.zip'
    for fileName in os.listdir('database/'):
        if '.json' in fileName:
            zipFiles += 'database/' + fileName + ' '
    os.system('zip -q database/archives/' + zipName + ' ' + zipFiles)

    #  connects to google drive
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    #  uploads recent file
    uploader = drive.CreateFile()
    uploader.SetContentFile('database/archives/' + zipName)
    uploader.Upload()

    QMessageBox.about(self, "Backup", "Files have been uploaded")

class graphCreation():
	'''
	P1
	Creating graphs for key data. The graphs on the managers panel will be the weeks intake and a bar chart for stock which will load with the page. There will be graphs for the most common treatment, income for a time period and outgoings per stock type these will be on a separate page with buttons to generate them.
	'''
	'''
	O4
	Data will be shown in tables, all the graphs on the manager panel will load with the page but any on the main chart form will have buttons to generate them.
	'''
    def __init__(self, ui):
        self.ui = ui
        self.appointmentFile = fileHandling('database/appointments.json').readFile()['data']
        self.treatmentFile = fileHandling('database/priceList.json').readFile()['data']

        self.fromDate = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.toDate = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    def create(self):
        creater = createCharts(self.fromDate, self.toDate)

        graphContent = creater.mostPopTreatment(self.appointmentFile, self.treatmentFile)

        self.ui.widgetTop.update_graph(graphContent, 0, 'center')

        graphContent = creater.income(self.appointmentFile)

        #  rotated so the year doesn't show
        self.ui.widgetBottom.update_graph(graphContent, 30, 'center')

def updateNotifications(ui, notifications):
	'''
	S4
	Staff should be able to add comments that show up on the manager's main homepage. Adding to the appointment when it’s made or edited to be completed.
	'''
	'''
	P4
	Using table view boxes to store data that can be selected for use. This was mentioned in #9 of input validation, they’ll be used for efficiency of data inputs, and improving the user interface. These will be filled with the use of threads.
	'''
	'''
	P6
	Creating stock alerts to show on the managers panel, so if stock is too low then the manager is informed.
	'''
	'''
	P7
	Staff members can add comments to appointments that the manager can view but they can’t unless they made the appointment.
	'''
	'''
	O4
	Data will be shown in tables, all the graphs on the manager panel will load with the page but any on the main chart form will have buttons to generate them.
	'''
    #  adds notifications to the manager menu
    columnTitles = ['Message']

    rowNum = len(notifications)

    ui.listNotifications.setRowCount(rowNum)
    ui.listNotifications.setColumnCount(len(columnTitles))
    ui.listNotifications.setHorizontalHeaderLabels(columnTitles)
    ui.listNotifications.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    for i in range(rowNum):
        ui.listNotifications.setItem(
            i, 0, QtWidgets.QTableWidgetItem(notifications[i]))

    ui.listNotifications.update()

#  manager menu page
def createManagerMenu(self):
	'''
	O1
	The managers panel will include items from processing objectives #1, #3, #6, #7 for rapid observation of data.
	'''
    self.pageManagerMenu = QtWidgets.QWidget()
    self.pageManagerMenu.setObjectName("pageManagerMenu")

    self.listNotifications = QtWidgets.QTableWidget(self.pageManagerMenu)
    self.listNotifications.setGeometry(QtCore.QRect(10, 70, 490, 590))
    font = QtGui.QFont()
    font.setFamily("Arial")
    self.listNotifications.setFont(font)
    self.listNotifications.setObjectName("listNotifications")
    self.listNotifications.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    self.notifications = []
    self.addNotifications = updateNotifications
    
    self.label_5 = QtWidgets.QLabel(self.pageManagerMenu)
    self.label_5.setGeometry(QtCore.QRect(10, 0, 141, 17))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_5.setFont(font)
    self.label_5.setObjectName("label_5")

    self.label_notifications = QtWidgets.QLabel(self.pageManagerMenu)
    self.label_notifications.setGeometry(QtCore.QRect(10, 45, 141, 17))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_notifications.setFont(font)
    self.label_notifications.setObjectName("label_notifications")
    
    self.label_7 = QtWidgets.QLabel(self.pageManagerMenu)
    self.label_7.setGeometry(QtCore.QRect(300, 0, 141, 17))
    font = QtGui.QFont()
    font.setFamily("Arial Black")
    self.label_7.setFont(font)
    self.label_7.setObjectName("label_7")
    
    self.btnBackup = QtWidgets.QPushButton(self.pageManagerMenu)
    self.btnBackup.setGeometry(QtCore.QRect(300, 30, 161, 29))
    font = QtGui.QFont()
    font.setFamily("Arial")
    self.btnBackup.setFont(font)
    self.btnBackup.setObjectName("btnBackup")
    
    self.widgetTop = chartClass(self.pageManagerMenu)
    self.widgetTop.setGeometry(QtCore.QRect(500, 10, 621, 330))
    self.widgetTop.setObjectName("widgetTop")
    
    self.widgetBottom = chartClass(self.pageManagerMenu)
    self.widgetBottom.setGeometry(QtCore.QRect(500, 335, 621, 330))
    self.widgetBottom.setObjectName("widgetBottom")
    
    self.stackedWidget.addWidget(self.pageManagerMenu)

    #  fill the graphs
    graphs = graphCreation(self)
    graphs.create()

    self.btnBackup.clicked.connect(lambda : backupFiles(self))
