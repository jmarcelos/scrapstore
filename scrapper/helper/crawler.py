from lxml import html as lhtml
import urllib2
from xml.dom import minidom
from mongoengine import *

class Crawler(object):

    USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    __opener = urllib2.build_opener()
    __opener.addheaders = [USER_AGENT]

    def crawl(self, url):
        if not url:
            raise ValueError('Null is not allowed')
        file = self.__opener.open(url)
        file_content = file.read().decode('utf-8')
        file.close()
        return file_content

    def crawl_HTML(self, url):
        doc = lhtml.fromstring(self.crawl(url))
        return doc


    def crawl_XML(self, url):
        xmldoc = minidom.parseString(self.crawl(url))
        return xmldoc

    def get_HTML_info(self, document, rules=None):
        if not len(document):
            raise ValueError('Document could not be null')

        return document.xpath(rules)

    def get_XML_info(self, document, rules=None):
        if not document:
            raise ValueError('Document could not be null')
        return document.getElementsByTagName('loc')

    def get_parsed_content(self, doc):
        return []

    def get_pagination_rule(self, page_number):
        return ""
