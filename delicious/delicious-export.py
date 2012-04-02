#!/usr/bin/env python
# -*- coding: utf-8 -*-
# delicious-export.py - Export your bookmarks from Delicious.com - 1/April/2012
# Copyright (C) 2012 Pablo Castellano <pablo@anche.no>
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
#

#### Configure
USERNAME = ''
PASSWORD = ''
### End configure

import mechanize
import re

__version__ = 0.2
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"

URL1 = 'https://delicious.com/login#'
DAT1 = 'username=%s&password=%s' %(USERNAME, PASSWORD)
URL2 = 'http://export.delicious.com/settings/bookmarks/export'
DAT2 = 'include_tags=yes&include_notes=yes'

req1 = mechanize.Request(URL1, DAT1)
res = mechanize.urlopen(req1)
print "Login... ", res.msg

ll = str(res.info()).splitlines()
cookies = ''

exp = re.compile('^Set-Cookie: (.*); Domain')
for l in ll:
	m = exp.match(l)
	if m is None:
		continue
	cookies = cookies + m.group(1) + "; "

cookies = cookies[:-2]

req2 = mechanize.Request(URL2, DAT2)
req2.add_header('Cookie', cookies)
res = mechanize.urlopen(req1)

print "Export...", res.msg

ll = res.readlines()

fp = open("delicious.html", "w")
fp.writelines(ll)
fp.close()

