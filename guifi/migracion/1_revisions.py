#!/usr/bin/env python

import MySQLdb
#import login
#import wikipedia

db = MySQLdb.connect("localhost", "root", "guifi", "guifi")
db.query("select timestamp from node_revisions where nid=2704 ORDER BY timestamp ASC")

r = db.store_result()

timestamps = []
for i in range(0, int(r.num_rows())):
	timestamps.append(unicode(r.fetch_row()[0][0]))

for t in timestamps:
	db.query("select body from node_revisions where nid=2704 and timestamp="+t)
	r = db.store_result()
	filename = "2704_"+t
	print "Writing to", filename
	fd = open(filename, "w")
	fd.write(unicode(r.fetch_row()[0][0]))
	fd.close()

### html2wiki ###


