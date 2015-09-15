from model.home import HomePageAmericanas, HomePage
from model.product import AmericanasProduct
from helper.crawler import Crawler


class SitemapReader():

    sitemap = []
    site = None

    def __init__(self, sitemaps):
        print "iniciando a leitura"
        self.sitemaps = sitemaps
        self.crawler = Crawler()

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
        xmldoc = self.crawler.crawlXML(url)
        localizacoes = self.crawler.getXMLInfo(xmldoc, 'loc')
        return localizacoes



def generateHomePages():

# roda sitemap gerando homepage
#x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml" })
#x = SitemapReader({"Netshoes": "http://www.netshoes.com.br/sitemap.xml"})
#x = SitemapReader({"Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml"})
#x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml" })
#ponto frio, walmart, amazon(http://www.amazon.com.br/sitemap-manual-index.xml) --> server error
    x = SitemapReader({"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml", "Extra":"http://buscando.extra.com.br/sitemap.xml", "Netshoes": "http://www.netshoes.com.br/sitemap.xml", "Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml" })
    lista = x.run()
    persiste = HomePage()
    persiste.save_in_bulk(lista)

#generateHomePages()

def generateProductPage():
#roda homepage gerando produto
    a = HomePageAmericanas()
    homepage_list = a.getList()
    for home in homepage_list:
        a.url = home['url']
        product_list_aux = a.parse()
        product_list = []
        for product in product_list_aux:
            prodAmericanas = AmericanasProduct(url=product)
            prodAmericanas.url = product
            product_list.append(prodAmericanas)
        persistencia = AmericanasProduct()
        import pdb; pdb.set_trace()
        
        persistencia.save_in_bulk(product_list)

generateProductPage()
