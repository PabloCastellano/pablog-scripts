#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wikiquoter.py - Extrae citas directas para es.wikiquote.org
# Copyright (C) 2012-2013 Pablo Castellano <pablo@anche.no>
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
# http://www.europapress.es/economia/noticia-alonso-pp-advierte-sindicatos-manifestaciones-no-crean-empleos-les-invita-trabajar-serio-20120211141205.htm
# http://www.lasprovincias.es/20120516/mas-actualidad/politica/corts-financiacion-local-201205161333.html
# http://www.elcorreo.com/vizcaya/20120516/local/azkuna-comercio-tiene-espabilar-201205161922.html
# http://www.laverdad.es/murcia/20120519/local/region/pedro-chico-tenemos-conseguir-201205191141.html
# http://www.20minutos.es/noticia/1459072/0/de-guindos/nacionalizacion-bankia/futuro-privatizacion/
# http://www.elconfidencial.com/espana/2013/02/13/el-informe-de-la-udef-contra-mato-deja-al-director-de-la-policia-al-borde-de-la-destitucion-114805/
# http://www.eldiario.es/politica/Gobierno-informado-Suiza-Barcenas-escandalo_0_100790133.html
# http://economia.elpais.com/economia/2013/02/13/actualidad/1360744450_237029.html
# http://www.elmundo.es/elmundo/2013/02/13/espana/1360771883.html

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = '1.2'
__date__ = "13/02/2013"
__miscdate__ = "20/05/2012 #LaCaixaEsMordor"


SUPPORTED_STYLES = ('15mpedia', 'eswikiquote')
SUPPORTED_SITES = {'abc': 'Diario ABC', 'publico': 'Diario Público', 'economista': 'El Economista', 'cs': 'Cadena Ser', 'ep': 'Europa Press',
                   'lp': 'Las Provincias', 'correo': 'El Correo', 'lv': 'La Verdad', '20m': '20 Minutos', 'ec': 'El Confidencial',
                   'eldiario': 'eldiario.es', 'pais': 'El País', 'mundo': 'El Mundo'}
STYLE = '15mpedia'
DEBUG = False

import datetime
import locale
import re
import sys
import urllib

#locale.setlocale(locale.LC_ALL, '')
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')


def print_debug(text):
    if DEBUG:
        print text


def guessType(url):
    if url.startswith('http://www.abc.es'):
        return 'abc'
    elif url.startswith('http://www.publico.es'):
        return 'publico'
    elif 'eleconomista.es' in url:
        return 'economista'
    elif url.startswith('http://www.cadenaser.com'):
        return 'cs'
    elif url.startswith('http://www.europapress.es'):
        return 'ep'
    elif url.startswith('http://www.lasprovincias.es'):
        return 'lp'
    elif url.startswith('http://www.elcorreo.com'):
        return 'correo'
    elif url.startswith('http://www.laverdad.es'):
        return 'lv'
    elif url.startswith('http://www.20minutos.es'):
        return '20m'
    elif url.startswith('http://www.elconfidencial.com'):
        return 'ec'
    elif url.startswith('http://www.eldiario.es'):
        return 'eldiario'
    elif 'elpais.com' in url:
        return 'pais'
    elif url.startswith('http://www.elmundo.es'):
        return 'mundo'
    else:
        return None


def formatResult(url, titulo, site, fecha):
    global STYLE
    if STYLE not in SUPPORTED_STYLES:
        print 'WARNING: STYLE "%s" not valid. Using eswikiquote by default'
        STYLE = 'eswikiquote'

    if STYLE == '15mpedia':
        result = "* [%s %s] (%s)" % (url, titulo, fecha.strftime('%d de %B de %Y'))
    elif STYLE == 'eswikiquote':
        result = "* \"-frase-\"\n** Fuente: [%s %s], %s, %s" % (url, titulo, site, fecha.strftime('%d de %B de %Y'))

    return result


