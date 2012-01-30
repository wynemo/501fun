def get_url_part(str1):
    import re
    import urllib
    o1 = re.search(r'"\s*(http|https).*?"',str1,re.I|re.M|re.S)
    if o1:
        return o1.group().replace('"','')
    return None

def get_src_part(str1):
    import re
    o1 = re.search(r'src\s*=\s*"\s*(http|https).*?"',str1,re.I|re.M|re.S)
    if o1:
        return get_url_part(o1.group())
    return None

def get_img_parts(str1):
    _c_str = '/proxy?url='
    _para = 'b64=1'
    import re
    import urllib
    import base64
    o1 = re.finditer(r'<\s*img.*?>',str1,re.I|re.M|re.S)
    for _1 in o1:
        __1 = get_src_part(_1.group())
        if __1:
            pass
            _tmp = _1.group().replace(__1,
                _c_str + urllib.quote_plus(base64.b64encode(urllib.quote_plus(__1))) + '&' + _para,
                1)
            str1 = str1.replace(_1.group(),
            _tmp,
            1)
    return str1

