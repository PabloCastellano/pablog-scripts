#!/usr/bin/env python
# recoverWord.py - Recover corrupted Word 2006 files - 3/April/2012
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

# I don't know a shit about Word formats.
# This tool was useful trying to recover the text from a damaged .doc Microsoft Word file
# This file was really a .zip file with xml inside. The file document.xml in the 'word' folder had all the text and it said something about http://schemas.openxmlformats.org/markup-compatibility/2006 so I guess it should be the 2006 version.
# Use LibreOffice!


import xml.dom.minidom as MD
import sys
import zipfile

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.2
__date__ = "14/04/2012"

TEXT_FILE = "word/document.xml"

print "Recover corrupted Word 2006 files"
print "Copyright (C) 2012 Pablo Castellano"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it under certain conditions."
print

if len(sys.argv) != 2:
	print "Usage: %s <corrupted_file.doc>" %sys.argv[0]
	sys.exit(1)

f = zipfile.ZipFile(sys.argv[1])
s = f.read(TEXT_FILE)
f.close()

#Save for debug
#fp = open("document.xml", "w")
#fp.write(s)
#fp.close()

#tree = MD.parse(filename)
tree = MD.parseString(s)
nodes = tree.getElementsByTagName("w:t")

fp = open("document.txt", "w")

for i in nodes:
	s = i.childNodes[0].nodeValue.encode('utf-8') + '\n'
	fp.write(s)

fp.close()

print "I hope you got something useful in document.txt"
