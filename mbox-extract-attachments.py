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

# Notes (RFC 1341):
# The use of a Content-Type of multipart in a body part within another multipart entity is explicitly allowed. In such cases, for obvious reasons, care must be taken to ensure that each nested multipart entity must use a different boundary delimiter. See Appendix C for an example of nested multipart entities. 
# The use of the multipart Content-Type with only a single body part may be useful in certain contexts, and is explicitly permitted. 
# The only mandatory parameter for the multipart Content-Type is the boundary parameter, which consists of 1 to 70 characters from a set of characters known to be very robust through email gateways, and NOT ending with white space. (If a boundary appears to end with white space, the white space must be presumed to have been added by a gateway, and should be deleted.) It is formally specified by the following BNF

# Related RFCs: 2047, 2044, 1522

__version__ = 0.2
__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"


import mailbox
import base64
import os
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print "Usage: %s <mbox_file> [directory]" %sys.argv[0]
	sys.exit(0)

filename = sys.argv[1]
directory = os.path.curdir

if not os.path.exists(filename):
	print "File doesn't exist:", filename
	sys.exit(1)

if len(sys.argv) == 3:
	directory = sys.argv[2]
	if not os.path.exists(directory) or not os.path.isdir(directory):
		print "Directory doesn't exist:", directory
		sys.exit(1)

mb = mailbox.mbox(filename)
nmes = len(mb)
attachments = 0 #Count extracted attachment

os.chdir(directory)

for i in range(len(mb)):
	print "Analyzing message number", i
	mes = mb.get_message(i)
	
#	em = email.message_from_string(mes.as_string())
#	pay1=em.get_payloads()[1]
#	pay.get_filename()
#	pay1.get_params() #??¿?¿? No todos
# 	pay1.get_param("Content-Disposition") # Nada
#	pay1.get('Content-Disposition')
#	pay1.get_params(header='content-disposition')
#	[('attachment', ''), ('filename', '=?ISO-8859-1?Q?ACTA_DE_LA_REUNI=D3N_INTERREGIONAL_DE_DINAMIZACI=D3N_24_y_29?=\n =?ISO-8859-1?Q?_JULIO=2Edoc?=')]
#	email.header.decode_header(name1)

	# Puede tener adjunto sin ser multipart?!
	if not mes.is_multipart():
		print "Not multipart, skip"
		continue

	payloads = mes.get_payload()
	npay = len(payloads)
	for p in range(npay):
		has_attachment = True
		payl = payloads[p]
		content = payl.as_string()
		lines = content.splitlines()

		dict_headers = dict()
		for li in lines:
			if li == '':
				break
			headers = li.split("; ")
			if '' in headers:
				headers.remove('')
			for h in headers:
				values = h.split(": ")
				if len(values) == 1:
					values = h.split('=')
					if len(values) == 1:
						print "Aborting. Unknown format: "
						print h
						sys.exit(1)
				if '' in values:
					values.remove('')

				dict_headers[values[0].lstrip()] = values[-1]

		has_attachment = dict_headers.get('Content-Disposition') == 'attachment'

		if not has_attachment:
			print "No attachment, skip"
			continue

		filename = dict_headers.get("filename")
		if filename.startswith('"'):
			filename = filename[1:-1]
		
		if filename is None:
			filename = "unknown_%d_%d.txt" %(i, p)

		print "Writing %d bytes to %s" %(len(content), filename)
		#file1_idx = file1.find('\n\n')
		#file1 = file1[file1_idx+2:]
		try:
			#FIX: dont overwrite (e.g. signature.asc is very common)
			fp = open(filename, "w")
			fp.write(content)
		except IOError:
			print 'headers'
			print '---------'
			print dict_headers
			print "Aborted"
			sys.exit(2)
		finally:
			fp.close()	

		attachments = attachments + 1

		#fp = open(filename+"_decoded.txt", "w")
		#fp.write(base64.b64decode(content))
		#fp.close()

print "--------------"
print "Total attachments extracted: ", attachments

