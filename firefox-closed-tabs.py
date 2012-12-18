#!/usr/bin/env python
# -*- coding: utf-8 -*-
# firefox-closed-tabs.py - Show closed tabs in Firefox profile - 18/dic/2012
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

__author__ = "Pablo Castellano <pablo@anche.no>"
__version__ = 0.1
__license__ = "GNU GPLv3+"
__date__ = "18/12/2012"

import json
import sys
import os

DEFAULT_DIR = '%s/.mozilla/firefox/' %os.path.expanduser('~')
ow = os.walk(DEFAULT_DIR)
folders = ow.next()[1]
folders.remove('Crash Reports')

print 'firefox-closed-tabs.py - Show closed tabs in Firefox profile'
print 'Usage: %s [sessionstore.js file]' %sys.argv[0]
print

if len(sys.argv) == 2:
	FILENAME=sys.argv[1]
else:
    if len(folders) > 1:
        print 'I have found %d firefox profiles:' %len(folders)
        for i, folder in enumerate(folders):
            print '  %d: %s' %(i, folder.split('.')[1])
        opt = int(raw_input('Please choose a number: '))
        while (opt < 0 or opt > len(folders)-1):
            opt = int(raw_input('Invalid number. Please try again: '))
        FILENAME = os.path.join(DEFAULT_DIR, folders[opt], 'sessionstore.js')
    else:
        FILENAME = os.path.join(DEFAULT_DIR, folders[0], 'sessionstore.js')

print 'Using filename:', FILENAME

fp = open(FILENAME)
j = json.load(fp)
fp.close()

windows = j.get('_closedWindows')
#len(windows) == 3

c = windows[0]

# len(c) == 12

#for l in c:
#	print l
"""
cookies
_shouldRestore
title
tabs
selected
_closedTabs
extData
height
width
sizemode
screenY
screenX

c['tabs']
c['_closedTabs']
c['tabs'][0]['entries']
c['tabs'][0]['entries'][0]['title']
c['tabs'][0]['entries'][0]['url']
"""

print 'TABS:', len(c['tabs'])
num_e = 0
num_t = 0

for t in c['tabs']:
    num_t += 1
    print 'Tab num', num_t
    if len(t['entries']) > 1:
        # What happens here??
        pass
    for e in t['entries']:
        num_e += 1
        print e['url']

print 'ENTRIES:', num_e