def getCite(url, t=None):
    if t is not None and t not in SUPPORTED_SITES.keys():
        print "Unsupported site. Please choose one from:"
        print SUPPORTED_SITES.keys()
        return

    if not (url.startswith("http://") or url.startswith('https://') or url.startswith("www")):
        print "URL looks wrong :?"
        sys.exit(1)

    if t is None:
        t = guessType(url)
        if t is None:
            print "Type couldn't be guessed. Please specify it manually."
            print SUPPORTED_SITES.keys()
            sys.exit(1)
        else:
            print_debug('Guessing url type... %s (%s)' % (SUPPORTED_SITES[t], t))

    f = urllib.urlopen(url)

    ll = f.read()
    f.close()

    if t == 'abc':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-9].decode('latin-1')
        fecha = re.search('<div class="date">D&iacute;a (.*)( - <span>|</div>)', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y - <span>%H.%Mh</span>')
    elif t == 'publico':
        titulo = re.search('<title>(.*)</title>', ll).group(1)
        fecha = re.search('<span class="fecha">(.*)</span>', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y %H:%M')
#       fecha_act = re.search('Actualizado: <span class="fecha">(.*)</span>', ll).group(1)
    elif t == 'economista':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-15]
        try:
            fecha = re.search('<div class="f-fecha">(.*) -', ll).group(1)
            fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        except:
            try:
                fecha = re.search('<small>EcoDiario.es \| (.*) - .*<span', ll).group(1)
                fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
            except:
                titulo = titulo.decode('utf-8')
                fecha = re.search('<span class="l-fecha">(.*)<span', ll).group(1).split(',')[1].strip()
                fecha = datetime.datetime.strptime(fecha, '%d de %B de %Y')
    elif t == 'cs':
        titulo = re.search('<title>(.*) \| (Noticia|Sonido)', ll).group(1).decode('latin-1')
        if url.endswith('/'):  # No viene la fecha!! :?
            fecha = url.split('/')[-3][:8]
        else:
            fecha = url.split('/')[-2][:8]
        fecha = datetime.datetime.strptime(fecha, '%Y%m%d')
    elif t == 'ep':
        titulo = re.search('<title>\r\n\t(.*)\r\n</title>', ll).group(1).decode('latin-1')
        import HTMLParser
        htmlparser = HTMLParser.HTMLParser()
        titulo = htmlparser.unescape(titulo)
        fecha = url.split('/')[-1].split('-')[-1][:8]
        fecha = datetime.datetime.strptime(fecha, '%Y%m%d')
    elif t == 'lp':
    #   titulo = re.search('<div class="mpdato">(.*)</div>', ll).group(1)
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-15].decode('latin-1')
        fecha = re.search('<div class="date">(.*) - <span>', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d.%m.%y')
    elif t == 'correo':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-11]
        fecha = re.search('<div class="date">(.*) - <span>', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d.%m.%y')
    elif t == 'lv':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-10].decode('latin-1')
        fecha = re.search('<div class="date">(.*) - <span>', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d.%m.%y')
    elif t == '20m':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-15].decode('latin-1')
        try:
            fecha = re.search('<li class="author">.* (.*) - .*', ll).group(1)
        except:
            fecha = re.search('<li class="author">.* (.*)</li>', ll).group(1)
        fecha = datetime.datetime.strptime(fecha, '%d.%m.%Y')
    elif t == 'ec':
        titulo = re.search('<title>(.*)</title>', ll).group(1)[:-21].decode('latin-1')
        fecha = ''.join(url.split('/')[4:7])
        fecha = datetime.datetime.strptime(fecha, '%Y%m%d')
        # TODO:
        """
        <a href="/espana/2013/02/13">13/02/2013</a>
                                    &nbsp;
            <span class="hora-publi">(06:00)</span>
        """
    elif t == 'eldiario':
        titulo = re.search('<title>(.*)</title>', ll).group(1).decode('utf-8')
        fecha = re.search('<span class="date">(.*)</span>', ll).group(1)[:-3]
        hora = re.search('<span class="time">(.*)</span>', ll).group(1)[:-1]
        fechahora = '%s %s' % (fecha, hora)
        fecha = datetime.datetime.strptime(fechahora, '%d/%m/%Y %H:%M')
    elif t == 'pais':
        titulo = re.search('<title>(.*)</title>', ll).group(1).split(' |')[0].decode('utf-8')
        try:
            fecha = re.search('</strong>, (.*)</div>', ll).group(1).strip()
            fecha = datetime.datetime.strptime(fecha, '%d de %B de %Y')
        except:
            fecha = re.search('class="actualizado".*>(.*) <abbr', ll).group(1)
            fecha = datetime.datetime.strptime(fecha, '%d %b %Y - %H:%M')
    elif t == 'mundo':
        titulo = re.search('<title>(.*)</title>', ll).group(1).split(' |')[0].decode('latin-1')
        fechahora = re.search('<p class="update">(.*)<strong>(.*)<abbr', ll).group(1).split(' ')[1][:-1]
        fechahora += ' ' + re.search('<p class="update">(.*)<strong>(.*)<abbr', ll).group(2)
        fecha = datetime.datetime.strptime(fechahora, '%d/%m/%Y %H:%M')

    result = formatResult(url, titulo, SUPPORTED_SITES[t], fecha)
    return result


if __name__ == "__main__":

    print "Wikiquoter v%s - Extrae citas directas para es.wikiquote.org" % __version__
    print "Copyright (C) 2011-2013 Pablo Castellano"
    print "This program comes with ABSOLUTELY NO WARRANTY."
    print "This is free software, and you are welcome to redistribute it under certain conditions."
    print

    # type = abc, publico
    if len(sys.argv) not in (2, 3):
        print "Usage: %s <URL> [type]" % sys.argv[0]
        sys.exit(0)

    result = getCite(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print result
