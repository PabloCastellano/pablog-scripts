#!/usr/bin/env python
# Este último script se encarga de meter los datos finalmente de la forma que queremos en la base de datos de mediawiki
#  usando la librería pywikipedia. Este proceso puede resultar muy lento por una limitación de la API aunque se hackeable.

import login
import wikipedia
import os

login.main()

site = wikipedia.getSite()

start_from = "2704_1282534026"
revs_dir = "2704"
rev_files = os.listdir(revs_dir)

i = 0
while rev_files[0] != start_from: 
	rev_files = rev_files[1:]
	i = i+1

for r in rev_files:
	page = wikipedia.Page(site, "Recortes")
	rev_file = os.path.join(revs_dir, r)
	fd = open(os.path.join(rev_file))
	txt = unicode(fd.read())
	fd.close()
	print "Writing rev number", r
	page.put(txt)
