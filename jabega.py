#!/usr/bin/env python
# -*- coding: utf-8 -*-
# jabega.py - Accede a Jábega (Universidad de Málaga) y renueva libros en alquiler - 16/Mayo/2009 03:56am
# Copyright (C) 2009 Pablo Castellano <pablo@anche.no>
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

__version__ = 2.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

#http://www.crummy.com/software/BeautifulSoup/documentation.html
import urllib
#from string import find
import re
from sys import exit
from BeautifulSoup import BeautifulSoup
import getpass

#############

print "jabega.py - Accede a Jábega (Universidad de Málaga) y muestra libros en alquiler"
print "Copyright (C) 2009 Pablo Castellano"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it under certain conditions."
print

name = raw_input("Introduce tu usuario (del tipo Apellidos, Nombre): ")
code = raw_input("Introduce tu DNI sin la letra: ")
pin = getpass.getpass("Introduce tu contraseña (no se mostrará): ")

params = urllib.urlencode({"name" : name, "code" : code, "pin" : pin, "submit" : "ENVIAR"})

try:
	f = urllib.urlopen("https://jabega.uma.es/patroninfo*spi/1145896/items", params)
except IOError:
	print "ERROR, compruebe su conexión a internet (proxy?)"
	exit(2)

lines = f.readlines()
f.close()

#print ''.join(lines)

soup = BeautifulSoup(''.join(lines))
#print soup.prettify()

#TODO: pasar de resultSet a list... 

#porque class es palabra reservada de python, como name tambien... ;)
nombres = soup.findAll(attrs={"class" : "patFuncTitle"})
vencimiento = soup.findAll("td", attrs={"class" : "patFuncStatus"})
signatura = soup.findAll("td", attrs={"class" : "patFuncCallNo"})

librosPrestados = len(nombres)-2

if(librosPrestados <= 0):
	print 'No tienes libros en préstamo!!'
	exit(1)

assert(len(vencimiento) == librosPrestados)
assert(len(signatura) == librosPrestados)

print librosPrestados, "libros en préstamo\n"

nombreExp=re.compile('<label for.*spi\"> (.*?) </a>')
vencimientoExp = re.compile('<td align=\"left\" class=\"patFuncStatus\"> (.*?) \n</td>')
signaturaExp = re.compile('<td align=\"left\" class=\"patFuncCallNo\"> (.*?)  </td>') 

#now regexp or string.find...
for i in range(librosPrestados):
	print nombreExp.search(str(nombres[librosPrestados+i+1])).group(1)
	print vencimientoExp.search(str(vencimiento[0])).group(1)
	print signaturaExp.search(str(signatura[0])).group(1)
	print
