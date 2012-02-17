def convert_link(s1):
    import re
    import urllib
    href_pattern = r'<\s*a.+?href\s*=\s*"https?://.*?"\s*>'
    link_pattern1 = r'href\s*=\s*"'
    link_pattern2 = r'.+?(?=")'
    flag1 = re.S|re.I|re.X
    iter1 = re.finditer(href_pattern,s1,flag1)
    new_str = ''
    pos = 0
    for each in iter1:
        url_obj1 = re.search(link_pattern1,each.group(),flag1)
        url_obj2 = re.search(link_pattern2,each.group()[url_obj1.end():],flag1)
        new_url = '/proxy?url=' + urllib.quote_plus(url_obj2.group())
        new_href = each.group()[:url_obj1.end()] + each.group()[url_obj1.end():].replace(url_obj2.group(),new_url,1)
        new_str += s1[pos:each.start()] + new_href
        pos = each.end()        
    new_str += s1[pos:]
    return new_str