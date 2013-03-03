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
__version__ = '0.3'
__date__ = "03/03/2013"

import datetime
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import web
import _mysql  # _mysql.OperationalError
from shutil import copy

# MySQL stuff
DB_NAME = 'drupalmigracion'
DB_USER = 'root'
DB_PASSWD = ''
DB_HOST = 'localhost'
DB_PREFIX = 'inconspablo_'  # leave blank '' if none
BLOG_AUTHOR = 'Pablo Castellano'
CANONICAL_URL = 'http://lainconscienciadepablo.net'

NID_DONT_MIGRATE = [48, 50, 52, 62, 129, 130, 132]

# Template stuff
STATIC_FILES = ['combined.20120830.css', '_pygments.css']
TEMPLATES_FILES = ['layout.html']
PANDOC_PATH = '/usr/bin/pandoc'
LINK_PATH = '/tmp/drupal2rst'
RUNRST_PATH = '/home/pablo/src/rstblog/ve/bin/run-rstblog'
MIGRATE_UNPUBLISHED = True  # Migrate status=0
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


def writeTitleRST(fp, title):
    """
    ===========
    Write title
    ===========
    """
    fp.write('\n' + '=' * len(title) + '\n')
    fp.write(title.encode('utf-8'))
    fp.write('\n' + '=' * len(title) + '\n\n')


def writeTags(fp, tagnames):
    """
    tags: [tag1, tag2, tag3]
    """
    if len(tagnames) > 0:
        fp.write('tags: [')
        fp.write(tagnames[0])
        for tag in tagnames[1:]:
            fp.write(', ')
            fp.write(tag)
        fp.write(']\n')


def writeHtmltoRST(fp, body):
    rstcode = html2rst(body.encode('utf-8'))
    fp.write(rstcode)


def getTitleFrom(title):
    title = title.lower()
    title = title.replace(' ', '-')
    title = title.replace('/', '-')
    title = title.replace(':', '')
    title = title.replace(';', '')
    title = title.replace('#', '')
    title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore')
    """
    title = title.replace('á','a')
    title = title.replace('é','e')
    title = title.replace('í','i')
    title = title.replace('ó','o')
    title = title.replace('ú','u')
    """
    return title

tstart = datetime.datetime.now()
print 'rst-to-drupal.py v%s' % __version__
print 'Migrate from Drupal 6.26 (and possibly others) to rstblog'
print 'Copyright (C) 2013 Pablo Castellano <pablo@anche.no>'
print

db = web.database(dbn="mysql", db=DB_NAME, user=DB_USER, pw=DB_PASSWD, host=DB_HOST)

try:
    if db.ctx:
        print 'Connected to database'
except _mysql.OperationalError, e:
    print 'Error connecting to database:', e
    sys.exit(1)
except:
    print 'Unknown error'
    sys.exit(1)

print 'Temporary folder:', TMPPATH

if MIGRATE_UNPUBLISHED:
    nodes = db.select(NODES_TABLE, what="nid,vid,type,title,created,status", order="nid ASC")
    unpublishednodes = db.select(NODES_TABLE, what="nid", where='status=0')
    print 'Found %d nodes in database that will be migrated soon' % len(nodes)
    print 'Note that %d of those are unpublished and will be migrated too' % len(unpublishednodes)
else:
    nodes = db.select(NODES_TABLE, what="nid,vid,type,title,created,status", where='status=1', order="nid ASC")
    print 'Found %d nodes in database that will be migrated soon' % len(nodes)

# Tags: keep them in ALL_TAGS dictionary
result = db.select(TERMS_D_TABLE, what='tid,name')
ALL_TAGS = {}
for tag in result:
    ALL_TAGS[tag['tid']] = tag['name'].encode('utf-8')

# Url aliases
# Remember: Cool uris don't change!
# TODO: what is 'pid' in this table??
aliases = db.select(URL_ALIAS_TABLE, what='src,dst')
# src = 'node/189' or 'taxonomy/term/159' or 'taxonomy/term/155/feed/feed' or 'user/1' or 'user/4/track' or 'user/4/track/feed'
alias_node_re = re.compile("^node/(\d+)")
alias_taxo_re = re.compile("^taxonomy/term/(\d+)(?:/feed/feed)?$")

