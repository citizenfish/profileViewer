# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileViewer
                                 A QGIS plugin
 View profile of lines with Z values
                             -------------------
        begin                : 2016-04-09
        copyright            : (C) 2016 by Dave Barter
        email                : dave@nautoguide.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load profileViewer class from file profileViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .profileViewer import profileViewer
    return profileViewer(iface)
