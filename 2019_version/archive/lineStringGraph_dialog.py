# -*- coding: utf-8 -*-
"""
/***************************************************************************
 lineStringGraphDialog
                                 A QGIS plugin
 This plugin displays a linestring with Z values as a graph
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-09-27
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Dave Barter
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

import os

from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'lineStringGraph_dialog_base.ui'))


class lineStringGraphDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(lineStringGraphDialog, self).__init__(parent)
        self.setupUi(self)
