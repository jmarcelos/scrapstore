# coding=utf-8
from datetime import datetime
from helper.crawler import Crawler
from mongoengine import *
from decimal import Decimal
import re
import logging

class ProductHistory(EmbeddedDocument):

    scan_date = DateTimeField(default=datetime.now)
    price = DecimalField()

    def to_dict(self):
        return {"price": self.price, "scan_date": self.scan_date}


class Product(Document, Crawler):

    url = StringField(max_length=400, required=True, unique=True)
    prod_id = IntField(default=-1, primary_key=True)
    name = StringField(max_length=200)
    description = StringField(max_length=200)
    site = StringField(max_length=20, required=True)
    keywords = SortedListField(StringField(), default=list)
    picture = StringField(max_length=200)
    product_history = ListField(EmbeddedDocumentField(ProductHistory))
    last_price = DecimalField()
    last_scan_date = DateTimeField()
    priority = IntField(default=10)


    meta = {'collection': 'PRODUCT_COLLECTION', 'allow_inheritance': True, 'abstract': True}


    def update_content(self):
        self.parse()
        try:
            self.save()
        except Exception, e:
            logging.error(e)


    def to_dict(self):
        return { "url" : self.url, "prod_id": self.prod_id, "name": self.name, "description" : self.description,  "site": self.site,
                 "keywords":self.keywords, "picture": self.picture, "product_history": self.product_history.to_dict,
                 "last_price": self.last_price, "last_scan_date": self.last_scan_date, "priority": self.priority }

    def parse(self):
        if self.url:
            try:
                doc = self.crawl_HTML(self.url)
                self = self.get_parsed_content(doc)
            except Exception, e:
                logging.error(e)
        return self

    def get_parsed_content(self, doc):
        raise NotImplementedError()

    def __str__(self):
        return "%s(prod_id=%s, nome=%s, site=%s, url=%s, last_scan_date=%s)" % (self.__class__.__name__,self.prod_id, self.name, self.site, self.url, str(self.last_scan_date))

    def __repr__(self):
        return  self.__str__()

    def __hash__(self):
        return hash(self.prod_id) ^ hash(self.url)

    @classmethod
    def update_products(cls):
        product_list = cls.objects
        logging.debug("Atualizando %d produtos", len(product_list))
        for product in product_list:
            product.update_content()
            logging.debug('Produto atualizado: %s', product)

class AmericanasProduct(Product):
    meta = {'collection': 'PRODUCT_AMERICANAS_COLLECTION'}

    def get_parsed_content(self, doc):
        self.name = self.get_HTML_info(doc, '//div[@class="mp-title"]/h1/@title')[0]
        self.site='Americanas'
        self.last_price = self.get_HTML_info(doc, '//div[@class="mp-pricebox-wrp"]/@data-price')[0]
        self.last_price = Decimal(self.last_price)
        self.last_scan_date = datetime.now()
        self.description = self.get_HTML_info(doc, '//head/meta[@name="description"]/@content')[0]
        self.keywords = self.get_HTML_info(doc, '//head/meta[@name="keywords"]/@content')[0].split(',')
        self.picture = self.get_HTML_info(doc, '//div/div/div/div/ul[@class="a-carousel-list"]/li/img/@src')[0]
        self.product_history.append(ProductHistory(price=self.last_price))
        #self.prod_id = self.get_HTML_info(doc, '//div[@class="mp-pricebox-wrp"]/@data-sku')[0]

        return self


class NetshoesProduct(Product):

    pattern = '([0-9]+.[0-9]+)'

    def get_parsed_content(self, doc):
        self.name = self.get_HTML_info(doc, '//head/meta[@name="title"]/@content')[0].encode("UTF-8") #tem que sliptar por |
        self.name, trash = self.name.split('|')
        self.name = self.name.strip()
        self.site='Netshoes'
        self.last_price = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/div/div[@class="price-holder"]/p[@class="new-price-holder"]/strong[@class="new-price"]')[0].text
        self.last_price = Decimal(re.search(self.pattern, self.last_price.replace(',', '.' )).group())
        self.last_scan_date = datetime.now()
        self.description = self.get_HTML_info(doc, '//head/meta[@name="description"]/@content')[0]
        self.picture = self.get_HTML_info(doc, '//head/meta[@property="og:image"]/@content')[0]
        self.product_history.append(ProductHistory(price=self.last_price))
        self.prod_id = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/input[@name="skuId"]/@value')[0].replace("-", "")

        return self


class SubmarinoProduct(Product):

    def get_parsed_content(self, doc):
        self.name = self.get_HTML_info(doc, '//div[@class="mp-title"]/h1/@title')[0]
        self.site='Americanas'
        self.last_price = self.get_HTML_info(doc, '//div[@class="mp-pricebox-wrp"]/@data-price')[0]
        self.last_price = Decimal(self.last_price)
        self.last_scan_date = datetime.now()
        self.description = self.get_HTML_info(doc, '//head/meta[@name="description"]/@content')[0]
        self.keywords = self.get_HTML_info(doc, '//head/meta[@name="keywords"]/@content')[0].split(',')
        self.picture = self.get_HTML_info(doc, '//div/div/div/div/ul[@class="a-carousel-list"]/li/img/@src')[0]
        self.product_history.append(ProductHistory(price=self.last_price))
        #self.prod_id = self.get_HTML_info(doc, '//div[@class="mp-pricebox-wrp"]/@data-sku')[0]

        return self

class ExtraProduct(Product):
    pass
