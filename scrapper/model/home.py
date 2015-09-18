import re
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
            url = self.url + "?" + self.get_pagination_rule(page_number)
            try:
                doc = self.crawl_HTML(url)
                product_list_aux = self.get_parsed_content(doc)
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
        super(HomePage, self).save_in_bulk(self.HOMELIST_COLLETION, content_list)

    def get_list(self):
        super(HomePage, self).read_content()

    def __str__(self):
        return "Classe: %s url:%s site=%s, prioridade=%d, data_scan=%s" %(self.__class__.__name__, self.self.url, self.site, self.prioridade, self.data_scan)

    def __repr__(self):
        return self.__str__()


#from sitemap import HomePageAmericanas; acom = HomePageAmericanas(); acom.url = "http://www.americanas.com.br/linha/267868/informatica/notebook"; acom.parse()

class HomePageAmericanas(HomePage):

    pagination_parameters = "ofertas.limit=%s&ofertas.offset=%s"
    quantidade_por_pagina = 90

    def get_parsed_content(self, doc):
        url_list = self.get_HTML_info(doc, '//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')
        id_list = self.get_HTML_info(doc, '//div[@class="paginado"]/section/article/div/form/meta/@content')
        return zip(url_list, id_list)

    def get_pagination_rule(self, page_number):
        if page_number == 1:
            return "ofertas.limit=%s" % self.quantidade_por_pagina
        return "ofertas.limit=%s&ofertas.offset=%s" % (self.quantidade_por_pagina, self.quantidade_por_pagina * page_number)

    def get_list(self):
        return super(HomePageAmericanas, self).read_content(self.HOMELIST_COLLETION, {'site': 'Americanas'})


class HomePageSubmarino(HomePageAmericanas):

    def get_list(self):
        return super(HomePageSubmarino, self).read_content(self.HOMELIST_COLLETION, {'site': 'Submarino'})


class HomePageExtra(HomePage):

    quantidade_por_pagina = 20
    pattern = '([0-9]+)'


    def parse(self):
        url_temp = self.url
        product_list = []

        while url_temp:
            try:

                doc = self.crawl_HTML(url_temp)
                product_list_aux = self.get_parsed_content(doc)
                product_list = product_list + product_list_aux
                url_temp = self.get_pagination_rule(doc)[0]
            except Exception, e:
                import traceback
                traceback.print_exc()
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                print e
                raise Exception()

        print "final " + str(len(product_list))
        return product_list

    def get_parsed_content(self, doc):
        url_list = self.get_HTML_info(doc, '//div[@class="prateleira"]/ul[@class="vitrineProdutos"]/li/div[@class="hproduct"]/a/@href')
        title_list = self.get_HTML_info(doc, '//div[@class="prateleira"]/ul[@class="vitrineProdutos"]/li/div[@class="hproduct"]/a/@title')
        id_list = self.__get_ids(title_list)
        return zip(url_list, id_list)

    def get_pagination_rule(self, doc):
        return self.get_HTML_info(doc, '//div[@id="sli_pagination_header"]/div[@class="pagination"]/ul[@class="ListaPaginas"]/li[@class="next"]/a/@href')

    def get_list(self):
        return super(HomePageExtra, self).read_content(self.HOMELIST_COLLETION, {'site': 'Extra'})

    def __get_ids(self, title_list):
        return map(self.__extractor, title_list)

    def __extractor(self, content):
        match_content = re.search(self.pattern, content)
        return match_content.group()
