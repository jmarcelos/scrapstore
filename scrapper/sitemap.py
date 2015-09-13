import urllib2
from xml.dom import minidom
from mongomodel import MongoCollection

class Sitemap(MongoCollection):

    url = None
    prioridade = 0
    data_scan = None
    site = None

    def __init__(self, url=None, site=None, prioridade=10, data_scan=None):
        self.url = url
        self.prioridade = prioridade
        self.data_scan = data_scan
        self.site = site


class SitemapReader:

    sitemap = []
    site = None
    USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')

    def __init__(self, sitemaps):
        print "iniciando a leitura"
        self.sitemaps = sitemaps

    def run(self):
        full_homepage_list = []
        for sitemap_key in self.sitemaps:
            url = self.sitemaps[sitemap_key]
            localizacoes = self.searchHomeProduct(url)
            homepage_list = self.readSitemap(localizacoes, sitemap_key)
            full_homepage_list.append(homepage_list)

        print len(full_homepage_list)
        return full_homepage_list

    def readSitemap(self, localizacoes, sitemap_key):
        homepage_list = []
        for local in localizacoes:
            url = local.firstChild.nodeValue
            if "xml" in url:
                homepage_list = self.readSitemap(self.searchHomeProduct(url), sitemap_key)
            else:
                conteudo = Sitemap(url=url, prioridade=10, site=sitemap_key)
                #print conteudo.to_dict()
                homepage_list.append(conteudo.to_dict())

        return homepage_list

    def searchHomeProduct(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [self.USER_AGENT]
        file = opener.open(url)
        file_content = file.read()
        file.close()
        xmldoc = minidom.parseString(file_content)

        localizacoes = xmldoc.getElementsByTagName('loc')

        return localizacoes

    def sameSitemapContent(self, content):

        return false

#x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml" })
x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml", "Extra":"http://buscando.extra.com.br/sitemap.xml" })
#x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml" })
print x.run()
