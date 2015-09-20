from lxml import html as lhtml
import urllib2
from xml.dom import minidom

class Crawler(object):

    #USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')

    #def __init__(self):
        #self.__opener = urllib2.build_opener()
        #self.__opener.addheaders = [self.USER_AGENT]

    def crawl(self, url):
        USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        opener = urllib2.build_opener()
        opener.addheaders = [USER_AGENT]
        print url
        if not url:
            raise ValueError('Null is not allowed')
        file = opener.open(url)
        file_content = file.read()
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

    def encode__openner(__opener):
        return
