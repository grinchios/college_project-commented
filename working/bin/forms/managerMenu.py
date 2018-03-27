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


def backupFiles(self):
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
