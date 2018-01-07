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

# Supported domains:
# * http://www.lasextanoticias.com
# * http://www.lasexta.com
# * Maybe others...

# Example encoded string: 7077f50772d81456186cf91ab66e6b8ec99250629a403fed91a4101a7dae78a2eb3e18f9ee6e9912b4809d74ca39b992ec1c7a3e422e92643de8eb5f1ec3ebf30e01a412a99c209f31d9dfad606a85d8f7bb8c557d95ebd95f0080744a40bccd505996bd5058106ff400ee3cd2a20929beee4ae3da536d3867bdc25f4083b267fd3ed24656761be8313dac245ccf0c07125079535739368d41
# Example url: http://www.lasexta.com/sextatv/veranodirecto/macrobotellon_en_madrid_mientras_el_papa_duerme/260233/6563
# Example url_list: http://www.lasexta.com/sextatv/salvados/completos/salvados__domingo__25_de_septiembre/501473/1

# TODO: rtmpdump -A and -B parameters should be used to download the specific portion of video but it doesn't work for me
# TODO: Parece que desde marzo de 2012 han dejado de alojar ellos mismos los vídeos (solo los nuevos, los antiguos siguen igual)
#       y ahora usan Akamai, que implementa varios sistemas de autenticación tal como se puede leer aqui:
#       http://www.akamai.com/dl/feature_sheets/FS_edgesuite_accesscontrol.pdf
#       Un ejemplo de este tipo de urls es:
# 	http://www.lasexta.com/sextatv/salvados/completos/salvados_en_cuba__recortando_la_revolucion/595863/1
#
#	Ademas el contenido esta en formato .f4f (Flash MP4 Video Fragment)
#	Mas info en: http://blogs.adobe.com/ktowes/2010/06/flash_player_101_http_dynamic.html
#	http://www.adobe.com/products/hds-dynamic-streaming.html
#
# 7704.107019           192.168.1.128   63.80.242.41    HTTP    487     GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag174?als=0.6,300,0.7,0,2053,1693,25.13,380,2,93,f,1037.82,2469.5,f,u,SHPFNCEPGIJK,2.6.8,93 HTTP/1.1
# 4472	19.507811	192.168.1.128	63.80.242.41	HTTP	494	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag346?als=246.94,300,1.54,0,1846,2231,25.42,1165,6,156,f,1823.49,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 5683	24.304801	192.168.1.128	63.80.242.41	HTTP	494	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag347?als=248.15,300,1.34,0,2292,2279,26.62,1165,6,156,f,1828.22,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 7018	29.460329	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag348?als=248.92,300,1.5,0,1975,2268,26.76,1165,6,156,f,1833.54,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 8530	35.100712	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag349?als=249.37,300,1.37,0,2568,2355,25.08,1175,6,156,f,1839.1,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 9995	39.883712	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag350?als=250.88,300,1.26,0,2121,2953,25.56,1175,6,156,f,1843.9,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 11307	44.668458	192.168.1.128	63.80.242.41	HTTP	494	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag351?als=252.01,300,1.68,0,2189,2425,25.81,1176,6,156,f,1848.77,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 12834	50.726115	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag352?als=252.02,300,1.53,0,1538,2214,13.5,1202,6,156,f,1854.24,2469.5,f,u,SHPFNCEPGIJK,2.6.8,156 HTTP/1.1
# 14175	55.614538	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag353?als=253.16,300,1.16,0,1749,2747,7.36,1262,6,157,f,1859.08,2469.5,f,u,SHPFNCEPGIJK,2.6.8,157 HTTP/1.1
# 15467	61.881159	192.168.1.128	63.80.242.41	HTTP	493	GET /z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag354?als=252.87,300,1.64,0,1555,1927,6.61,1347,6,157,f,1865.36,2469.5,f,u,SHPFNCEPGIJK,2.6.8,157 HTTP/1.1
#http://lasextavod-f.akamaihd.net/z/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4/0_e8775c2b4acd5464_Seg1-Frag174?als=0.6,300,0.7,0,2053,1693,25.13,380,2,93,f,1037.82,2469.5,f,u,SHPFNCEPGIJK,2.6.8,93
# rtmp://vod.lasexta.com/vod/_definst_/salvados/hd/PPD0000884012501_SALVADOS_125_18_03_2012_21_33_24_h264.mp4

# http://lasextavod-f.akamaihd.net/z/lasextanoticias/sd/eco10_20120412_1612583153.flv/manifest.f4m
# http://lasextavod-f.akamaihd.net/z/lasextanoticias/sd/eco10_20120412_1612583153.flv/manifest.f4m?hdcore=2.6.8
# http://lasextavod-f.akamaihd.net/z/lasextanoticias/sd/eco10_20120412_1612583153.flv/manifest.f4m?hdcore=2.6.8&g=HFQYTVWLTKMQ
#
# Anuncios:
# http://p.lasexta.com/2/sexta/noticias/videos/1438227006
# Otros:
# www.lasexta.com//media/swf/players/sextaon/assets/imgV2/controls/mosca.png
# www.lasexta.com//media/swf/players/sextaon/assets/imgV2/controls/btnPlay.png
# ...

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = '0.6.4'
__date__ = "07/01/2018"

RTMP_URL = "rtmp://vod.lasexta.com/vod/_definst_/salvados/sd/"
HTTP_URL = 'http://descarga.lasexta.com/salvados/sd/'
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
		versionAkamai = plain_url.startswith('http')
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
			print
			print "(%d/%d) Descripción: %s" %(i+1, len(nodesUrl), title)
			print plain_url
			filename = plain_url.split('?')[0].split('/')[-1]
			if versionAkamai:
				filename = plain_url.split('?')[0].split('/')[-2]
				plain_url = HTTP_URL + filename
				print plain_url
				print 'wget -c', plain_url
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

	if versionAkamai:
		print
		print "Ten en cuenta que ahora lasexta.com usan un nuevo metodo para alojar los videos que no está soportado completamente por este script"
		print "La url que has introducido pertenece este tipo."

###
if __name__ == "__main__":

	print "LaSexta video downloader v%s" %__version__
	print "Copyright (C) 2011-2012 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print

	if len(sys.argv) != 2:
		print "Usage: %s <URL|encoded string>" %sys.argv[0]
		sys.exit(0)

	decodeRTMP(sys.argv[1])
