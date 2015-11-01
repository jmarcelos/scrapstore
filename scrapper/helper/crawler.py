# coding=utf-8
from lxml import html as lhtml
import urllib2
from xml.dom import minidom
import pycurl
import StringIO
import logging
import json

class Crawler(object):

    USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    _opener = urllib2.build_opener()
    _opener.addheaders = [USER_AGENT]
    _curl = pycurl.Curl()

    def crawl(self, url):
        if not url:
            raise ValueError('Null is not allowed')
        file = self._opener.open(url)
        file_content = file.read()
        file.close()
        return file_content

    def crawl_HTML(self, url):
        doc = lhtml.fromstring(self.crawl(url))
        return doc

    def crawl_json(self, url):
        data = json.loads(self.crawl(url))
        return data

    def crawl_HTML_with_headers(self, url):
        if not url:
            raise ValueError('Null is not allowed')

        body = StringIO.StringIO()
        headers = StringIO.StringIO()

        self.__curl.setopt( pycurl.URL, str(url) )
        self.__curl.setopt( pycurl.WRITEFUNCTION, body.write )
        self.__curl.setopt( pycurl.HEADERFUNCTION, headers.write )

        try:
            self.__curl.perform()
            content = body.getvalue()
            headers = headers.getvalue()

            body.close()

            return content,headers
        except Exception, msg:
            logging.error("Nao foi possivel buscar [%s] - [%s]" % (url, msg))
            return

    def crawl_XML(self, url):
        xmldoc = minidom.parseString(self.crawl(url))
        return xmldoc

    def get_HTML_info(self, document, rules=None):
        if not document:
            raise ValueError('Document could not be null')

        return document.xpath(rules)

    def get_XML_info(self, document):
        if not document:
            raise ValueError('Document could not be null')
        return document.getElementsByTagName('loc')

    def get_parsed_content(self, doc):
        return []

    def get_pagination_rule(self, page_number):
        return ""
