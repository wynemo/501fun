#!/usr/bin/env python
#coding:utf-8

import web
from config import settings

render = settings.render

def my_notfound():
    """Returns a `404 Not Found` error."""
    return web.notfound(render.custom404())

urls = ('/','501fun_t_api.twitterapi.ttcbk.index',
    '/auth','501fun_t_api.twitterapi.ttauth.auth',
    '/api/(.*)','501fun_t_api.twitterapi.ttapi.api',
    '/dropbox(.*)','dropboxpublic.dppub.Dropbox0',
    '/dp(.*)','dropboxpublic.dppub.Dropbox',
    '/proxy($|/.*)','proxy.proxy.proxy', 
    '/april1/?','april1.badperson.fool',
    r'/todo','todo.todo.todo',
    r'/todo/add','todo.todo.add',
    r'/todo/delete','todo.todo.delete1',
    '/autopac','pac.autopac.autopac',
    '/dict($|/.*)','dictmd.dictmd.dictmd', 
    '(.*)','proxy.proxy.proxy'
    #'/t2p','t2p',
    #'/test','testdisqus'
)

app = web.application(urls, globals())
app.notfound = my_notfound
application = app.wsgifunc()
if __name__=="__main__":
#    app.run()
    pass


#class t2p:
#    def GET(self):
#        return render.t2p()
#    def POST(self):
#        i = web.input()
#        web.header('Content-Type', 'text/html')
#        status,message = util.send_text_to_imgur(i.myarea)
#        return  '<div>' + status + ' ' + message + '</div>'

#class testdisqus():
#    def GET(self):
#        return render.testdisqus()
