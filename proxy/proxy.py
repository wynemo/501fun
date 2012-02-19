#!/usr/bin/env python
# coding: utf-8

import web
from util import picType
from tco import handle_damn_tco
import img
from convert_link import convert_link
from config import settings
import urllib2
import css

render = settings.render
std_headers = settings.std_headers

class proxy:
    def GET(self,para):
        import re
        import base64
        import urllib
        i = web.input()
        b64 = None
        url = None
        try:
            url = i.url
            b64 = i.b64
        except:
            pass
        
        if url == None:
            return render.proxy()
            pass

        if b64 == '1':
            pass
            url = urllib.unquote_plus(base64.b64decode(url))
        url = re.sub(r'#\w*','',url)
        request = urllib2.Request(url.encode('utf-8'), None, std_headers)
        i1 = urllib2.urlopen(request)
        s2 = i1.read()

        try:
            web.header('Content-Length',i1.headers['Content-Length'],unique=True)
        except Exception,e:
            pass

        #get content type
        content_type = None
        try:
            content_type = i1.headers.getheader('Content-Type')
        except:
            pass
        if content_type and len(content_type):
            web.header('Content-Type',content_type, unique=True)

        pt1 = picType(i1.headers.type)
        if pt1:
            return s2

        s2 = img.get_img_parts(s2)    
        head_obj = re.search(r'<head.*</head>',s2,re.S|re.I|re.X)
        if head_obj:
            css_urls = css.handle_css(head_obj.group(),i1.url)
            char_obj = re.search(r'<meta[^<]*?charset=.*?/>',head_obj.group(),re.S|re.X|re.I)
            char_type = ''
            if char_obj:
                char_type = char_obj.group()

            title_obj = re.search(r'<title.*</title>',head_obj.group(),re.S|re.I|re.X)
            title_type = ''
            if title_obj:
                title_type = title_obj.group()

            s2 = s2.replace(head_obj.group(),
            '<head>' + char_type + title_type + css_urls + '</head>',
            1)
            return convert_link(s2)#link proxy
        else:
            if url.startswith('http://t.co') or url.startswith('https://t.co'):#god damned t.co
                new_url = handle_damn_tco(s2)
                if(new_url and len(new_url)):
                    raise web.seeother('/proxy?url=' + urllib.quote_plus(new_url))#iter
            return convert_link(s2)

