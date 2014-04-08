#!/usr/bin/env python
# -*- coding: utf-8 -*-
# browsers_check_extension_keys.py - Check extensions signatures
# Copyright (C) 2014 Pablo Castellano <pablo@anche.no>
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

__author__ = "Pablo Castellano <pablo@anche.no>"
__version__ = 0.1
__license__ = "GNU GPLv3+"
__date__ = "2014-04-08"

import os

FFX_PATH = os.path.expanduser('~/.mozilla/firefox')
CHROMIUM_PATH = os.path.expanduser('~/.config/chromium/Default/Extensions')
CHROME_PATH = os.path.expanduser('~/.config/google-chrome/Default/Extensions')
VERBOSE = False

KEYS = {
    'https-everywhere': 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6MR8W/galdxnpGqBsYbqOzQb2eyW15YFjDDEMI0ZOzt8f504obNs920lDnpPD2/KqgsfjOgw2K7xWDJIj/18xUvWPk3LDkrnokNiRkA3KOx3W6fHycKL+zID7zy+xZYBuh2fLyQtWV1VGQ45iNRp9+Zo7rH86cdfgkdnWTlNSHyTLW9NbXvyv/E12bppPcEvgCTAQXgnDVJ0/sqmeiijn9tTFh03aM+R2V/21h8aTraAS24qiPCz6gkmYGC8yr6mglcnNoYbsLNYZ69zF1XHcXPduCPdPdfLlzVlKK1/U7hkA28eG3BIAMh6uJYBRJTpiGgaGdPd7YekUB8S6cy+CQIDAQAB'
}


FFX_EXT_PATHS = {
    'https-everywhere': 'https-everywhere@eff.org'
}

CHROMIUM_EXT_PATHS = {
    'https-everywhere': 'gcbommkclmclpchllfjekcdonpmejbdp'
}

TOTAL_OKS = 0
TOTAL_FAILS = 0


def check_firefox():
    global TOTAL_OKS, TOTAL_FAILS

    print 'Checking firefox...'
    if not os.path.isdir(FFX_PATH):
        print 'Installation not found'
        return

    for key in KEYS:
        (_, profiles, _) = os.walk(FFX_PATH).next()
        profiles.remove('Crash Reports')
        for profile in profiles:
            full_path = os.path.join(FFX_PATH, profile, 'extensions', FFX_EXT_PATHS[key])
            if not os.path.isdir(full_path):
                if VERBOSE:
                    print 'Extension not found in profile:', profile
                continue
            if VERBOSE:
                print full_path
            key_file = os.path.join(full_path, 'install.rdf')
            with open(key_file) as fp:
                content = fp.read()
                begin = content.find('<em:updateKey>') + 14
                end = content.find('</em:updateKey>', begin)
                signature = content[begin:end]
                if signature == KEYS[key]:
                    print 'OK\t', key, profile
                    TOTAL_OKS += 1
                else:
                    print 'FAIL\t', key, profile
                    TOTAL_FAILS += 1
    print


def check_chromium():
    global TOTAL_OKS, TOTAL_FAILS

    print 'Checking chromium...'
    if not os.path.isdir(CHROMIUM_PATH):
        print 'Installation not found'
        return

    for key in KEYS:
        extension_path = os.path.join(CHROMIUM_PATH, CHROMIUM_EXT_PATHS[key])
        if not os.path.isdir(extension_path):
            print 'Extension not found'
            continue
        full_path = os.path.join(extension_path, os.listdir(extension_path)[0])
        if VERBOSE:
            print full_path
        key_file = os.path.join(full_path, 'manifest.json')
        with open(key_file) as fp:
            content = fp.read()
            begin = content.find('"key": "') + 8
            end = content.find('",', begin)
            signature = content[begin:end]
            if signature == KEYS[key]:
                print 'OK\t', key
                TOTAL_OKS += 1
            else:
                print 'FAIL\t', key
                TOTAL_FAILS += 1
    print


def check_chrome():
    global TOTAL_OKS, TOTAL_FAILS

    print 'Checking chrome...'
    if not os.path.isdir(CHROME_PATH):
        print 'Installation not found'
        return

    for key in KEYS:
        extension_path = os.path.join(CHROME_PATH, CHROMIUM_EXT_PATHS[key])
        if not os.path.isdir(extension_path):
            print 'Extension not found'
            continue
        full_path = os.path.join(extension_path, os.listdir(extension_path)[0])
        if VERBOSE:
            print full_path
        key_file = os.path.join(full_path, 'manifest.json')
        with open(key_file) as fp:
            content = fp.read()
            begin = content.find('"key": "') + 8
            end = content.find('",', begin)
            signature = content[begin:end]
            if signature == KEYS[key]:
                print 'OK\t', key
                TOTAL_OKS += 1
            else:
                print 'FAIL\t', key
                TOTAL_FAILS += 1
    print


if __name__ == '__main__':
    check_firefox()
    check_chromium()
    check_chrome()

    print 'Results:'
    print '%d extensions of %d were OK' % (TOTAL_OKS, TOTAL_OKS + TOTAL_FAILS)
