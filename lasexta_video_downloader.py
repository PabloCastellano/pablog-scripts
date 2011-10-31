#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# lasexta_video_downloader.py - Download videos from lasexta.com
# Copyright (C) 2011 Pablo Castellano <pablo@anche.no>
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

# Example encoded string: 7077f50772d81456186cf91ab66e6b8ec99250629a403fed91a4101a7dae78a2eb3e18f9ee6e9912b4809d74ca39b992ec1c7a3e422e92643de8eb5f1ec3ebf30e01a412a99c209f31d9dfad606a85d8f7bb8c557d95ebd95f0080744a40bccd505996bd5058106ff400ee3cd2a20929beee4ae3da536d3867bdc25f4083b267fd3ed24656761be8313dac245ccf0c07125079535739368d41
# Example url: http://www.lasexta.com/sextatv/veranodirecto/macrobotellon_en_madrid_mientras_el_papa_duerme/260233/6563

# TODO: rtmpdump -A and -B parameters should be used to download the specific portion of video but it doesn't work for me
# TODO: Add suport for playlists like http://www.lasexta.com/sextatv/salvados/completos/salvados__domingo__25_de_septiembre/501473/1

__author__ = "Pablo Castellano <pablo@anche.no>"
__date__ = "22/08/2011"

from Crypto.Cipher import ARC4
import sys

import urllib
import re
from string import hexdigits


def parseUrl(url):
	f = urllib.urlopen(url)
	s = None
	
	for l in f.readlines():
		n = l.find("_urlVideo")
		if n != -1:
			s = l[n:]
			break
    
	f.close()
	
	if s == None:
		print "Sorry, no video url could be found!"
		sys.exit(1)
	
	return re.compile("^_urlVideo=([a-f0-9]+)").match(s).group(1)


# From the Internets
def HexToByte(hexStr):
	bytes = []
	hexStr = ''.join( hexStr.split(" ") )
	
	for i in range(0, len(hexStr), 2):
		bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
	
	return ''.join( bytes )


def isHex(hexStr):
	for c in hexStr:
		if c not in hexdigits:
			return False
	
	return True


def decodeRTMP(Str):
	if Str.startswith("http://") or Str.startswith("www") or Str.startswith("lasexta"):
		Str = parseUrl(Str)
	elif not isHex(Str):
		print "Wrong parameter."
		print "Usage: %s [URL|encoded string]" %sys.argv[0]
		sys.exit(1)
	
	c = ARC4.new("sd4sdfkvm234")
	d = c.decrypt(HexToByte(Str))
	
	print d
	print
	print "Use rtmpdump to download:"
	print 'rtmpdump -m 300 -o download.flv -r "%s"' %d


if __name__ == "__main__":
	
	print "LaSexta video downloader"
	print "Copyright (C) 2011 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print
	
	if len(sys.argv) != 2:
		print "Usage: %s [URL|encoded string]" %sys.argv[0]
		sys.exit(0)
	
	decodeRTMP(sys.argv[1])
