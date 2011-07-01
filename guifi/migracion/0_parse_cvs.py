#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import re

csv = csv.reader(open("book.csv", 'rb'))
paramigrar = []
total = 0
regexp = re.compile("http://guifi.net/node/(\d+)$")

for i in range(6):
	csv.next()

# Las líneas del CSV cuyo 4º campo != 'No', se guardan
try:
	while(True):
		l = csv.next()
		total = total + 1
		try:
			if l[3].lower() != 'no':
				l.pop(3)
				l[0] = regexp.search(l[0]).group(1)
				paramigrar.append(l)
		except IndexError:
			print "-- Index Error --", l
except StopIteration:
	pass

print "Fin"

for l in paramigrar:
	print l
#	print l[1]

print
print "Se van a migrar", len(paramigrar), "de", total, "artículos."
print "¿Desea continuar?"

A = sys.stdin.readline()
