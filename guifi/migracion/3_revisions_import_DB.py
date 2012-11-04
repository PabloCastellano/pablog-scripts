#!/usr/bin/env python
# Este último script se encarga de meter los datos finalmente de la forma que queremos en la base de datos de mediawiki
#  usando consultas INSERT de mysql

#Habria que tener cuidado de no petar la base de datos enviando las consultas muy rápido (!)

# Funciones utiles de mediawiki:
# /usr/share/mediawiki/includes/Revision.php - insertOn, getPreviousRevisionId

# Tested with mediawiki 1.15.5-3

import datetime
import os
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
	
	# Save recent changes
#	INSERT /* RecentChange::save WikiSysop */  INTO `recentchanges` (rc_timestamp,rc_cur_time,rc_namespace,rc_title,rc_type,rc_minor,rc_cur_id,rc_user,rc_user_text,rc_comment,rc_this_oldid,rc_last_oldid,rc_bot,rc_moved_to_ns,rc_moved_to_title,rc_ip,rc_patrolled,rc_new,rc_old_len,rc_new_len,rc_deleted,rc_logid,rc_log_type,rc_log_action,rc_params,rc_id) VALUES ('20110815160455','20110815160455','0','Jiji','0','0','2','1','WikiSysop','','5','4','0','0','','127.0.0.1','1','0','34','53','0','0',NULL,'','',NULL)	
	# Save log page
#	INSERT /* LogPage::saveContent WikiSysop */  INTO `logging` (log_id,log_type,log_action,log_timestamp,log_user,log_namespace,log_title,log_comment,log_params) VALUES (NULL,'patrol','patrol','20110815160455','1','0','Jiji','','5\n4\n1')	

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



# page_id
# SELECT /* LinkCache::addLinkObj WikiSysop */  page_id,page_len,page_is_redirect  FROM `page`  WHERE page_namespace = '0' AND page_title = 'Jijo'  LIMIT 1


# last revision (rev_parent_id)
# SELECT /* Revision::getPreviousRevisionId WikiSysop */  page_latest  FROM `page`  WHERE page_id = '3'  LIMIT 1


