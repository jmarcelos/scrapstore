import urllib2
from xml.dom import minidom
from mongomodel import MongoCollection
from lxml import html as lhtml

class HomePage(MongoCollection):

    url = None
    prioridade = 0
    data_scan = None
    site = None

    USER_AGENT = ('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')

    def __init__(self, url=None, site=None, prioridade=10, data_scan=None):
        self.url = url
        self.prioridade = prioridade
        self.data_scan = data_scan
        self.site = site

#precisa refator, nao utilizei o crawler porque a americanas retornava uma listagem estatica de 30 elementos, independente da pagina

    def parse(self):
        page_number = 1
        product_list = []

        while True:

            opener = urllib2.build_opener()
            opener.addheaders = [self.USER_AGENT]
            url = self.url + "?" + self.getPaginationRule(page_number)
            file = opener.open(url)
            file_content = file.read()
            file.close()
            doc = lhtml.fromstring(file_content)
            product_list_aux = self.getProductList(doc)
            print url + "  " + str(len(product_list_aux))
            print product_list_aux
            if not product_list_aux:
                break
            product_list = product_list + product_list_aux
            page_number += 1
            #product_list_aux = []

        print "final " + str(len(product_list))
        print product_list

    def getProductList(self, doc):
        return []

    def getPaginationRule(self, page_number):
        return ""

    def save_in_bulk(self,list_content):
        super(HomePage, self).save_in_bulk(self.PRODUCTLIST_COLLETION, [c.to_dict() for c in list_content])


#from sitemap import HomePageAmericanas; acom = HomePageAmericanas(); acom.url = "http://www.americanas.com.br/linha/267868/informatica/notebook"; acom.parse()

#para crawlear cada home e preciso carregar o objeto e depois executar o parse que ira retornar as urls de produto
class HomePageAmericanas(HomePage):

    pagination_parameters = "ofertas.limit=%s&ofertas.offset=%s"
    quantidade_por_pagina = 90

    def getProductList(self, doc):
        return  doc.xpath('//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')

    def getPaginationRule(self, page_number):
        if page_number == 1:
            return "ofertas.limit=%s" % self.quantidade_por_pagina
        return "ofertas.limit=%s&ofertas.offset=%s" % (self.quantidade_por_pagina, self.quantidade_por_pagina * page_number)
