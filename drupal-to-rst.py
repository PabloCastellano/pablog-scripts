#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# rst-to-drupal.py - Migrate from Drupal 6.26 (and possibly others) to rstblog
# Copyright (C) 2013 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# WARNING: This version is unfinished!!!

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.1
__date__ = "19/01/2013"

import datetime
import os
import subprocess
import sys
import tempfile
import web
import _mysql #_mysql.OperationalError
from shutil import copy

# MySQL stuff
DB_NAME = 'drupalmigracion'
DB_USER = 'root'
DB_PASSWD = ''
DB_HOST = 'localhost'
DB_PREFIX = 'inconspablo_' # leave blank '' if none

# Template stuff
STATIC_FILES = ['combined.20120830.css']
TEMPLATES_FILES = ['layout.html']
PANDOC_PATH = '/usr/bin/pandoc'
LINK_PATH = '/tmp/drupal2rst'
MIGRATE_UNPUBLISHED = True # Migrate status=0
TMPPATH = tempfile.mkdtemp(prefix='rst-drupal-')
STATIC_PATH = os.path.join(TMPPATH, 'static')
TEMPLATES_PATH = os.path.join(TMPPATH, '_templates')

REVISIONS_TABLE = DB_PREFIX + 'node_revisions'
NODES_TABLE = DB_PREFIX + 'node'
URL_ALIAS_TABLE = DB_PREFIX + 'url_alias'
FILES_TABLE = DB_PREFIX + 'files'
COMMENTS_TABLE = DB_PREFIX + 'comments'
TERMS_D_TABLE = DB_PREFIX + 'term_data'
TERMS_N_TABLE = DB_PREFIX + 'term_node'

# Converts HTML into RST using pandoc
def html2rst(htmlcode):
    p = subprocess.Popen([PANDOC_PATH, '--from=html', '--to=rst'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate(htmlcode)[0]

print 'rst-to-drupal.py - Migrate from Drupal 6.26 (and possibly others) to rstblog'
print 'Copyright (C) 2013 Pablo Castellano <pablo@anche.no>'
print

db = web.database(dbn="mysql", db=DB_NAME, user=DB_USER, pw=DB_PASSWD, host=DB_HOST)

try:
    if db.ctx != False:
        print 'Connected to database'
except _mysql.OperationalError, e:
    print 'Error connecting to database:', e
    sys.exit(1)
except:
    print 'Unknown error'
    sys.exit(1)

print 'Temporary folder:', TMPPATH

if MIGRATE_UNPUBLISHED:
    nodes = db.select(NODES_TABLE, what="nid,vid,type,title,created", order="nid ASC")
else:
    nodes = db.select(NODES_TABLE, what="nid,vid,type,title,created", where='status=1', order="nid ASC")

result = db.select(TERMS_D_TABLE, what='tid,name')
ALL_TAGS = {}
for tag in result:
    ALL_TAGS[tag['tid']] = tag['name'].encode('utf-8')

for node in nodes:
    nid = node['nid']
    vid = node['vid']
    print 'Retrieving node %s (revision %s)' %(nid, vid)
    rev = db.select(REVISIONS_TABLE, what="title,body,timestamp,format", where='nid=%d and vid=%d' %(nid,vid))[0]
    #format=4 -> filtered html
    #format=2 -> full html
    tags = db.select(TERMS_N_TABLE, what='tid', where='nid=%d and vid=%d'%(nid,vid))
    tagnames = []
    for t in tags:
        tid = t['tid']
        tagnames.append(ALL_TAGS[tid])
    ts = datetime.datetime.fromtimestamp(rev['timestamp'])
    if node['type']=='page':
        rstfilepath = os.path.join(TMPPATH, '%d.rst'%nid)
    else:
        # type == 'story'
        rstpath = os.path.join(TMPPATH, str(ts.year), str(ts.month), str(ts.day))
        if not os.path.exists(rstpath):
            os.makedirs(rstpath)
        rstfilepath = os.path.join(rstpath, '%d.rst'%nid)

    htmlfilepath = os.path.join(TMPPATH, '%d.html'%nid)
    with open(htmlfilepath, 'w') as fp:
        fp.write(rev['body'].encode('utf-8'))

    rstcode = html2rst(rev['body'].encode('utf-8'))
    print 'html2rst:', rstfilepath
    with open(rstfilepath, 'w') as fp:
        if len(tagnames) > 0:
            fp.write('tags: [')
            fp.write(tagnames[0])
            for tag in tagnames[1:]:
                fp.write(', ')
                fp.write(tag)
            fp.write(']\n')
        fp.write('\n')
        fp.write('='*len(node['title']))
        fp.write('\n')
        fp.write(node['title'].encode('utf-8'))
        fp.write('\n')
        fp.write('='*len(node['title']))
        fp.write('\n\n')
        fp.write(rstcode)
    print 'Copy to folder:', rstfilepath

# Create config.yml
ymlfilepath = os.path.join(TMPPATH, 'config.yml')
with open(ymlfilepath, 'w') as fp:
    fp.write("""\
active_modules: [blog, tags]
author: "Pablo Castellano"
canonical_url: http://lainconscienciadepablo.net\
""")
print 'Created basic config.yml'

# Copy templates
if len(TEMPLATES_FILES):
    os.mkdir(TEMPLATES_PATH)
    for f in TEMPLATES_FILES:
#        copy(f, TEMPLATES_PATH)
        copy(f, os.path.join(TEMPLATES_PATH, 'layout.html'))
    print 'Copied template(s)'

# Copy static files
if len(STATIC_FILES) > 0:
    os.mkdir(STATIC_PATH)
    for f in STATIC_FILES:
        copy(f, STATIC_PATH)
    print 'Copied static file(s)'

if os.path.islink(LINK_PATH):
    os.unlink(LINK_PATH)
os.symlink(TMPPATH, LINK_PATH)
