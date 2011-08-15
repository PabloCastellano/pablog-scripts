#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Este script extrae y mete en un diccionario {uid, name} de cada usuario

#BUG: problema con tildes en los nombres?!? con unicode() no funciona

import MySQLdb

# Conectamos a la bbdd de guifi.net en la máquina virtual
db = MySQLdb.connect("192.168.1.30", "root", "guifi", "guifi")

# Consultamos las revisiones del nodo (artículo) 2704 (http://guifi.net/node/2704)
db.query("select uid, name from users order by uid")

r = db.store_result()

# añadimos a una lista todas las revisiones que tiene el artículo 2704, convertidas a unicode
usersl = []
print int(r.num_rows())

for i in range(0, int(r.num_rows())):

	row = r.fetch_row()
	uid = row[0][0]
#	name = unicode(row[0][1])
	name = row[0][1]
	#print uid, name
	usersl.append((uid, name))
		
users = dict(usersl)

for k in users.keys():
	print k, users.get(k)
