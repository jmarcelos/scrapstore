import urllib2
from xml.dom import minidom
from mongomodel import MongoCollection
from crawl import Crawler
from lxml import html as lhtml
from re import sub


class HomePage(MongoCollection):

    url = None
    prioridade = 0
    data_scan = None
    site = None

    def __init__(self, url=None, site=None, prioridade=10, data_scan=None):
        self.url = url
        self.prioridade = prioridade
        self.data_scan = data_scan
        self.site = site

    def parse(self):
        page_number = 1
        product_list = []
        while True:
            url = self.url + "?" + self.getPaginationRule(page_number)
            html,headers = Crawler().get(self.url)
            doc = lhtml.fromstring(html)
            product_list_aux = self.getProductList(doc)
            print url
            print len(product_list_aux)
            if not product_list_aux:
                break
            product_list = product_list + product_list_aux
            page_number += 1
            #break
        return product_list


    def getProductList(self, doc):
        return []

    def getPaginationRule(self, page_number):
        return ""

#from sitemap import HomePageAmericanas; acom = HomePageAmericanas(); acom.url = "http://www.americanas.com.br/linha/267868/informatica/notebook"; acom.parse()

class HomePageAmericanas(HomePage):

    pagination_parameters = "ofertas.limit=%s&ofertas.offset=%s"
    quantidade_por_pagina = 90

    def getProductList(self, doc):
        return  doc.xpath('//div[@class="paginado"]/section/article/div/form/@action')

    def getPaginationRule(self, page_number):
        return "ofertas.limit=%s&ofertas.offset=%s" % (self.quantidade_por_pagina, self.quantidade_por_pagina * page_number)

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

        #print "final"
        #print len(full_homepage_list)
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
                #print conteudo.to_dict()
                homepage_list.append(conteudo)

        #print "dentro do readSitemap"
        #print len(homepage_list)
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

    #perfomance rules!!!
    #def sameSitemapContent(self, content):
    #    return false

#x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml" })
#x = SitemapReader({"Netshoes": "http://www.netshoes.com.br/sitemap.xml"})
#x = SitemapReader({"Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml"})
#x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml" })

#ponto frio, walmart, amazon(http://www.amazon.com.br/sitemap-manual-index.xml) --> server error
#x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml", "Extra":"http://buscando.extra.com.br/sitemap.xml", "Netshoes": "http://www.netshoes.com.br/sitemap.xml", "Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml" })

#lista = x.run()
#persiste = MongoCollection()
#persiste.save_in_bulk([c.to_dict() for c in lista])
