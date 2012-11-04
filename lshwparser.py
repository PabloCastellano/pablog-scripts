#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lshwparser.py - Parses the output of "lshw -xml" - 4/Nov/2012
# Copyright (C) 2012 Pablo Castellano <pablo@anche.no>
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

# Running lshw as root you also get the following details:
#   - Memory banks, its description and the module in it (if any)
#   - Hard disks, including model, serial number and partitions...

__author__ = "Pablo Castellano <pablo@anche.no>"
__version__ = 0.1
__license__ = "GNU GPLv3+"
__date__ = "04/11/2012"

from lxml import etree
import sys

if len(sys.argv) != 2:
	print "Usage: %s <filename.xml>" %sys.argv[0]
	sys.exit(1)

tree = etree.parse(sys.argv[1])
root = tree.getroot()

assert(root.xpath('/node/node[@id="core"]/description/text()')[0] == 'Motherboard')
nodes = {}

nodes['name'] = root.xpath('/node/@id')[0]

nodes['motherboard'] = {}
nodes['motherboard']['product'] = root.xpath('/node/node[@id="core"]/product/text()')[0]
nodes['motherboard']['vendor'] = root.xpath('/node/node[@id="core"]/vendor/text()')[0]
nodes['motherboard']['version'] = root.xpath('/node/node[@id="core"]/version/text()')[0]

ncores=int(root.xpath('/node/configuration/setting[@id="cpus"]/@value')[0])
nodes['cpu'] = {}    
ncache=2

nodes['cpu']['product'] = root.xpath('/node/node/node[@id="cpu:0"]/product/text()')[0]
nodes['cpu']['socket'] = root.xpath('/node/node/node[@id="cpu:0"]/slot/text()')[0]
nodes['cpu']['bits'] = root.xpath('/node/node/node[@id="cpu:0"]/width/text()')[0]
nodes['cpu']['clock'] = root.xpath('/node/node/node[@id="cpu:0"]/clock/text()')[0]
		
for n in range(ncores):
	nodes['cpu'][n] = {}
	nodes['cpu'][n]['cache'] = {}
	for nc in range(ncache):
		nodes['cpu'][n]['cache'][nc] = {}
		nodes['cpu'][n]['cache'][nc]['desc'] = root.xpath('/node/node/node[@id="cpu:0"]/node[@id="cache:%d"]/description/text()' %nc)[0]
		nodes['cpu'][n]['cache'][nc]['size'] = root.xpath('/node/node/node[@id="cpu:0"]/node[@id="cache:%d"]/size/text()' %nc)[0]
		nodes['cpu'][n]['cache'][nc]['slot'] = root.xpath('/node/node/node[@id="cpu:0"]/node[@id="cache:%d"]/slot/text()' %nc)[0]


nodes['memory'] = {}
nodes['memory']['size'] = root.xpath('/node/node/node[@id="memory"]/size/text()')[0]

nnetwork = 2
nodes['network'] = {}
for n in range(nnetwork):
	nodes['network'][n] = {}
	nodes['network'][n]['desc'] = root.xpath('//node[@id="network:%d"]/description/text()' %n)[0]
	nodes['network'][n]['product'] = root.xpath('//node[@id="network:%d"]/product/text()' %n)[0]
	nodes['network'][n]['dev'] = root.xpath('//node[@id="network:%d"]/logicalname/text()' %n)[0]
	nodes['network'][n]['mac'] = root.xpath('//node[@id="network:%d"]/serial/text()' %n)[0]
	nodes['network'][n]['driver'] = root.xpath('//node[@id="network:%d"]/configuration/setting[@id="driver"]/@value' %n)[0]
	

from pprint import pprint
pprint(nodes)
