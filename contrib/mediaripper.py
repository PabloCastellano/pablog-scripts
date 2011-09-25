#!/usr/bin/env python
"""
	This script pulls 'audio/mpeg' and 'video/x-flv' data out of TCP streams.
	MP3 files will be automatically re-named based on the info in the ID3 tag.
	
	This can be used to save audio and video files from sites like Grooveshark, Youtube, and others.

	Run the script, then open your browser and play the music or video you'd like to save.

	Some of this is based off of pieces of code I managed to find on google. Then I modified it for my needs.

	The most current version can be found at: http://roycormier.net/download/mediaripper.py
"""

# apt-get install python-dpkt python-pypcap python-eyed3
from __future__ import division
import dpkt, pcap
import re
import eyeD3
import hashlib
import os
import sys

file_counter = 0
conn = dict()
#You may need to set this to something such as wlan0 if using WiFi
interface='wlan1'

def rename_id3(filename):

    if os.path.isfile(filename)==False:
        print "File not found: "+filename
        return

    print "Processing: "+filename
    tag = eyeD3.Tag()
    tag.link(filename)

    artist = tag.getArtist()
    if len(artist)==0:
        artist = "unknown"

    title = tag.getTitle()
    if len(title)==0:
        with open(filename) as inFile:
	    d = hashlib.sha1()
	    d.update(inFile.read())
	    digest = d.hexdigest()
	    title = digest
    new_filename = artist+' - '+title+'.mp3'
    print "Renaming "+filename+" to "+new_filename
    os.rename(filename,new_filename)
    return

def getContent(pkt):
    global file_counter, conn
    eth = dpkt.ethernet.Ethernet(pkt)
    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
        return
    ip = eth.data
    if ip.p != dpkt.ip.IP_PROTO_TCP:
        return
    tcp = ip.data
    data = tcp.data

    if len(data) < 4:
        return

    # tupl uniquely identifies a TCP connection
    tupl = (ip.src, ip.dst, tcp.sport, tcp.dport)

    if tupl not in conn and tcp.data[:4] != 'HTTP':
        return

    #Flash Video file
    if tcp.data[:4] == 'HTTP' and 'video/x-flv' in data:
        content_length = None
        if 'Content-Length' in data:
            m = re.search('Content-Length: (\d+)', data, re.I)
            if m:
                content_length = int(m.group(1))
            else:
                print 'failed match'
        if content_length:
            header_end = data.find('\r\n\r\n')
            received = len(data) - header_end - 4
            if received < content_length:
                print 'FLV Size:',content_length
                filename = 'video_{0}.flv'.format(file_counter)
                print 'Temporarily saving as', filename
                file_counter += 1
                f = open(filename, 'wb')
                header_end
                f.write(data[header_end+4:])
                conn[tupl] = [content_length, f, 'video/x-flv']
                return
            # These should not be called, unless the audio is very short
            print 'Done receiving packet!'
            print('Clen:',content_length,'Recv:',received)
        else:
            print 'no content length!!!'

    if tcp.data[:4] == 'HTTP' and 'audio/mpeg' in data:
        content_length = None
        if 'Content-Length' in data:
            m = re.search('Content-Length: (\d+)', data, re.I)
            if m:
                content_length = int(m.group(1))
            else:
                print 'failed match'
        if content_length:
            header_end = data.find('\r\n\r\n')
            received = len(data) - header_end - 4
            if received < content_length:
                print 'MP3 Size:',content_length
                filename = 'Track_{0}.mp3'.format(file_counter)
                print 'Temporarily saving as', filename
                file_counter += 1
                f = open(filename, 'wb')
                header_end
                f.write(data[header_end+4:])
                conn[tupl] = [content_length, f, 'audio/mpeg']
                return
            # These should not be called, unless the audio is very short
            print 'Done receiving packet!'
            print('Clen:',content_length,'Recv:',received)
        else:
            print 'no content length!!!'
    if tupl in conn:
        content_length, f, content_type = conn[tupl]
        percent = (f.tell()/content_length)*100
	sys.stdout.write("\rDownloading %s %s: %2d%% " % (content_type,f.name,percent))
	sys.stdout.flush()
        f.write(data)
        if f.tell() >= content_length:
            f.close()
            print 'Saved', content_length, 'bytes'
            del conn[tupl]

	    #Read the ID3 tag and Rename the file accordingly
	    if content_type=='audio/mpeg':
                rename_id3(f.name)

pc = pcap.pcap(interface)
print "Running.. Waiting for data..."
for ts, pkt in pc:
    getContent(pkt)
