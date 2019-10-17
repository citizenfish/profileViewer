import os
from qgis.PyQt import uic
from qgis.gui import (
    QgsDockWidget,
    QgsPanelWidgetStack,
    QgsPanelWidget
)

from qgis.PyQt.QtCore import (
    QUrl,
    QSettings,
    pyqtSignal
)

WIDGET_UI, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'lsDockWidget.ui'))


class lsDockWidget(QgsPanelWidget, WIDGET_UI):

    MODE_CANVAS = 'CANVAS'
    MODE_LAYOUT = 'LAYOUT'

    resizeWindow = pyqtSignal()

    def __init__(self, mode=MODE_CANVAS, parent=None, iface=None):

        super().__init__(parent)
        self.setupUi(self)
        if iface is None:
            from qgis.utils import iface
            self.iface = iface
        else:
            self.iface = iface

class lsDock(QgsDockWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr('Line Graph'))
        self.setObjectName('lsyDock')

        self.panel_stack = QgsPanelWidgetStack()
        self.setWidget(self.panel_stack)

        self.main_panel = lsDockWidget()
        self.panel_stack.setMainPanel(self.main_panel)
        self.main_panel.setDockMode(True)