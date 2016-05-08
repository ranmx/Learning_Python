# -*- coding: utf-8 -*-
import urllib2
import re
import chardet
import sys
import zlib
import cookielib
import json
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.7,zh-CN;q=0.3",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0"
}


class LogIn(object):
    def __init__(self):
        self.url = "https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F&renew=1"


class GuidePage(object):
    def __init__(self):
        self.URL_NEW = 'http://sh.fang.lianjia.com/list/pg'
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        self.headers = HEADERS
        self.url_list = list()
        self.href_pattern = re.compile('/detail/')
        self.text_pattern = re.compile('.+')
        self.url_pattern = re.compile('(/detail/\w+)')

    def _get_page_url(self):
        for i in range(1, 65):
            yield self.URL_NEW + str(i)

    def _get_response(self, url):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            elif hasattr(e, 'reason'):
                print e.reason

    def _get_html(self, response):
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)
        return html

    def _get_url(self, html):
        url_list = []
        html_soup = BeautifulSoup(html, "lxml")
        tag_list = html_soup.find_all('a', href=self.href_pattern, text=self.text_pattern)
        for tag in tag_list:
            url = re.search(self.url_pattern, str(tag))
            url_list.append(url.group())
        return url_list

    def get_url(self):
        for page in self._get_page_url():
            response = self._get_response(page)
            html = self._get_html(response)
            self.url_list += self._get_url(html)
            return self.url_list


class CourtPage(object):
    def __init__(self):
        self.URL_PAGE = 'http://sh.fang.lianjia.com/'
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        self.headers = HEADERS
        self.url_list = list()
        self.con_pat = re.compile('(\S+)')
        pathes = GuidePage().get_url()
        for path in pathes:
            self.url_list.append(self.URL_PAGE + path)

    def _get_page_url(self, path):
        return self.url_list.pop()

    def _get_response(self, url):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            elif hasattr(e, 'reason'):
                print e.reason

    def _get_html(self, response):
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)
        return html

    def _get_feature_dict(self, html):
        info_dict = {}
        html_soup = BeautifulSoup(html, "lxml")
        box = html_soup.find('div', class_="box-left")
        # --------------------------------------------
        name = box.find('h1').text
        price_box = box.find('p', class_="jiage").find_all('span')
        try:
            unit = price_box[2].text
            price = price_box[1].text + unit
        except IndexError:
            price = 'TBD'

        tag_list = box.find('p', class_="small-tags").text.replace('\n', ' ').strip()
        location = box.find('p', class_="where").text.strip()
        [distinct, address] = location.split('-')
        when_block = box.find('p', class_="when").text
        when = re.findall(self.con_pat, when_block)[1]
        type_block = box.find('p', class_="wu-type").text
        type_list = re.findall(self.con_pat, type_block)
        type_con = str()
        for i in range(1, len(type_list)):
            type_con += type_list[i]
        # --------------------------------------------
        info_dict.update({'name': name})
        info_dict.update({'price': price})
        info_dict.update({'tags': tag_list})
        info_dict.update({'distinct': distinct})
        info_dict.update({'address': address})
        info_dict.update({'type': type_con})
        info_dict.update({'time': when})
        return info_dict

    def test(self):
        for url in self.url_list:
            print url
            response = self._get_response(url)
            if response:
                html = self._get_html(response)
                dict = self._get_feature_dict(html)
                for key in dict.keys():
                    print key, ' = ', dict[key]
                print '-' * 30



def test():
#    guide_page = GuidePage()
#    url_list = guide_page.get_url()
#    file = open('urls.txt', 'w')
#    for item in url_list:
#        file.write(item)
#        print item
#    file.close()
    CourtPage().test()



test()
