#!/usr/bin/env python
# Este último script se encarga de meter los datos finalmente de la forma que queremos en la base de datos de mediawiki
#  usando consultas INSERT de mysql

#Habria que tener cuidado de no petar la base de datos enviando las consultas muy rápido (!)

# Funciones utiles de mediawiki:
# /usr/share/mediawiki/includes/Revision.php - insertOn, getPreviousRevisionId

# Tested with mediawiki 1.15.5-3

import datetime
import os
# This is ugly
#import MySQLdb
import web


def writeRev(text, pname)

	revTextID = db.insert('text', old_text=text, old_flags='utf-8')
	
	try:
		pid = db.select('page', what='page_id', where='page_title=$pname', vars=locals())[0]['page_id']
		revParentID = db.select('page', what='page_latest', where='page_id=$pid', limit=1, vars=locals())[0]['page_latest']
	except IndexError:
		#Pagename doesn't exist
		pid = 0
		revParentID = None
		
	uid = 1 # user id
	uname = "WikiSysop"# user name
	comm = "Migracion" # Esto no puede tener acentos ni cosas no estándares
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	pageLatest = db.insert('revision', rev_page=pid, rev_text_id=revTextID, rev_comment=comm, rev_minor_edit=0, rev_user=uid, rev_user_text=uname, rev_timestamp=now, rev_deleted=0, rev_len=len(text), rev_parent_id=revParentID)
	
	# Update latest page
	db.update('page', page_latest=pageLatest, where="page_id=$pid", vars=locals())
	
	# User changes
	userEditCount = db.select('user', what="user_editcount", where="user_id=$uid", vars=locals())[0]['user_editcount']
	db.update('user', where="user_id=$uid", user_editcount=userEditCount+1, vars=locals())
	db.update('user', where="user_id=$uid", user_touched=now, vars=locals())
	
	# Invalidate cache
	db.delete('objectcache', where="1=1")
	
	
	
if __name__ == "__main__":
	# Connect to database
	#db = MySQLdb.connect("localhost", "wikiguifi", "guifi", "wiki_guifilocal")
	db = web.database(dbn="mysql", db="wiki_guifilocal", user="wikiguifi", pw="guifi")

	start_from = "2704_1282534026"
	revs_dir = "2704"
	rev_files = os.listdir(revs_dir)

	i = 0
	while rev_files[0] != start_from: 
		rev_files = rev_files[1:]
		i+=1

	for r in rev_files:
		rev_file = os.path.join(revs_dir, r)
		fd = open(os.path.join(rev_file))
		txt = unicode(fd.read())
		fd.close()
		print "Writing rev number", r
		writeRev(txt)


