#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wq_ajax_server.py - Interfaz AJAX para wikiquoter.py
# Copyright (C) 2013 Pablo Castellano <pablo@anche.no>
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

# http://stackoverflow.com/questions/336866/how-to-implement-a-minimal-server-for-ajax-in-python

from wsgiref.simple_server import make_server

import wikiquoter

FILE = 'index.html'
PORT = 8080
WIKIQUOTER_PATH = './wikiquoter.py'


def getCite(url):
    print 'getcite:', url
    return wikiquoter.getCite(url)


def wikiquoter_app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
            print 'Request(s):\n', request_body
        except (TypeError, ValueError):
            request_body = ""

        response_body = ''
        for url in request_body.splitlines():
            try:
                response_body += getCite(url).encode('utf-8')
            except Exception, e:
                print e
                response_body += "!!ERROR!!: " + url
            response_body += '\n'

        print 'debug:'
        print response_body
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [response_body]
    else:
        response_body = open(FILE).read()
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]


def open_browser():
    """Start a browser after waiting for half a second."""
    import threading
    import webbrowser
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()


def start_server():
    """Start the server."""
    httpd = make_server("", PORT, wikiquoter_app)
    httpd.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()
