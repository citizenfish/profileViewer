#pip3 install PyQtChart
from PyQt5.QtWidgets import QApplication, QMainWindow
#from PyQt5.QtChart import QChart,QChartView,QLineSeries
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from PyQt5.QtChart import QChart,QChartView,QLineSeries

from PyQt5.QtGui import QPainter

import sys
import inspect
inspect.getfile(QChart)

class ChartArea(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Dave Test")
        self.resize(230,254)
        self.show()

        #QtChart Stuff
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)

        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    w = ChartArea()
    sys.exit(qApp.exec_())

