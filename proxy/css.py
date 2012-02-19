import re
import urllib

re_cos = re.S|re.I|re.X 

def handle_css(html_str,url):
    rv = ''
    try:
        rule1 = r'<\s*link[^>]+?type\s*=\s*"\s*text/css[^>]+?/>'
        rule2 = r'href\s*=\s*"'
        rule3 = r'https?\S+?\s*(?=")'
        rule4 = r'/\S+?\s*(?=")'
        css_cos1 = '<link href="'
        css_cos2 = '" type="text/css" rel="stylesheet" />'
        o1 = re.finditer(rule1,html_str,re_cos)
        for each in o1:
            #print 'each is ',each.group()
            o2 = re.search(rule2,each.group(),re_cos)
            if o2:
                #print 'o2 is ',o2.group()
                o3 = re.search(rule3,each.group()[o2.end():],re_cos)
                css_url = ''
                if o3:
                    css_url = o3.group()
                else:
                    o4 = re.search(rule4,each.group()[o2.end():],re_cos)
                    if o4:
                        #print o4.group()
                        css_url = get_base_url(url) + o4.group()
                if len(css_url):
                    css_url = '/proxy?url=' + urllib.quote(css_url)
                    rv += css_cos1 + css_url + css_cos2
    except Exception,e:
        print 'e is ',str(e)
    return rv

def get_base_url(url):
    rule5 = r'\w+://([\w-]+\.)+[\w-]+'
    o5 = re.search(rule5,url,re_cos)
    if o5:
        return o5.group()
    return None
    


        
