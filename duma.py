#!/usr/bin/env python
# -*- coding: utf-8 -*-
# duma.py - Accede a la DUMA (Universidad de Málaga) y muestra estadísticas - 18/febrero/2011
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
#

__version__ = 1.0
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

from mechanize import Browser
import re
from BeautifulSoup import BeautifulSoup
import getpass

CREDITOS_TOTAL = 337.5 # Ingeniería Informática Superior

print "duma.py - Accede a la DUMA (Universidad de Málaga) y muestra estadísticas"
print "Copyright (C) 2011 Pablo Castellano"
print "This program comes with ABSOLUTELY NO WARRANTY."
print "This is free software, and you are welcome to redistribute it under certain conditions."
print

br = Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.6.0')]
br.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
br.addheaders.append(('Accept-Language', 'en-us,en;q=0.5'))
br.addheaders.append(('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'))
br.addheaders.append(('Keep-Alive', '300'))
br.addheaders.append(('Connection', 'keep-alive'))
br.open("https://www.sci.uma.es/wuma/protegido/za/ficha.php?id=50643")

while br.title() != 'POST data':
	username = raw_input("Introduce tu usuario (del tipo xxxx@alu.uma.es): ")
	password = getpass.getpass("Introduce tu contraseña (no se mostrará): ")

	br.select_form(nr=0)
	br["username"] = username
	br["password"] = password
	br.submit()

	if br.title() != 'POST data':
		print "Usuario o contraseña incorrectos. Pruebe de nuevo."
	print

br.select_form(nr=0)
br.submit()
a = br.follow_link(url='ficha.php?id=50650')
lines = a.readlines()

lines2=[]
for l in lines:
	lines2.append(l.decode('latin-1'))

soup = BeautifulSoup(''.join(lines2))
td = soup.findAll('td')
exp=re.compile('<td class="sci_za">(.*?)</td>')

asignaturas = []
for i in range(0, len(td)/7):
	asig = exp.search(str(td[7*i]))
	anyo = exp.search(str(td[7*i+1]))
	conv = exp.search(str(td[7*i+2]))
	calif = exp.search(str(td[7*i+3]))
	tipo = exp.search(str(td[7*i+4]))
	c1 = exp.search(str(td[7*i+5]))
	c2 = exp.search(str(td[7*i+6]))
	asignaturas.append([str(asig.group(1)), str(anyo.group(1)), str(conv.group(1)), str(calif.group(1)), str(tipo.group(1)), str(c1.group(1)), str(c2.group(1))])

#Corrige los creditos vacios = 0
for x in asignaturas:
	if x[5] == '':
		x[5] = 0
	if x[6] == '':
		x[6] = 0

aprobados=0
notables=0
sobresalientes=0
matriculas=0
for x in asignaturas:
	print "%s %s %s %s %s %s %s" %(x[0].ljust(44), x[1].ljust(10), x[2].ljust(10), x[3].ljust(13), x[4].ljust(13), x[5], x[6])
	if x[3] == 'NOTABLE':
		notables = notables +1
	elif x[3] == 'APROBADO':
		aprobados = aprobados +1
	elif x[3] == 'SOBRESALIENTE':
		sobresalientes = sobresalientes +1
	elif x[3] == 'MATRIC.HONOR':
		matriculas = matriculas +1
	else:
		print 'VALOR DESCONOCIDO!', x[3]

suma = 0.0
for x in asignaturas:
	suma = suma + float(x[5]) + float(x[6])

print
print "Resumen (%s asignaturas):" %(len(asignaturas))
print "Aprobados:", aprobados
print "Notables:", notables
print "Sobresalientes:", sobresalientes
print "Matrículas de honor:", matriculas
print
print "Nota media:", (aprobados + notables*2 + sobresalientes*3 + matriculas*4)/float(len(asignaturas))
print "Créditos: %.2f de %.2f (%.2f%%)" %(suma, CREDITOS_TOTAL, suma*100.0/CREDITOS_TOTAL)
