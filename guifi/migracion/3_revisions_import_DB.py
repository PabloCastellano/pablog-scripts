#!/usr/bin/env python
# Este último script se encarga de meter los datos finalmente de la forma que queremos en la base de datos de mediawiki
#  usando consultas INSERT de mysql

#Habria que tener cuidado de no petar la base de datos enviando las consultas muy rápido (!)

import os
import MySQLdb

db = MySQLdb.connect("localhost", "wikiguifi", "guifi", "wiki_guifilocal")

start_from = "2704_1282534026"
revs_dir = "2704"
rev_files = os.listdir(revs_dir)

i = 0
while rev_files[0] != start_from: 
	rev_files = rev_files[1:]
	i = i+1

for r in rev_files:
	#page = wikipedia.Page(site, "Recortes")
	rev_file = os.path.join(revs_dir, r)
	fd = open(os.path.join(rev_file))
	txt = unicode(fd.read())
	fd.close()
	print "Writing rev number", r
	#page.put(txt)
	# INSERT(...)