NODE_ALIASES = {}
TAG_ALIASES = {}
for alias in aliases:
    src = alias['src'].encode('utf-8')
    if src.startswith('user/'):
        continue
    dst = alias['dst'].encode('utf-8')
    if alias_node_re.match(src) is not None:
        nid = int(alias_node_re.match(src).group(1))
        NODE_ALIASES[nid] = {'src': src, 'dst': dst}
    elif alias_taxo_re.match(src) is not None:
        tid = int(alias_taxo_re.match(src).group(1))
        TAG_ALIASES[tid] = {'src': src, 'dst': dst}
    else:
        print 'Skipping unknown alias: %s --> %s' % (src, dst)

fp_aliases = open('/tmp/drupal2rst.aliases', 'w')
# Nodes
for node in nodes:
    nid = node['nid']

    if nid in NID_DONT_MIGRATE:
        continue

    vid = node['vid']
    created = node['created']
    status = node['status']
    title = node['title']
    pagetitle = getTitleFrom(title)
    print 'Pagetitle:', pagetitle
    if status == 0:
        title += ' (unpublished)'
    # Get last revision of the node
    print 'Retrieving node %s (revision %s)' % (nid, vid)
    # We could retrieve the timestamp field but we use the creation of the node as timestamp
    rev = db.select(REVISIONS_TABLE, what="title,body,format", where='nid=%d and vid=%d' % (nid, vid))[0]
    body = rev['body']
    #format=4 -> filtered html
    #format=2 -> full html
    # Get the tags of the node
    tags = db.select(TERMS_N_TABLE, what='tid', where='nid=%d and vid=%d' % (nid, vid))
    tagnames = []
    for t in tags:
        tid = t['tid']
        tagnames.append(ALL_TAGS[tid])
    ts = datetime.datetime.fromtimestamp(created)
    # Deal with pages and blog posts
    if node['type'] == 'page':
        rstfilepath = os.path.join(TMPPATH, '%s.rst' % pagetitle)
    else:
        # type == 'story'
        rstpath = os.path.join(TMPPATH, str(ts.year), str(ts.month), str(ts.day))
        if not os.path.exists(rstpath):
            os.makedirs(rstpath)
        rstfilepath = os.path.join(rstpath, '%s.rst' % pagetitle)

    # Save html for debugging purposes :)
    #htmlfilepath = os.path.join(TMPPATH, '%s.html'%pagetitle)
    """
    htmlfilepath = rstfilepath + '.html'
    with open(htmlfilepath, 'w') as fp:
        fp.write(body.encode('utf-8'))
    """

    print 'html2rst:', rstfilepath
    with open(rstfilepath, 'w') as fp:
        writeTags(fp, tagnames)
        writeTitleRST(fp, title)
        writeHtmltoRST(fp, body)
    print 'Copy to folder:', rstfilepath

    if nid in NODE_ALIASES:
        url = '%s/%d/%d/%d/%s/' % (CANONICAL_URL, ts.year, ts.month, ts.day, pagetitle)
        fp_aliases.write(NODE_ALIASES[nid]['src'] + '\n')
        fp_aliases.write(NODE_ALIASES[nid]['dst'] + '\n')
        fp_aliases.write(url + '\n\n')
    else:
        print 'No alias for thiz node'

fp_aliases.close()

# Create basic config.yml
ymlfilepath = os.path.join(TMPPATH, 'config.yml')
with open(ymlfilepath, 'w') as fp:
    fp.write("""\
active_modules: [blog, tags, youtube, pygments]
author: "%s"
canonical_url: %s
modules:
  pygments:
    style: tango\
""" % (BLOG_AUTHOR, CANONICAL_URL))
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

print 'Building html'
p = subprocess.Popen([RUNRST_PATH, 'build', TMPPATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
with open('/tmp/drupal2rst_build.log', 'w') as fp:
    fp.write(p.communicate()[0])
print 'Saved build log to /tmp/drupal2rst_build.log'
print 'You can now run yourself the following command to start a basic webserver:'
print RUNRST_PATH, 'serve', TMPPATH
tend = datetime.datetime.now()
ttotal = tend - tstart
print 'Finished in %f seconds' % ttotal.total_seconds()
