from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from linestringgraph.lsDockWidget import lsDock


class lineStringGraph:
    def __init__(self, iface):
        self.iface = iface
        # This represents my dock widget class
        self.dock_widget = None

    def initGui(self):
        self.action = QAction('DAVE5', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

        self.dock_widget = lsDock.lsDock()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.hide()

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.information(None, 'Line String Graph', 'Do something useful here')
        self.dock_widget.show()