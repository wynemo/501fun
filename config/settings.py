#!/usr/bin/env python
# coding: utf-8
import web
import os

def get_home_dir():
    try:
        dir1 = os.environ['OPENSHIFT_REPO_DIR']
        if not dir1.endswith('/'):
            dir1 += '/'
        dir1 += 'wsgi/'
        return dir1
    except:
        return './'

render = web.template.render(get_home_dir() + 'templates/', cache=False)

web.config.debug = False

consumer_key = ""
consumer_secret = ""

#for j.mp link
no_jmp = True
bitly_name = ''
bitly_key = ''

std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
    #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-us,en;q=0.5'
                }
                

