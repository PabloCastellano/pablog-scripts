#!/usr/bin/env python
# Este primer script se encarga de extraer la información útil de la base de datos de drupal de guifi.net
# La extrae y la guarda en archivos, para su posterior tratado.

import web
import MySQLdb

# Conectamos a la bbdd de guifi.net en la máquina virtual
db = web.database(dbn="mysql", db="guifi", user="root", pw="guifi", host="192.168.1.30")

# Consultamos las revisiones del nodo (artículo) 2704 (http://guifi.net/node/2704)
results = db.select('node_revisions', what="timestamp", where="nid=2704", order="timestamp ASC")

# añadimos a una lista todas las revisiones que tiene el artículo 2704, convertidas a unicode
timestamps = []
for r in results:
	timestamps.append(r['timestamp'])

# Hacemos una consulta por cada revisión para obtener el texto de cada una y lo guardamos a un archivo
#  que tiene como nombre <numero de nodo>_<numero de revisión>: Ej. 2704_1309466777
for t in timestamps:
	results = db.select('node_revisions', what="body", where="nid=2704 and timestamp=$t", vars=locals())
	filename = "2704_"+t
	print "Writing to", filename
	fd = open(filename, "w")
	fd.write(r['body'])
	fd.close()
