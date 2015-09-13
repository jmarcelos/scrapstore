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

    def __init__(self, sitemaps):
        print "iniciando a leitura"
        self.sitemaps = sitemaps

    def run(self):
        for sitemap_key in self.sitemaps:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]

            file = opener.open(self.sitemaps[sitemap_key])
            file_content = file.read()
            file.close()
            xmldoc = minidom.parseString(file_content)

            localizacoes = xmldoc.getElementsByTagName('loc')

            for local in localizacoes:
                conteudo = Sitemap(url=local.firstChild.nodeValue, prioridade=10, site=self.site)
                conteudo.save()

x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml"})
x.run()