#
#		   19 Query	INSERT /* Revision::insertOn WikiSysop */  INTO `text` (old_id,old_text,old_flags) VALUES (NULL,'Esta es una pagina muy molona tia!\n\nYa te digo, tron.','utf-8')
#		   19 Query	INSERT /* Revision::insertOn WikiSysop */  INTO `revision` (rev_id,rev_page,rev_text_id,rev_comment,rev_minor_edit,rev_user,rev_user_text,rev_timestamp,rev_deleted,rev_len,rev_parent_id) VALUES (NULL,'2','5','','0','1','WikiSysop','20110815160455','0','53','4')
#		   19 Query	UPDATE /* Article::updateRevisionOn WikiSysop */  `page` SET page_latest = '5',page_touched = '20110815160455',page_is_new = '0',page_is_redirect = '0',page_len = '53' WHERE page_id = '2' AND page_latest = '4'
#		   19 Query	DELETE /* Article::updateRedirectOn WikiSysop */ FROM `redirect` WHERE rd_from = '2'
#		   19 Query	INSERT /* RecentChange::save WikiSysop */  INTO `recentchanges` (rc_timestamp,rc_cur_time,rc_namespace,rc_title,rc_type,rc_minor,rc_cur_id,rc_user,rc_user_text,rc_comment,rc_this_oldid,rc_last_oldid,rc_bot,rc_moved_to_ns,rc_moved_to_title,rc_ip,rc_patrolled,rc_new,rc_old_len,rc_new_len,rc_deleted,rc_logid,rc_log_type,rc_log_action,rc_params,rc_id) VALUES ('20110815160455','20110815160455','0','Jiji','0','0','2','1','WikiSysop','','5','4','0','0','','127.0.0.1','1','0','34','53','0','0',NULL,'','',NULL)
#		   19 Query	INSERT /* LogPage::saveContent WikiSysop */  INTO `logging` (log_id,log_type,log_action,log_timestamp,log_user,log_namespace,log_title,log_comment,log_params) VALUES (NULL,'patrol','patrol','20110815160455','1','0','Jiji','','5\n4\n1')
#		   19 Query	UPDATE /* User::incEditCount WikiSysop */  `user` SET user_editcount=user_editcount+1 WHERE user_id = '1'
#		   19 Query	UPDATE /* User::invalidateCache WikiSysop */  `user` SET user_touched = '20110815160500' WHERE user_id = '1'
#		   20 Query	DELETE /* MediaWikiBagOStuff::_doquery WikiSysop */ FROM `objectcache` WHERE keyname='wiki_guifilocal:pcache:idhash:2-0!1!0!!en!2'
#		   20 Query	INSERT /* MediaWikiBagOStuff::_doinsert WikiSysop */ IGNORE INTO `objectcache` (keyname,value,exptime) VALUES ('wiki_guifilocal:pcache:idhash:2-0!1!0!!en!2','uS�n�0��9_����\'m�5�K���n�T��=���5X8vd;-l��s\n�@���~���7c�X��(�ƂY��i]��K�jYƢz\r;�M,���Y4mfs�8�KZ�I�+�K��I��ƭ�<
#                                                                                                                        ��f�������F��j���4�c���K��)jሁF����\Z]�����K �n�c$�&���\\[�î��$B���&+��#t�қq���q���k��ɑ����A����w\r(+�������V�Nhu$��<��Y����?�\'?����\0y�nC����V��Z�$�.�dM�3Qn�ݰ4�a��0����O�D\r�hݐ�&	�N�dD���xF�{r�!�qU���;��6�pF��b	b�8e���>0��VeW���A����Q�G�c�N�1[,DG���]��#��._�ƶ�`,��K��hp��#/�LdGw��_O{�e�C��e�����\r���������P�%�oN}���/ ��^�R�ٟT��˥��\\���Xh�g�A��7J���z <W��݀q\'a�h�E��]�KU�.�R��^>��KaѾ}��Y��k�)�,�RL���','20110816160455')

#    creando pg nueva:
# 		   86 Query	SELECT /* Revision::fetchFromConds WikiSysop */  rev_id,rev_page,rev_text_id,rev_timestamp,rev_comment,rev_user_text,rev_user,rev_minor_edit,rev_deleted,rev_len,rev_parent_id,page_namespace,page_title,page_latest  FROM `page`,`revision`  WHERE page_namespace = '0' AND page_title = 'Jijo' AND (rev_id=page_latest) AND (page_id=rev_page)  LIMIT 1
#		   86 Query	BEGIN
#		   86 Query	INSERT /* Article::insertOn WikiSysop */ IGNORE INTO `page` (page_id,page_namespace,page_title,page_counter,page_restrictions,page_is_redirect,page_is_new,page_random,page_touched,page_latest,page_len) VALUES (NULL,'0','Jijo','0','','0','1','0.773300919514','20110815170226','0','0')
#		   86 Query	INSERT /* Revision::insertOn WikiSysop */  INTO `text` (old_id,old_text,old_flags) VALUES (NULL,'prueba id','utf-8')
#		   86 Query	SELECT /* Revision::getPreviousRevisionId WikiSysop */  page_latest  FROM `page`  WHERE page_id = '3'  LIMIT 1
#		   86 Query	INSERT /* Revision::insertOn WikiSysop */  INTO `revision` (rev_id,rev_page,rev_text_id,rev_comment,rev_minor_edit,rev_user,rev_user_text,rev_timestamp,rev_deleted,rev_len,rev_parent_id) VALUES (NULL,'3','8','Summary','0','1','WikiSysop','20110815170226','0','9','0')
#		   86 Query	UPDATE /* Article::updateRevisionOn WikiSysop */  `page` SET page_latest = '8',page_touched = '20110815170226',page_is_new = '1',page_is_redirect = '0',page_len = '9' WHERE page_id = '3' AND page_latest = '0'
#		   86 Query	DELETE /* Article::updateRedirectOn WikiSysop */ FROM `redirect` WHERE rd_from = '3'

