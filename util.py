xinwei_font_path = '../STZHONGS.TTF'
arial_font_path = '../lucon.ttf'


def picType(s1):
    s2 = s1.lower()
    if s2.endswith('jpg')\
        or s2.endswith('jpeg'):
        return 'jpeg'
    if s2.endswith('png'):
        return 'png'
    if s2.endswith('gif'):
        return 'gif'
    return None

def get_chs_lnk(str1,plus=1):
    import re,urllib
    u1 = str1.decode('utf-8')
    #o1 = re.search(ur'[\u4e00-\u9fff]+',u1)
    o1 = re.search(ur'[^\w\~\#\:\.\?\+\=\&\%\@\-\\\/]+',u1)
    if not o1:
        return str1
    while o1:
        if plus == 1:
            _1 = (urllib.quote_plus(o1.group().encode('utf-8'))).decode('utf-8')
        else:
            _1 = (urllib.quote(o1.group().encode('utf-8'))).decode('utf-8')
        u1 = u1.replace(o1.group(),_1)
        #o1 = re.search(ur'[\u4e00-\u9fff]+',u1)
        o1 = re.search(ur'[^\w\~\#\:\.\?\+\=\&\%\@\-\\\/]+',u1)

    return u1.encode('utf-8')


def stealStuff(str1,name):
    import minus
    import imghdr
    try:
        if(str1):
            type1 =imghdr.what('memory',str1)
            str2 = name + '.' + type1
            gallery1 = minus.CreateGallery()
            value_editor_id = gallery1.editor_id#unicode
            value_reader_id = gallery1.reader_id#unicode
            if(len(value_editor_id)):
                item1 = minus.UploadItem(str2,gallery1,itemData=str1)
                return 'success',r'http://min.us/l' + item1.id
            else: return 'error','minus gallery error'
        return 'error','link no data'
    except Exception, e:
        return 'error',str(e)    
    
def send_text_to_imgur(u_text):
    import imgur,urllib,urllib2
    try:
        u_text = u_text.replace(u'|',u'')
        u_text = u_text.replace(u'\r',u'').replace(u'\n',u'|')
        a_text = urllib.quote(u_text.encode('utf-8'))
        print 'http://chart.apis.google.com/chart?chst=d_text_outline&chld=000000|14|l|FFFFFF|_|' + a_text
        a_text = urllib2.urlopen('http://chart.apis.google.com/chart?chst=d_text_outline&chld=000000|14|l|FFFFFF|_|' + a_text).read()
        return 'success',imgur.up_to_imgur(a_text)
        #return 'success',imgur.up_to_imgur(t2p1(u_text))
    except Exception, e:
        return 'error',str(e)
    
def send_text_to_minus(name,u_text):
    return stealStuff(t2p(u_text,xinwei_font_path),name)
    
def t2p(u_text,
    font_path,
    font_size = 16,
    line_height = 20,
    pic_width = 400):
    import PIL
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw 
    import cStringIO

    text_color = (0,0,0)#black
    bg_color = (255,255,255)#white

    font = ImageFont.truetype(font_path,font_size)

    y1 = 0
    x1 = 0
    list1 = []
    _line = u''

    for _1 in u_text: 
        _tmp = font.getsize(_1)[0]
        x1 += _tmp  
        if x1 > pic_width:      
            _t1 = y1, _line
            list1.append(_t1)
            y1 += line_height
            x1 = _tmp
            _line = ''
        _line += _1
        
    _t1 = y1,_line
    list1.append(_t1)    

    img = Image.new("RGBA", (pic_width,len(list1)*line_height),bg_color)
    draw = ImageDraw.Draw(img)

    for num,(a,b) in enumerate(list1):
        draw.text((0, a),b,text_color,font=font)

    del draw
    #img.save("a_test.png")
    
    #write to file object
    f = cStringIO.StringIO()
    img.save(f, "PNG")
    f.seek(0)
    str1 = f.read()
    f.close()
    return str1    
    
def t2p1(u_text):
    import PIL
    from PIL import ImageFont
    from PIL import Image
    from PIL import ImageDraw 
    import cStringIO
    
    text_color = (0,0,0)#black
    bg_color = (255,255,255)#white

    font_size = 16
    line_height = 20
    pic_width = 400
    
    xinwei_font = ImageFont.truetype(xinwei_font_path,font_size)
    arial_font = ImageFont.truetype(arial_font_path,font_size)

    y1 = 0
    x1 = 0
    list1 = []
    list2 = []

    c0orc1 = 0

    for _1 in u_text: 
        if _1 == u'\r':
            continue
        if _1 == u'\n':
            y1 += line_height
            x1 = 0
            continue
        if isnotc0orc1(_1):
            _tmp = xinwei_font.getsize(_1)[0]
            c0orc1 = 1
        else:
            _tmp = arial_font.getsize(_1)[0]
            c0orc1 = 0

        x1 += _tmp  

        if x1 > pic_width:      
            y1 += line_height
            x1 = _tmp
        if 1 == c0orc1:
            _t1 = x1 - _tmp,y1,_1
            list1.append(_t1)    
        else:
            _t2 = x1 - _tmp,y1,_1
            list2.append(_t2)    
  
    #print len(list1)
    img = Image.new("RGBA", (pic_width,y1+line_height+5),bg_color)
    draw = ImageDraw.Draw(img)

    for (a,b,c) in list2:
        draw.text((a, b+5),c,text_color,font=arial_font)
    for (a,b,c) in list1:
        draw.text((a, b),c,text_color,font=xinwei_font)
        #draw.text((a, b),c,text_color,font=xinwei_font)
        

    del draw
    
    #write to file object
    f = cStringIO.StringIO()
    img.save(f, "PNG")
    f.seek(0)
    str1 = f.read()
    f.close()
    return str1  

def isnotc0orc1(u_str):
    import re
    return re.search(ur'[^\u0000-\u009f]+',u_str)    
