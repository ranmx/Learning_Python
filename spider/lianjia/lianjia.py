# -*- coding: utf-8 -*-
import urllib2
import re
import chardet
import sys
import zlib
import cookielib
import json
from bs4 import BeautifulSoup
import threading
import MySQLdb

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
        threads = []
        lock = threading.Lock()
        for page in self._get_page_url():
            t = threading.Thread(target=self._run, args=(page, lock))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.url_list

    def _run(self, page, lock):
        response = self._get_response(page)
        html = self._get_html(response)
        lock.acquire()
        self.url_list += self._get_url(html)
        lock.release()


class CourtPage(object):
    def __init__(self, db):
        self.URL_PAGE = 'http://sh.fang.lianjia.com'
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        self.headers = HEADERS
        self.url_list = list()
        self.con_pat = re.compile('(\S+)')
        self.db = db
        paths = GuidePage().get_url()
        for path in paths:
            self.url_list.append(self.URL_PAGE + path)

    def _get_page_url(self):
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

    def _get_feature_dict(self, html, db):
        # info_dict = {}
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
        # info_dict.update({'name': name})
        # info_dict.update({'price': int(price)})
        # info_dict.update({'tags': tag_list})
        # info_dict.update({'distinct': distinct})
        # info_dict.update({'address': address})
        # info_dict.update({'type': type_con})
        # info_dict.update({'time': when})
        info_list = [name, price, tag_list, distinct, address, type_con, when]
        t = tuple(info_list)
        query = ("INSERT INTO lianjia "
                "(name, price, tag_list, region, address, type_con, open_time) "
                 "VALUES(%s,%s,%s,%s,%s,%s,%s)", t)
        db.exe(query)
        print name, "is done"

    def run(self):
        thread_pool = []
        for url in self.url_list:
            self._execute(url)
#            t = threading.Thread(target=self._execute, args=(url, 0))
# #           thread_pool.append(t)
#        for t in thread_pool:
#            t.start()
#        for t in thread_pool:
#            t.join()

    def _execute(self, url):
        response = self._get_response(url)
        if response:
            html = self._get_html(response)
            self._get_feature_dict(html, self.db)


class MysqlWrapper(object):
    def __init__(self, command=''):
        self.lock = threading.RLock()
        if command != '':
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            self._conn_close(conn)

    def _get_conn(self):
        cxn = MySQLdb.connect(user='ran', passwd='test1234', db='lianjia')
        return cxn

    def _conn_close(self, conn=None):
        if conn is not None:
            conn.close()

    def conn_trans(func):

        def connection(self, *args, **kwargs):
            self.lock.acquire()
            conn = self._get_conn()
            kwargs['conn'] = conn
            rs = self.exe(self, *args, **kwargs)
            self._conn_close(conn)
            return rs

        return connection

    @conn_trans
    def exe(self, command, conn=None):
        cur = conn.cursor()
        try:
            cur.execute(command)
            conn.commit()
        except Exception, e:
            print e
            return -2
        return 0


def main():
    # info_list = [name, int(price), tag_list, distinct, address, type_con, when]
    command = ("CREATE TABLE IF NOT EXISTS new_house"
               "(name TEXT, price TEXT, tag_list TEXT, region TEXT, "
               "address TEXT, type_con TEXT, open_time TEXT)")
    db = MysqlWrapper(command)
    cp = CourtPage(db)
    cp.run()


if __name__ == "__main__":
    main()
