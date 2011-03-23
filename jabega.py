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

__version__ = 1.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

#http://www.crummy.com/software/BeautifulSoup/documentation.html
import urllib
#from string import find
import string
from sys import exit
from os import system
from BeautifulSoup import BeautifulSoup
import getpass

#############
def parseNombre(nom):
	i = string.find(nom, '>', 38) +2
	f = string.find(nom, '<', i) -1
	
	return nom[i:f]

def parseVencimiento(venc):
	i = string.find(venc, "VENCE")
	f =	string.find(venc, '<', i) -2
	r = string.find(venc, "patFuncRenewCount")

	if r != -1:
		#ha sido renovado...
		ir = string.find(venc, '>', f) +1
		fr = string.find(venc, '<', ir)
		return venc[i:f] + " (" + venc[ir:fr] + ")"
	
	return venc[i:f]

def parseSignatura(sig):
	i = string.find(sig, '>') +2
	f = string.find(sig, '<', i) -1

	return sig[i:f]

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

#TODO: saber pasar de resultSet a list... 

#soup.findAll(attrs={"class" : "patFuncBarcode"})
#porque class es palabra reservada de python, como name tambien... ;)

nombres = soup.findAll(attrs={"class" : "patFuncTitle"})
#
# [<td colspan="5" align="center" class="patFuncTitle">
# <strong>2 EJEMPLARES PRESTADOS</strong></td>, <td align="left" class="patFuncTitle"><a href="/patroninfo*spi/1145896/item&amp;1449832"> Análisis y diseño de algoritmos : un enfoque teórico y práctico / José Ignacio Pélaez Sánchez ; con  </a>
# <br />
# </td>, <td align="left" class="patFuncTitle"><a href="/patroninfo*spi/1145896/item&amp;1088057"> Estructura y diseño de computadores / David A. Patterson, John L. Hennessy, con la colaboración de J </a>
# <br />
# </td>]
#

vencimiento = soup.findAll("td", attrs={"class" : "patFuncStatus"})
#
# [<td align="left" class="patFuncStatus"> VENCE 19-05-09  <span class="patFuncRenewCount">Renovado 1 vez</span>
# </td>, <td align="left" class="patFuncStatus"> VENCE 18-05-09 
# </td>]
#

signatura = soup.findAll("td", attrs={"class" : "patFuncCallNo"})
#
# [<td align="left" class="patFuncCallNo"> EIF-2/PEL/ana  </td>, <td align="left" class="patFuncCallNo"> EIB-1/PAT/est,II Vol. 2 </td>]

librosPrestados = len(nombres)-2

if(librosPrestados <= 0):
	print 'No tienes libros en préstamo!!'
	exit(1)

assert(len(vencimiento) == librosPrestados)
assert(len(signatura) == librosPrestados)

print librosPrestados, "libros en préstamo\n"

#now regexp or string.find...
for i in range(librosPrestados):
#	print parseNombre(str(nombres[librosPrestados+i]))
	print parseNombre(str(nombres[librosPrestados+i+1]))
	print parseVencimiento(str(vencimiento[i]))
	print parseSignatura(str(signatura[i]))
	print
