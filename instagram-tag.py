# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 21:52:37 2014

@author: dajun.tian
"""

"""
client_id <- ""
client_secret <- ""
https://api.instagram.com/v1/media/popular?client_id=CLIENT-ID
"""

import urllib2
import json
import time
import sys

outfilename = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime()) + "tag-instagram-json.txt"

def tag_array():
    #produce the list of tags to search
    #modidify contents between """ and """
    #keep the tags aligned(indented)
    tag_candidate_str = """
		tag
        """
    return tag_candidate_str.split()

def craw_tag(tag, outfilename, totalRequest = 100):
    #search the tag and store the results to outfilename
    next_url = "https://api.instagram.com/v1/tags/%s/media/recent?client_id=58372fa3afca4abdb00b286a68a04209" %tag    
    count = 0
    with open(outfilename, 'a') as outfile:
        try:
            while next_url:
                #print 'fetching URL:', next_url
                response = urllib2.urlopen(next_url)
                data = json.loads(response.read())
                time.sleep(0.72)
                for media in data['data']:
                    json.dump(media, outfile)
                    outfile.write('\n')
                    count += 1
                    #print count, totalRequest
                    if count >= totalRequest:
                        print "finishing fetching :", tag, "file stored at :", outfilename
                        print "total counts", count                        
                        return
                next_url = data['pagination']['next_url']
               
        except:
            print "error:", sys.exc_info()[0]
            print "probably reaches all the medias"            

def load_param(location):
    with open(location, "r") as infile:
        result = []
        for line in infile:
            tag_count = line.split()
            result.append([tag_count[0], int(tag_count[1])])
        return result
    
def loop_all_tag():
    #loop through all the tags in the tag_array()
    #return the filename
    param = load_param('tag_count.txt')

    for p in param:
        craw_tag(p[0], outfilename, totalRequest = p[1])
        
loop_all_tag()
