#!/usr/bin/env python
# Este primer script se encarga de extraer la información útil de la base de datos de drupal de guifi.net
# La extrae y la guarda en archivos, para su posterior tratado.

import MySQLdb
#import login
#import wikipedia

# Conectamos a la bbdd de guifi.net en la máquina virtual
db = MySQLdb.connect("192.168.1.30", "root", "guifi", "guifi")

# Consultamos las revisiones del nodo (artículo) 2704 (http://guifi.net/node/2704)
db.query("select timestamp from node_revisions where nid=2704 ORDER BY timestamp ASC")

r = db.store_result()

# añadimos a una lista todas las revisiones que tiene el artículo 2704, convertidas a unicode
timestamps = []
for i in range(0, int(r.num_rows())):
	timestamps.append(unicode(r.fetch_row()[0][0]))

# Hacemos una consulta por cada revisión para obtener el texto de cada una y lo guardamos a un archivo
#  que tiene como nombre <numero de nodo>_<numero de revisión>: Ej. 2704_1309466777
for t in timestamps:
	db.query("select body from node_revisions where nid=2704 and timestamp="+t)
	r = db.store_result()
	filename = "2704_"+t
	print "Writing to", filename
	fd = open(filename, "w")
	fd.write(unicode(r.fetch_row()[0][0]))
	fd.close()
