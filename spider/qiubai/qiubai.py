# coding=utf-8
import urllib2
import re
import chardet
import sys
import zlib

PAGE = 1
URL_24H = 'http://www.qiushibaike.com/hot/page/'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
headers = {'User-Agent': USER_AGENT}

url = URL_24H + str(PAGE)
sys_code = sys.getdefaultencoding()
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)

except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    elif hasattr(e, 'reason'):
        print e.reason

content = response.read()
gzipped = response.headers.get('Content-Encoding')
if gzipped:
    print "gzipped"
    content = zlib.decompress(content, 16+zlib.MAX_WBITS)

filename = 'qiubai.html'
fileobj = open(filename, 'w')
fileobj.write(content)

infoencode = chardet.detect(content).get('encoding', 'utf-8')
html = content.decode(infoencode, 'ignore').encode('gbk')

joke_pattern = "<div class=\"content\">\s(.+?)</div>\s+(<div class=\"thumb\">)?"
pattern_comp = re.compile(joke_pattern, re.DOTALL)
jokes = re.findall(pattern_comp, content)
for items in jokes:
    if items[1] != "<div class=\"thumb\">":
        html = items[0].decode(infoencode, 'ignore').encode('gbk')
        print html


