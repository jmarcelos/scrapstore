from lxml import html as lhtml
import urllib2
from xml.dom import minidom

class Crawler:

    USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
    __opener = None

    def __init__(self):
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.USER_AGENT]

    def crawl(self, url):
        if not url:
            raise ValueError('Null is not allowed')
        file = self.__opener.open(url)
        file_content = file.read()
        file.close()
        return file_content

    def crawlHTML(self, url):
        doc = lhtml.fromstring(self.crawl(url))
        return doc


    def crawlXML(self, url):
        xmldoc = minidom.parseString(self.crawl(url))
        return xmldoc

    def getHTMLInfo(self, document, rules=None):
        if not document:
            raise ValueError('Document could not be null')
        #return document.xpath('//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')
        return document.xpath(rules)

    def getXMLInfo(self, document, rules=None):
        if not document:
            raise ValueError('Document could not be null')
        #return document.xpath('//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')
        return document.getElementsByTagName('loc')

    def getParsedContent(self, doc):
        return []

    def getPaginationRule(self, page_number):
        return ""
