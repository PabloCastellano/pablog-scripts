#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# guifi_stats4.py - Muestra por orden de creación los nodos de una zona especificada como parámetro
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

__version__ = 1.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

import xml.dom.minidom as MD
import sys

def NodesByDate(nodes):
	uberNodes = []
	for i in nodes:
		uberNodes.append((i.attributes["created"].value, i.attributes["title"].value, i.attributes["status"].value, i.attributes["id"].value))
		#print i.attributes["created"].value, i.attributes["title"].value

	#Ordena por el segundo parametro: fecha de creacion
	#print sorted(uberNodes, key=lambda d: d[1])
	uberNodes.sort()
	return uberNodes

def recuento(uN):
	lastdate = 0

	for i in uN:
		date1 = i[0].split()[0][0:-2]
		date2 = i[0].split()[0][-2:]
		if date1 > lastdate:
			print date1
			lastdate = date1
		
		if i[2] != "Planned":
			print i[2][0] + '   ' + date2 + '\t' + i[1] + '\thttp://guifi.net/node/' + i[3]
		else:
			print '    ' + date2 + '\t' + i[1] + '\t\thttp://guifi.net/node/' + i[3]


if len(sys.argv) != 2:
	print "Usage: %s <detail_file>" %(sys.argv[0])
	sys.exit(1)
	
tree = MD.parse(sys.argv[1])
nodes = tree.getElementsByTagName("node")

uberNodes = NodesByDate(nodes)
#print uberNodes

recuento(uberNodes)

