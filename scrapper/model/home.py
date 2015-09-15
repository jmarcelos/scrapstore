from helper.mongomodel import MongoCollection
from helper.crawler import Crawler

class HomePage(MongoCollection, Crawler):

    url = None
    prioridade = 0
    data_scan = None
    site = None

    def __init__(self, url=None, site=None, prioridade=10, data_scan=None):
        self.url = url
        self.prioridade = prioridade
        self.data_scan = data_scan
        self.site = site
        Crawler.__init__(self)

    def parse(self):
        page_number = 1
        product_list = []
        while True:
            url = self.url + "?" + self.getPaginationRule(page_number)
            try:
                doc = self.crawlHTML(url)
                product_list_aux = self.getParsedContent(doc)
                print url
                if not product_list_aux:
                    break
                product_list = product_list + product_list_aux
            except Exception, e:
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                print e
                continue

            page_number += 1
        print "final " + str(len(product_list))
        return product_list

    def save_in_bulk(self,content_list):
        super(HomePage, self).save_in_bulk(self.HOMELIST_COLLETION, [c.to_dict() for c in content_list])

    def getList(self):
        super(HomePage, self).read_content()

#from sitemap import HomePageAmericanas; acom = HomePageAmericanas(); acom.url = "http://www.americanas.com.br/linha/267868/informatica/notebook"; acom.parse()

class HomePageAmericanas(HomePage):

    pagination_parameters = "ofertas.limit=%s&ofertas.offset=%s"
    quantidade_por_pagina = 90

    def getParsedContent(self, doc):
        product_list = self.getHTMLInfo(doc, '//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')
        return product_list

    def getPaginationRule(self, page_number):
        if page_number == 1:
            return "ofertas.limit=%s" % self.quantidade_por_pagina
        return "ofertas.limit=%s&ofertas.offset=%s" % (self.quantidade_por_pagina, self.quantidade_por_pagina * page_number)

    def getList(self):
        return super(HomePageAmericanas, self).read_content(self.HOMELIST_COLLETION, {'site': 'Americanas'})
