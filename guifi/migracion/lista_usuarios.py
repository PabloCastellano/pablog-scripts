#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Este script extrae y mete en un diccionario {uid, name} de cada usuario

#BUG: problema con tildes en los nombres?!? con unicode() no funciona

import web

# Conectamos a la bbdd de guifi.net en la máquina virtual
db = web.database(dbn="mysql", db="guifi", user="root", pw="guifi", host="192.168.1.30")

results = db.select('users', what='uid, name', order="uid")

usersl = []

for r in results:
	uid = r['uid']
	name = r['name']
	#print uid, name
	usersl.append((uid, name))
		
users = dict(usersl)

for k in users.keys():
	print k, users.get(k)

print
print "Total users:", len(results)
