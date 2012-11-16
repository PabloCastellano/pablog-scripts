#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rss-zone.py - Download CNML and generate RSS feed with latest nodes
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
#
# TODO:
# * Growth bar graphs
# * Subscription: send e-mail with updates (instantly, weekly...)
# * Find removed nodes, updated nodes... and every change

__version__ = 1.1
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__date__ = "16/11/2012"

from datetime import datetime
import urllib
import sys
import xml.dom.minidom as MD

#Just set the following variable:
CNML_ID = '21629' # Málaga provincia

# ~~~~~~~~~~~~~~~~~~~~~~

CNML_URL = 'https://guifi.net/guifi/cnml/%s/detail' %CNML_ID
ZONE_URL = 'https://guifi.net/node/%s' %CNML_ID
CNML_FILE = '%s_detail.cnml' %CNML_ID
RSS_HEAD = """\
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title>Guifi.net RSS for zone "%s" (%s)</title>
    <link>%s</link>
    <description></description>
    <language>en</language>\n"""
RSS_BODY = """\
    <item>
        <title>%s (%s)</title>
        <link>https://guifi.net/node/%s</link>
        <description>New node "%s" at (%s, %s)</description>
        <pubDate>%s</pubDate>
        <dc:creator>rss-zone.py</dc:creator>
    </item>\n"""
RSS_FOOT = '</channel>\n</rss>\n'


def getNodesSortedByDate(tree):
	nodes = tree.getElementsByTagName('node')
	sorted_nodes = []
	for node in nodes:
		this_node = dict()
		for attr in ['created','title','id','lat','lon']:
			this_node[attr] = node.getAttribute(attr)
		"""
		if node.childNodes == []:
			this_node['desc'] = ''
		else:
			this_node['desc'] = node.childNodes[0].nodeValue
		"""
		sorted_nodes.append(this_node)
	sorted_nodes.sort()
	sorted_nodes.reverse()
	return sorted_nodes


def printRSSNodes(nodes, limit=20, fp=sys.stdout):
	fp.write(RSS_HEAD %('Málaga provincia', CNML_ID, ZONE_URL))
	for node in nodes[:limit]:
		(date1, time1) = node['created'].split()
		nodedate = datetime(int(date1[:4]),int(date1[4:6]),int(date1[-2:]), int(time1[:2]), int(time1[2:]))
		fp.write(RSS_BODY %(node['title'], node['id'], node['id'], node['title'], node['lat'], node['lon'], nodedate.strftime('%a, %d %b %Y %H:%M:00 +0000')))
	fp.write(RSS_FOOT)


sys.stderr.write('Guifi.net rss-zone.py - Generate RSS feed with latest nodes\n')
sys.stderr.write('Usage: %s [output_file.rss] [output_file.log]\n\n' %sys.argv[0])
sys.stderr.write('#1: Downloading CNML from %s\n' %CNML_URL)
fUrl = urllib.urlopen(CNML_URL)
content = fUrl.read()
fUrl.close()
fLocal = open(CNML_FILE, 'w')
fLocal.write(content)
fLocal.close()
sys.stderr.write('#2: Accesing to CNML data\n')
tree = MD.parse(CNML_FILE)
nodes = getNodesSortedByDate(tree)
if len(sys.argv) >= 2:
	limit = len(nodes)
	sys.stderr.write('#3: Generating RSS feed (saving %d nodes to %s)\n\n' %(limit, sys.argv[1]))
	# Write to file
	fp = open(sys.argv[1], 'w')
	printRSSNodes(nodes, limit, fp)
	fp.close()
else:
	limit = 20
	sys.stderr.write('#3: Generating RSS feed (stdout, limit=%d)\n\n' %limit)
	printRSSNodes(nodes, limit)

sys.stderr.write('Result:\n')
try:
	fp = open('rss_zone_last_update','r')
	last_node_id = fp.read()
	fp.close()
	for newnodes, node in enumerate(nodes):
		if node['id'] == last_node_id:
			break
	print '  Nodes since last run:', str(newnodes)
except IOError:
	print '  First time running this script'
	newnodes = len(nodes)

last_node = nodes[0]
# Save log and number of nodes created since last run
if len(sys.argv) == 3:
	fp = open(sys.argv[2], 'a')
else:
	fp = open('rss_zone.log', 'a')
fp.write('-- Run on %s --\n' %str(datetime.today()))
fp.write('Last node "%s" (https://guifi.net/node/%s) created on %s\n' %(last_node['title'], last_node['id'], last_node['created']))
fp.write('%d new nodes since last update\n' %newnodes)
for node in nodes[:newnodes]:
	fp.write('    - %s\n' %node['title'])
fp.write('\n')
fp.close()
sys.stderr.write('  Last node "%s" (https://guifi.net/node/%s) created on %s\n' %(last_node['title'], last_node['id'], last_node['created']))
sys.stderr.write('  %d new nodes since last update:\n' %newnodes)
for node in nodes[:newnodes]:
	sys.stderr.write('    - %s\n' %node['title'])
# Save last node created
fp = open('rss_zone_last_update','w')
fp.write(last_node['id'])
fp.close()
