from PyQt5 import QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *

from datetime import date, timedelta, datetime

class createCharts():
    def __init__(self, fromDate, toDate):
        self.fromDate = fromDate
        self.toDate = toDate

    def mostPopTreatment(self, appointments, treatments):
        tmpdict = {}
        #  adds each treatment type to the dictionary
        #  and increments on each occasion of it

        for i in range(len(appointments)):
            #  gets the id and name of the performed treatment to be displayed
            treatmentID = appointments[i][str(i)]['treatment']
            treatmentName = treatments[int(treatmentID)][treatmentID]['name']

            #  gets the appointment date for checking
            appointmentDate = appointments[i][str(i)]['date']

            #todo
            #  date validation
            if self.fromDate <= appointmentDate <= self.toDate:
                try:
                    tmpdict[treatmentName] += 1
                except:
                    tmpdict[treatmentName] = 1

        #  creates the list for the graph to display
        returnList = []

        #  initialises an inner list of
        #  [x value, y value]
        innerList = ['', 0]

        for treatment in list(tmpdict.keys()):
            innerList = [treatment, int(tmpdict[treatment])]
            returnList.append(innerList)

        return returnList

    def income(self, appointments):
        d1 = date(int(self.toDate[:4]), int(self.toDate[5:7]), int(self.toDate[8:]))
        d2 = date(int(self.fromDate[:4]), int(self.fromDate[5:7]), int(self.fromDate[8:]))

        delta = d1 - d2

        tmpdict = {}

        #  creates a dictionary of each day
        for i in range(delta.days + 1):
            tmpdict[(d2 + timedelta(days=i)).strftime('%Y-%m-%d')] = 0

        for i in range(len(appointments)):
            #  gets the appointment date for checking
            appointmentDate = appointments[i][str(i)]['date']
            appointmentPrice = appointments[i][str(i)]['cost']

            if self.fromDate <= appointmentDate <= self.toDate:
                tmpdict[appointmentDate] += appointmentPrice

        #  creates the list for the graph to display
        returnList = []

        #  initialises an inner list of
        #  [x value, y value]
        innerList = ['', 0]

        keys = list(tmpdict.keys())

        for treatment in keys:
            innerList = [treatment, int(tmpdict[treatment])]
            returnList.append(innerList)

        returnList = sorted(returnList, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))

        return returnList

    def outgoings(self, appointments, treatments):
        tmpdict = {}
        #  adds each treatment type to the dictionary
        #  and increments on each occasion of it

        # todo
        #  date validation
        for i in range(len(appointments)):
            #  gets the appointment date for checking
            appointmentDate = appointments[i][str(i)]['date']

            if self.fromDate <= appointmentDate <= self.toDate:
                #  gets the id and name of the performed treatment to be displayed
                treatmentID = appointments[i][str(i)]['treatment']
                stockUsed = treatments[int(treatmentID)][treatmentID]['stock']

                #  for each piece of stock used
                #  add total outgoing to the graph data
                for stock in stockUsed:
                    try:
                        stockName = stock[1]
                        stockPrice = float(stock[2])
                        stockAmount = float(stock[3])

                        tmpdict[stockName] += int(stockPrice) * int(stockAmount)
                    except:
                        tmpdict[stockName] = int(stockPrice) * int(stockAmount)

        #  creates the list for the graph to display
        returnList = []

        #  initialises an inner list of
        #  [x value, y value]
        innerList = ['', 0]

        for treatment in list(tmpdict.keys()):
            innerList = [treatment, int(tmpdict[treatment])]
            returnList.append(innerList)

        return returnList

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
        QSizePolicy.Expanding,
        QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
      
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        
    def update_graph(self, graphValues, rot, ha):
        #  Updates the graph with new letters frequencies
        self.canvas.ax.clear()

        #  initialises the xaxis labels
        xlabel = [graphValues[i][0] for i in range(len(graphValues))]
        
        for i in range(len(graphValues)):
            j = graphValues[i]
            
            #  j[0] = x position/label
            #  j[1] = y value to bar up to
            self.canvas.ax.bar(j[0], j[1])
            self.canvas.ax.set_xticks(xlabel)

            #  writes the xaxis labels on an angle
            self.canvas.ax.set_xticklabels(xlabel, rotation=rot, ha=ha)

        #  enable grid only on the Y axis
        self.canvas.ax.get_yaxis().grid(True)

        #  force an image redraw
        self.canvas.draw()
