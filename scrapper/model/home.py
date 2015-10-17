import re
from helper.crawler import Crawler
from datetime import datetime
from mongoengine import *
from product import *
import logging


class HomePage(Crawler, Document):

    url = StringField(max_length=250, required=True, unique=True)
    priority = IntField(default=10)
    last_scan_date = DateTimeField()
    site = StringField(max_length=20, required=True)

    meta = {'collection': 'HOMELIST_COLLETION', 'allow_inheritance': True}

    def parse(self):
        raise NotImplementedError()

    def generate_product_list(self, url_id_list):
        raise NotImplementedError()

    @staticmethod
    def get_products():
        return self.__class__.objects()

    @staticmethod
    def add_products(product_list):
        i = 0
        for product in product_list:
            try:
                product.save()
                i+=1
            except Exception as e:
                logging.error(e)

        logging.debug("Tentativa de inserir %d registros, mas foram inseridos %d", len(product_list), i)
        return i

    def scanned(self):
        self.last_scan_date = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return "Classe: %s url:%s site=%s, prioridade=%d, data_scan=%s" %(self.__class__.__name__, self.url, self.site, self.priority, self.last_scan_date)

    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.site) ^ hash(self.url)

#from sitemap import HomePageAmericanas; acom = HomePageAmericanas(); acom.url = "http://www.americanas.com.br/linha/267868/informatica/notebook"; acom.parse()

class HomePageAmericanas(HomePage):

    pagination_parameters = "ofertas.limit=%s&ofertas.offset=%s"
    quantidade_por_pagina = 90

    meta = {'allow_inheritance': True}

    def parse(self):
        logging.debug('Iniciando parser americanas')
        page_number = 0
        product_list = []

        while True:
            url = self.url + "?" + self.get_pagination_rule(page_number)
            logging.debug(url)
            page_number += 1
            try:
                doc = self.crawl_HTML(url)
                product_list_aux = self.get_parsed_content(doc)
                if not product_list_aux:
                    break
                product_list = product_list + product_list_aux
            except Exception, e:
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                logging.error(e)


        logging.debug("Homes parseadas, lidos  %d produtos", len(product_list))
        return self.generate_product_list(product_list)

    def get_parsed_content(self, doc):
        url_list = self.get_HTML_info(doc, '//div[@class="paginado"]/section/article/div/form/div[@class="productImg"]/a/@href')
        id_list = self.get_HTML_info(doc, '//div[@class="paginado"]/section/article/div/form/meta/@content')
        return zip(url_list, id_list)

    def get_pagination_rule(self, page_number):
        if page_number < 1:
            return "ofertas.limit=%s" % self.quantidade_por_pagina
        return "ofertas.limit=%s&ofertas.offset=%s" % (self.quantidade_por_pagina, self.quantidade_por_pagina * page_number)

    def generate_product_list(self, url_id_list):
        product_list = []

        for content in url_id_list:
            americanas = AmericanasProduct(prod_id=content[1], url=content[0], site='Americanas')
            product_list.append(americanas)

        logging.debug("Retornando %d produtos", len(product_list))
        return product_list


class HomePageSubmarino(HomePageAmericanas):
    def generate_product_list(self, url_id_list):
        product_list = []

        for content in url_id_list:
            americanas = SubmarinoProduct(prod_id=content[1], url=content[0], site='Americanas')
            product_list.append(americanas)

        logging.debug("Retornando %d produtos", len(product_list))
        return product_list


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
                if not product_list_aux:
                    break
                product_list = product_list + product_list_aux
                url_temp = self.get_pagination_rule(doc)
            except Exception, e:
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                logging.error(e)


        logging.debug("Homes parseadas, lidos  %d produtos", len(product_list))
        return self.generate_product_list(product_list)

    def generate_product_list(self, url_id_list):
        product_list = []

        for content in url_id_list:
            extra = ExtraProduct(url=content[0], prod_id=content[1], site='Extra')
            product_list.append(extra)

        logging.debug("Retornando lista de produtos")
        return product_list

    def get_parsed_content(self, doc):
        url_list = self.get_HTML_info(doc, '//div[@class="prateleira"]/ul[@class="vitrineProdutos"]/li/div[@class="hproduct"]/a/@href')
        title_list = self.get_HTML_info(doc, '//div[@class="prateleira"]/ul[@class="vitrineProdutos"]/li/div[@class="hproduct"]/a/@title')
        id_list = self.__get_ids(title_list)
        return zip(url_list, id_list)

    def get_pagination_rule(self, doc):
        pags = self.get_HTML_info(doc, '//div[@id="sli_pagination_header"]/div[@class="pagination"]/ul[@class="ListaPaginas"]/li[@class="next"]/a/@href')
        if pags:
            return pags[0]
        return

    def __get_ids(self, title_list):
        return map(self.__extractor, title_list)

    def __extractor(self, content):
        match_content = re.search(self.pattern, content)
        return match_content.group()

    def to_dict(self):
        return { "url" : self.url, "priority": self.priority, "last_scan_date": self.last_scan_date, "site": self.site}


class HomePageNetshoes(HomePage):

    pagination_parameters = "?No=%d"
    quantidade_por_pagina = 60
    main_url = "http://netshoes.com.br"
    page_number = 1
    def parse(self):
        url_temp = self.url
        product_list = []

        while url_temp:
            try:
                doc = self.crawl_HTML(url_temp)
                product_list_aux = self.get_parsed_content(doc)
                if not product_list_aux:
                    break
                product_list = product_list + product_list_aux
                url_temp = self.get_pagination_rule(doc)
            except Exception, e:
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                logging.error(e)

        return self.generate_product_list(product_list)

    def get_pagination_rule(self, doc):
        page = self.page_number
        self.page_number +=1
        if page == 1:
            return self.url
        return self.url + self.pagination_parameters % (self.quantidade_por_pagina * page)


    def get_parsed_content(self, doc):
        logging.debug("Parseando conteudo Netshoes")
        url_relative_list = self.get_HTML_info(doc, '//div[@class="main-content "]/div[@class="results-wrapper"]/ul[@class="product-list"]/li/span[@class="single-product"]/a/@href')
        products_list = self.get_HTML_info(doc, '//div[@class="main-content "]/div[@class="results-wrapper"]/ul[@class="product-list"]/li/span[@class="single-product"]/a/@data-product')
        url_list = self.get_full_url(url_relative_list)
        skus_list = self.__get_ids(products_list)
        return zip(url_list, skus_list)

    def __get_ids(self, product_list):
        return map(self.__extractor, product_list)

    def __extractor(self, content):
        #trocar por expressao regular
        return content.split(',')[6].split(':')[1].replace('"', '').replace('-', '')

    def get_full_url(self, url_relative_list):
        return map(lambda url: self.main_url + url,  url_relative_list)
