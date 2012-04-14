#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# lasexta_video_downloader.py - Download videos from lasexta.com
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

# Example encoded string: 7077f50772d81456186cf91ab66e6b8ec99250629a403fed91a4101a7dae78a2eb3e18f9ee6e9912b4809d74ca39b992ec1c7a3e422e92643de8eb5f1ec3ebf30e01a412a99c209f31d9dfad606a85d8f7bb8c557d95ebd95f0080744a40bccd505996bd5058106ff400ee3cd2a20929beee4ae3da536d3867bdc25f4083b267fd3ed24656761be8313dac245ccf0c07125079535739368d41
# Example url: http://www.lasexta.com/sextatv/veranodirecto/macrobotellon_en_madrid_mientras_el_papa_duerme/260233/6563
# Example url_list: http://www.lasexta.com/sextatv/salvados/completos/salvados__domingo__25_de_septiembre/501473/1

# TODO: rtmpdump -A and -B parameters should be used to download the specific portion of video but it doesn't work for me
# TODO: Parece que desde marzo de 2012 han dejado de alojar ellos mismos los vídeos (solo los nuevos, los antiguos siguen igual)
#       y ahora usan Akamai, que implementa varios sistemas de autenticación tal como se puede leer aqui:
#       http://www.akamai.com/dl/feature_sheets/FS_edgesuite_accesscontrol.pdf
#       Un ejemplo de este tipo de urls es:
# 	http://www.lasexta.com/sextatv/salvados/completos/salvados_en_cuba__recortando_la_revolucion/595863/1

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.6
__date__ = "14/04/2012"

RTMP_URL = "rtmp://vod.lasexta.com/vod/_definst_/salvados/sd/"
#"rtmp://vod.lasexta.com/vod/_definst_/salvados/sd/PPD0000884012601_SALVADOS_126_25_03_2012_21_31_47_Ipad.mp4"

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
			encoded_url = re.compile("^_urlVideo=([a-f0-9]+)").match(s).group(1)
			t = 1
			break
		n = l.find('<meta property="og:video"')
		if n != -1:
			l = l[n:]
			m = l.find('_url_list')
			s = l[m:]
			encoded_url = re.compile("^_url_list=([a-f0-9]+)").match(s).group(1)
			t = 2
			break
    
	f.close()
	
	if s is None or encoded_url is None:
		print "Sorry, no video url could be found!"
		sys.exit(1)
	
	return (encoded_url, t)


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


def decodeRTMP(url):
	if url.startswith("http://") or url.startswith("www") or url.startswith("lasexta"):
		(encoded_url, t) = parseUrl(url)
	elif not isHex(url):
		print "Wrong parameter."
		print "Usage: %s [URL|encoded string]" %sys.argv[0]
		sys.exit(1)
	else:
		(encoded_url, t) = (url, 1)
	
	c = ARC4.new("sd4sdfkvm234")
	plain_url = c.decrypt(HexToByte(encoded_url))

	if t==1:
		print plain_url
		filename = plain_url.split('?')[0].split('/')[-1]
		print
		print "Use rtmpdump to download:"
		print 'rtmpdump -m 300 -o %s -r "%s"' %(filename, plain_url)

	else: #url_list
#		print "URL intermedia: %s\n" %plain_url
		import xml.dom.minidom as MD
		f = urllib.urlopen(plain_url)
		xmlString = f.read()
		f.close()
		tree = MD.parseString(xmlString)
		nodesTitle = tree.getElementsByTagName('title')
		nodesUrl = tree.getElementsByTagName('url')
		nodesUrlHD = tree.getElementsByTagName('urlHD')

		# No todos los videos tienen version HD
		hayHD = nodesUrlHD != []
		versionAkamai = nodesUrl[0].childNodes[0].nodeValue.startswith('http')

		print "La url contiene varios %d videos:" %len(nodesUrl)
		for i in range(len(nodesUrl)):
			plain_url = nodesUrl[i].childNodes[0].nodeValue
			title = nodesTitle[i].childNodes[0].nodeValue.encode('utf-8')
			print "(%d/%d) Descripción: %s" %(i+1, len(nodesUrl), title)
			print plain_url
			filename = plain_url.split('?')[0].split('/')[-1]
			if versionAkamai:
				filename = plain_url.split('?')[0].split('/')[-2]
				plain_url = RTMP_URL + filename
				print plain_url
			print 'rtmpdump -m 300 -o %s -r "%s"' %(filename, plain_url)
			if hayHD and not versionAkamai:
				encoded_url = nodesUrlHD[i].childNodes[0].nodeValue
				c = ARC4.new("sd4sdfkvm234")
        			plain_urlHD = c.decrypt(HexToByte(encoded_url))
				filenameHD = plain_urlHD.split('?')[0].split('/')[-1]
				print plain_urlHD
				print 'VERSION HD:'
				print 'rtmpdump -m 300 -o %s -r "%s"' %(filenameHD, plain_urlHD)
			print

		if versionAkamai:
			print "Ten en cuenta que ahora lasexta.com usan un nuevo metodo para alojar los videos que no está soportado completamente por este script"
			print "La url que has introducido pertenece este tipo."

###
if __name__ == "__main__":
	
	print "LaSexta video downloader"
	print "Copyright (C) 2011-2012 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print
	
	if len(sys.argv) != 2:
		print "Usage: %s <URL|encoded string>" %sys.argv[0]
		sys.exit(0)
	
	decodeRTMP(sys.argv[1])
