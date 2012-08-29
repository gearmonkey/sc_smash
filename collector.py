#!/usr/bin/env python
# encoding: utf-8
"""
collector.py

grabs all the downloadable soundcloud tracks from a users incoming (that are downloadable), then mashes them together

Created by Benjamin Fields on 2012-08-24.
Copyright (c) 2012 . All rights reserved.
"""

import sys
import getopt
import soundcloud
import config
import requests


help_message = '''
runs as $python collector sc_username output.mp3
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    verbose = False
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
        if len(args) != 2:
            raise Usage(help_message)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    sc_client = soundcloud.Client(
        client_id=config.SC_CLIENT_ID,
        client_secret=config.SC_CLIENT_SECRET,
        username='bfields',
        password="""V_7PHuh39oQe6@e'lpL\-!UH'"""
    )
    
    print 'Hi', sc_client.get('/me').username,
    print 'fetching your downloadable incoming tracks...'
    
    tracks = []
    for item in sc_client.get('e1/me/stream').collection:
        if not item['type'] == 'track':
            #for now just skip non-tracks
            continue
        print 'trying to download',item['track'][u'title'], 'by', item['track'][u'user'][u'username']
        track = sc_client.get(item['track'][u'stream_url'].split('.com')[-1])
        try:
            with open('cache/'+item['track'][u'permalink_url'].split('/')[-1]+'.mp3', 'wb') as wh:
                wh.write(track.raw_data)
        except Exception, err:
            print 'failed, because:', err
            continue
        tracks.append(track)
    print 'fetched', len(tracks), 'tracks'
            
        
    
if __name__ == "__main__":
    sys.exit(main())
