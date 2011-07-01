#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import re

if len(sys.argv) != 2:
	print "Uso: %s <archivo.csv>" %(sys.argv[0])
	sys.exit()

fd = open(sys.argv[1], "rb")
csv = csv.reader(fd)
paramigrar = []
total = 0
regexp = re.compile("http://guifi.net/node/(\d+)$")

for i in range(6):
	csv.next()

# Las líneas del CSV cuyo 4º campo != 'no', se guardan
try:
	while(True):
		l = csv.next()
		total = total + 1
		try:
			if l[3].lower() != 'no':
				l.pop(3) #Este campo ya no es útil
				l[0] = regexp.search(l[0]).group(1) #Sustituimos la url por el nid directamente
				paramigrar.append(l)
		except IndexError:
			print "-- Index Error --", l
except StopIteration:
	pass

fd.close()
print "Fin"

for l in paramigrar:
	print l
#	print l[1]

print
print "Se van a migrar", len(paramigrar), "de", total, "artículos."
print "¿Desea continuar? [S/n]"

A = sys.stdin.readline()
