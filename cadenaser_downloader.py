#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cadenaser_downloader.py - Descarga audios de la web Cadena Ser - 10/abril/2012
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

#Ejemplos:
#http://www.cadenaser.com/espana/audios/baltasar-garzon-pierde-vigilancia-estatica-domicilio-hoy-hoy-2012/csrcsrpor/20120404csrcsrnac_2/Aes/
#http://www.cadenaser.com/espana/audios/rajoy-hay-presidente-gobierno-va-dar-cara-va-esconder/csrcsrpor/20120410csrcsrnac_11/Aes/
# NOT FOUND: http://www.cadenaser.com/espana/audios/aguirre-puedes-autorizar-puta-mierda/csrcsrpor/20100129csrcsrnac_8/Aes/

#TODO: Guardar la info ID3...
#
#

__author__ = "Pablo Castellano <pablo@anche.no>"
__version__ = 0.1
__license__ = "GNU GPLv3+"
__date__ = "14/04/2012"

import mechanize
import re
import sys
import os
	
print "cadenaser_downloader.py - Descarga audios de la web Cadena Ser"
print "Copyright (C) 2012 Pablo Castellano"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it under certain conditions."
print
	
if len(sys.argv) != 2:
	print "Usage: %s <url>" %sys.argv[0]
	sys.exit(1)

url = sys.argv[1]
req = mechanize.Request(url)
res = mechanize.urlopen(req)
#body = res.read()
bodyl = res.readlines()
#i = body.find('obj.urlHTML5')
exp = re.compile('^obj.urlHTML5 = \'(.*)\';$')

for l in bodyl:
	m = exp.match(l)
	if m is None:
		continue
	else:
		break

if m is None:
	print "No funcionó"
	sys.exit(1)

dl_url = m.group(1) 

print "\nLa url de descarga es la siguiente:\n%s\n" %dl_url
c = raw_input("¿Desea iniciar la descarga? [S/n]: ")

if c.lower() == 'n':
	sys.exit(0)

req = mechanize.Request(dl_url)
res = mechanize.urlopen(req)

filename = dl_url.split('/')[-1]

if os.path.exists(filename):
	print "El archivo \'%s\' ya se encuentra en este directorio. Se cancela la descarga." %filename
	sys.exit(1)

print 'Descargando %s...' %filename,

fp = open(filename, 'w')
fp.write(res.read())
fp.close()

print 'completado!'
