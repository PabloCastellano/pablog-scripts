#!/usr/bin/env python3
# search_libreborme.py - Buscar usando la API de Libreborme.net
# Más información en https://libreborme.readthedocs.org/es/latest/api/
#
# Copyright (C) 2015 Pablo Castellano <pablo@anche.no>
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

import urllib.request
import json
import sys

USER_AGENT = ''  # Can be blank
HOST = 'https://libreborme.net'

####################
SEARCH_PERSON_ENDPOINT = '{host}/borme/api/v1/persona/search/?q={query}&page={page}'
SEARCH_COMPANY_ENDPOINT = '{host}/borme/api/v1/empresa/search/?q={query}&page={page}'


def search_libreborme(query, type, page=1):
    if type == 'person':
        url = SEARCH_PERSON_ENDPOINT.format(host=HOST, query=query, page=page)
    elif type == 'company':
        url = SEARCH_COMPANY_ENDPOINT.format(host=HOST, query=query, page=page)
    else:
        raise ValueError('Invalid type: {0}'.format(type))

    if USER_AGENT:
        req = urllib.request.Request(url, data=None, headers={'User-Agent': USER_AGENT})
    else:
        req = urllib.request.Request(url, data=None)

    f = urllib.request.urlopen(req)
    data = f.read().decode('utf-8')
    return json.loads(data)


def print_results(data):
    objects = data['objects']
    for o in objects:
        print('{name} ({host}{url})'.format(name=o['name'], host=HOST, url=o['resource_uri']))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} "query" <person|company|all>'.format(sys.argv[0]))
        sys.exit(-1)

    if sys.argv[2] == 'all':
        data = search_libreborme(sys.argv[1], 'person')
        print_results(data)
        data = search_libreborme(sys.argv[1], 'company')
        print_results(data)
    else:
        data = search_libreborme(sys.argv[1], sys.argv[2])
        print_results(data)
