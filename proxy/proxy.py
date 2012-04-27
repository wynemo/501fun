#!/usr/bin/env python
# coding: utf-8

import web
from config import settings
import convert_link
import deny
import util
from tco import handle_damn_tco
import urllib2

render = settings.render
std_headers = settings.std_headers

class proxy:
    def GET(self,para):
        import re
        import base64
        import urllib
        from StringIO import StringIO
        import gzip
        import zlib

        def my_direct(url):
            #print 'host is ',web.ctx.host
            if web.ctx.host == "501fun.dabin.info": 
                raise web.seeother("https://" + web.ctx.host + url)
            else:
                raise web.seeother(url) 

        def set_len_header(len1 = None):
            if i1.headers.has_key('Content-Length'):
                if len1:
                    web.header('Content-Length',len1,unique=True)
                else:
                    web.header('Content-Length',i1.headers['Content-Length'],unique=True)
                    
        def is_html(type1):
            if type1 and len(type1):
                return -1 != type1.lower().find('text/html')
            return False
            
        def redirect_tco(url):
            if url.lower().startswith('http://t.co') or\
                url.lower().startswith('https://t.co'):#god damned t.co
                new_url = handle_damn_tco(s2)
                if(new_url and len(new_url)):
                    url1 = '/proxy?url=' + util.my_quote_plus(new_url) +\
                        '&nojs=1'
                    set_len_header()
                    my_direct(url1)#303

        i = web.input()
        b64 = None
        nojs = None
        url = None
        rf = None

        try:url = i.url
        except:pass

        if not url:
            return render.proxy()

        try:nojs = i.nojs
        except:pass

        try:b64 = i.b64
        except:pass

        try:rf = i.rf
        except:pass

        if b64 == '1':
            url = urllib.unquote_plus(base64.b64decode(url))
        url = re.sub(r'#.*','',url)
        
        header1 = std_headers.copy()
        header1['User-Agent'] = web.ctx.env.get('HTTP_USER_AGENT', header1['User-Agent'])
        #if web.ctx.env.has_key('HTTP_ACCEPT'):
        #    print web.ctx.env['HTTP_ACCEPT']
        request = urllib2.Request(url.encode('utf-8'), None, header1)
        if rf:
            request.add_header('Referer',rf)
        try:
            i1 = urllib2.urlopen(request,timeout = 3)
        except Exception,e:
            return str(e)
                
        s2 = i1.read()
        if i1.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(s2)
            f = gzip.GzipFile(fileobj=buf)
            s2 = f.read()
        elif i1.info().get('Content-Encoding') == 'deflate':
            try:
                s2 = zlib.decompress(s2)
            except:
                s2 = zlib.decompressobj(-zlib.MAX_WBITS).decompress(s2)
        #get content type
        content_type = None
        if i1.headers.has_key('Content-Type'):
            content_type = i1.headers['Content-Type']
            #content_type = i1.headers.getheader('Content-Type')
            if content_type and len(content_type):
                #print 'content_type is ',content_type
                web.header('Content-Type',content_type, unique=True)
        #else:
        #    print 'no content type'
        #    pass
               
        #image     
        type1 = i1.headers.type
        pt1 = util.picType(type1)
        if pt1:
            set_len_header()
            return s2
        
        #css
        if type1.lower().endswith('css'):
            #s2 = convert_link.conver_url_in_css(s2)
            s2 = convert_link.convert_html_tag_url(s2,i1.url)
            set_len_header(str(len(s2)))
            return s2

        
        #twitter t.co
        redirect_tco(url)   
            
        if is_html(content_type) or\
            re.search(r'<\s*html',s2,re.S|re.I):#should be html
            #convert
            s2 = convert_link.convert_html_tag_url(s2,i1.url)#conver href,src in tag
            #deny
            s2 = deny.replace_all_plus(s2)
            
            set_len_header(str(len(s2)))
            return s2
        else:
            #other type
            set_len_header()
            return s2

