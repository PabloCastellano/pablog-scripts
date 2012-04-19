#!/usr/bin/env python
# recoverOdt.py - Replace keywords in .odt files - 19/April/2012
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


import sys
import zipfile
import datetime

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.1
__date__ = "19/04/2012"

TEXT_FILE = "content.xml"

now = datetime.datetime.now()
FECHA = "%d de %d de %d" %(now.day, now.month, now.year)
CAMBIOS = {'%NOMBRE%':'Pablo', '%DIRECCION%':'Calle tal tal tal', '%FECHA%':FECHA}

print "Replace keywords in .odt files"
print "Copyright (C) 2012 Pablo Castellano"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it under certain conditions."
print

if len(sys.argv) != 2:
	print "Usage: %s <file.odt>" %sys.argv[0]
	sys.exit(1)

filename = sys.argv[1]

f = zipfile.ZipFile(filename, 'a', zipfile.ZIP_DEFLATED)

# nl = f.namelist()
# nl[3] == 'content.xml'
# ff = f.filelist[3].filename
# ff == 'content.xml'

s = f.read(TEXT_FILE)

for i in CAMBIOS.iteritems():
	s = s.replace(i[0], i[1])

f.writestr(TEXT_FILE, s)
f.close()

print "Done"
