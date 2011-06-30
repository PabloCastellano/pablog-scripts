#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# guifi_search.py - Busca en la web de guifi.net
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

__version__ = 1.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

from BeautifulSoup import BeautifulSoup
import re
import sys
import urllib

#TODO :https
SEARCH_URL = "http://guifi.net/es/search/node/"
NODE_URL = "http://guifi.net/node/"

def guifi_search(node):
	url = SEARCH_URL + node + " type:guifi_node"
	f = urllib.urlopen(url)
	lines = f.readlines()
	f.close()
	soup = BeautifulSoup(''.join(lines))
	nodos = soup.findAll(attrs={"class" : "title"})

	nodosExp=re.compile('<a href=\"(.*?)\">(.*?)</a>')

	for no in nodos:
		print nodosExp.search(str(no)).group(2), nodosExp.search(str(no)).group(1)
	
def guifi_num_search(node):
	print node

if len(sys.argv) != 2:
	print "Usage: %s <node number of name>" %(sys.argv[0])
	sys.exit(1)

try:
	num = int(sys.argv[1])
	guifi_num_search(num)
except ValueError:
	guifi_search(sys.argv[1])


