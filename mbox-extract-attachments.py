#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mbox-extract-attachments.py - Extract attachments from mbox files - 16/March/2012
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

__version__ = 0.1
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"


import mailbox
import base64
import os
import sys

if len(sys.argv) != 2:
	print "Usage: %s <mbox_file>" %sys.argv[0]
	sys.exit(0)

filename = sys.argv[1]

if not os.path.exists(filename):
	print "File doesnt exist:", filename
	sys.exit(1)

mb = mailbox.mbox(filename)
nmes = len(mb)

for i in range(len(mb)):
	print "Analyzing message number", i
	mes = mb.get_message(i)
	
	# Puede tener adjunto sin ser multipart?!
	if not mes.is_multipart():
		print "Not multipart, skip"
		continue

	payloads = mes.get_payload()
	npay = len(payloads)
	for p in range(npay):
		payl = payloads[p]
		content = payl.as_string()
		filename = "pay%d_%d.txt" %(i, p)
		print "Writing %d bytes to %s" %(len(content), filename)
		#file1_idx = file1.find('\n\n')
		#file1 = file1[file1_idx+2:]
		fp = open(filename, "w")
		fp.write(content)
		fp.close()

		#fp = open(filename+"_decoded.txt", "w")
		#fp.write(base64.b64decode(content))
		#fp.close()

