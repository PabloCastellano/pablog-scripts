#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wikiquoter.py - Extrae citas directas para es.wikiquote.org
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

# http://www.abc.es/20120413/sociedad/abci-wert-consejo-ministros-201204131341.html
# http://www.publico.es/espana/423455/wert-la-victoria-del-pp-no-fue-solo-por-mayoria-absoluta-sino-universal
# http://www.eleconomista.es/noticias/noticias/3780127/02/12/WertNo-estamos-para-gastar-40000-millones-de-euros-en-estudiantes-que-dejan-la-carrera-amedias.html
# http://www.cadenaser.com/sociedad/audios/wert-fuera-opositor-estaria-dando-saltos-alegria-han-restituido-temario-llevo-trabajando-anos/csrcsrpor/20120208csrcsrsoc_8/Aes/ #no viene fecha?

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.1
__date__ = "27/04/2012"


SUPPORTED_SITES = ('abc', 'publico', 'economista', 'cs')

import re
import sys
import urllib


def getCite(url, t):
	if not (url.startswith("http://") or url.startswith("www")):
		print "URL looks wrong :?"
		sys.exit(1)
	
	if t not in SUPPORTED_SITES:
		print "Unsupported site. Please choose one from:"
		print SUPPORTED_SITES
		return

	f = urllib.urlopen(url)

	ll = f.read()
	f.close()

	if t == 'abc':
		titulo = re.search('<title>(.*)</title>', ll).group(1).decode('latin-1')
		fecha = re.search('<div class="date">D&iacute;a (.*)( - <span>|</div>)', ll).group(1)
	elif t == 'publico':
		titulo = re.search('<title>(.*)</title>', ll).group(1)
		fecha = re.search('<span class="fecha">(.*)</span>', ll).group(1)
		fecha_act = re.search('Actualizado: <span class="fecha">(.*)</span>', ll).group(1)
	elif t == 'economista':
		titulo = re.search('<title>(.*)</title>', ll).group(1)
		fecha = re.search('<div class="f-fecha">(.*) -', ll).group(1)
	elif t == 'cs':
		titulo = re.search('<title>(.*) \| Sonido', ll).group(1).decode('latin-1')
		if url.endswith('/'): # No viene la fecha!! :?
			fecha = url.split('/')[-3][:8]
		else:
			fecha = url.split('/')[-2][:8]


	print "* \"-frase-\"\n** [%s %s], %s" %(url, titulo, fecha)


if __name__ == "__main__":
	
	print "Wikiquoter - Extrae citas directas para es.wikiquote.org"
	print "Copyright (C) 2011-2012 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print
	
	# type = abc, publico
	if len(sys.argv) != 3:
		print "Usage: %s <URL> <type>" %sys.argv[0]
		sys.exit(0)
	
	getCite(sys.argv[1], sys.argv[2])
