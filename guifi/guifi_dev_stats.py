#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# guifi_dev_stats.py - Muestra un recuento del hardware utilizado en los nodos de una zona especificada como parámetro
# Copyright (C) 2011 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Ejemplos:
# Málaga provincia: http://guifi.net/guifi/cnml/21629/detail
# Málaga: http://guifi.net/guifi/cnml/26494/detail
# Guifi.net: http://guifi.net/guifi/cnml/3671/detail (>17MB)

# Run it like:
# $ python guifi_dev_stats.py <file> |sort| uniq -c | sort -n

__version__ = 1.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

import xml.dom.minidom as MD
import sys

if len(sys.argv) != 2:
	print "Usage: %s <detail_file>" %(sys.argv[0])
	sys.exit(1)
	
tree = MD.parse(sys.argv[1])
devices = tree.getElementsByTagName("device")

for dev in devices:
	typen = dev.getAttribute('type')
	if typen == 'radio':
		print dev.getAttribute("name")
