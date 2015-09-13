import urllib2
from xml.dom import minidom
from mongomodel import MongoCollection
from home import HomePageAmericanas, HomePage


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
            full_homepage_list = full_homepage_list + homepage_list

        return full_homepage_list

    def readSitemap(self, localizacoes, sitemap_key):
        homepage_list = []
        for local in localizacoes:
            url = local.firstChild.nodeValue
            if "xml" in url:
                homepage_list_aux = self.readSitemap(self.searchHomeProduct(url), sitemap_key)
                homepage_list = homepage_list + homepage_list_aux
            else:
                conteudo = HomePage(url=url, prioridade=10, site=sitemap_key)
                homepage_list.append(conteudo)

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

#x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml" })
#x = SitemapReader({"Netshoes": "http://www.netshoes.com.br/sitemap.xml"})
#x = SitemapReader({"Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml"})
#x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml" })

#ponto frio, walmart, amazon(http://www.amazon.com.br/sitemap-manual-index.xml) --> server error
x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml", "Extra":"http://buscando.extra.com.br/sitemap.xml", "Netshoes": "http://www.netshoes.com.br/sitemap.xml", "Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml" })

lista = x.run()
persiste = HomePage()
persiste.save_in_bulk(lista)
