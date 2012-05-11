#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ondaazul_downloader.py - Download videos from www.ondaazulmalaga.es
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

# Example url: http://www.ondaazulmalaga.es/television/video/informativo-mediodia/11181

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.1
__date__ = "14/04/2012"

import sys
import urllib


def getURL(url):
	if not (url.startswith("http://") or url.startswith("www")):
		print "URL looks wrong :?"
		sys.exit(1)
	
	f = urllib.urlopen(url)

	ll = f.read()
	f.close()

	n = ll.find('_url_xml_datos')
	if n == -1:
		print "Error1"
		sys.exit(1)

	line = ll[n:]

	m = line.find('&')
	url2 = line[15:m]

#	print "URL intermedia: ", url2

	f = urllib.urlopen(url2)
	xmlstring = f.read()
	f.close()

	n = xmlstring.find('rtmp')
	xmlstring = xmlstring[n:]
	m = xmlstring.find('</url>')
	url3 = xmlstring[:m]

	filename = url3.split('/')[-1]

	print "Use rtmpdump to download:"
	print 'rtmpdump -m 300 -o %s -r "%s"' %(filename, url3)


if __name__ == "__main__":
	
	print "Onda Azul video downloader"
	print "Copyright (C) 2011-2012 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print
	
	if len(sys.argv) != 2:
		print "Usage: %s <URL>" %sys.argv[0]
		sys.exit(0)
	
	getURL(sys.argv[1])
