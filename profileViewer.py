# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileViewer
                                 A QGIS plugin
 View profile of lines with Z values
                              -------------------
        begin                : 2016-04-09
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Dave Barter
        email                : dave@nautoguide.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *
from osgeo import ogr
import math
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from profileViewer_dialog import profileViewerDialog
import os.path


class profileViewer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'profileViewer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = profileViewerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Profile Viewer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'profileViewer')
        self.toolbar.setObjectName(u'profileViewer')



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('profileViewer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/profileViewer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Profile Viewer'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Profile Viewer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
       
        #Get the current selected feature
        layer = self.iface.activeLayer()
        selected_feature = layer.selectedFeatures()[0]
        
        #Read its geometry
        qgisgeom = selected_feature.geometry()
        wkb = qgisgeom.asWkb()
        
        #Convert to ogr
        ogr_geom_wkb = ogr.CreateGeometryFromWkb(wkb)

        #First Height Value
        last_point = ogr_geom_wkb.GetPoint(0)
        distance = 0
        plot_x = [0]
        plot_y = [last_point[2]]
        for i in range(1,ogr_geom_wkb.GetPointCount()):
            pt = ogr_geom_wkb.GetPoint(i)
            #We had better be in EPSG:27700
            #distance = distance + math.sqrt((pt[0] - last_point[0])**2 + (pt[1] - last_point[1])**2)
            distance = distance + 20
            #plot_points.append([distance,pt[2]])
            plot_x.append(distance)
            plot_y.append(pt[2])

        self.scene = QtGui.QGraphicsScene(self.dlg)
        figure =  plt.figure()
        ax   =  figure.add_subplot(111)
        ax.hold(False)
        ax.set_title("Dodgy Elevation Graph")


        x_sm = np.array(plot_x)
        y_sm = np.array(plot_y)
        x_smooth = np.linspace(x_sm.min(), x_sm.max(), 400)
        y_smooth = spline(plot_x, plot_y, x_smooth)

        ax.plot(plot_x,plot_y,'*',x_smooth, y_smooth, 'red')

        canvas = FigureCanvas(figure)
        self.scene.addWidget(canvas)
        self.dlg.graphicsView.setScene(self.scene)

        self.dlg.show()
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
           pass
    