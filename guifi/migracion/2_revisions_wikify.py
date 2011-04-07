#!/usr/bin/env python

import os

rev_files = os.listdir("2704u")

for r in rev_files:
	rev_file = os.path.join("2704u", r)
	wiki_file = os.path.join("2704w", r)
	print "Converting", rev_file
	command = "html2wiki --dialect MediaWiki " + rev_file + " > " + wiki_file
	os.system(command) 

## Muy lento por la API
