#!/usr/bin/env python
import os
import socket
import sys
import re

# Disable output buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# TODO: Use threads
# TODO: port not default

config = '/etc/munin/munin.conf'
hosts = []


def readconfig(filename):
    global hosts
    with open(filename) as fp:
        for line in fp.readlines():
            match = re.match('^\s+address\s+(.*)\s*$', line)
            if match:
                hosts.append(match.group(1))


def checkhost(host, port=4949):
    s = socket.socket()
    res = 'FAILED'
    try:
        s.connect((host, port))
        buf = s.recv(100)
        if 'munin' in buf:
            res = 'OK'
        else:
            res = 'UNKNOWN'
    except:
        pass

    return res


if __name__ == '__main__':
    readconfig(config)
    for host in hosts:
        print "Checking host %s...\t" % host,
        res = checkhost(host)
        print res
