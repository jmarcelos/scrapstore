from datetime import datetime
from helper.crawler import Crawler
from mongoengine import *
from decimal import Decimal
import re

class ProductHistory(EmbeddedDocument):

    scan_date = DateTimeField(default=datetime.now)
    price = DecimalField()

    def to_dict(self):
        return {"price": self.price, "scan_date": self.scan_date}


class Product(Crawler, Document):

    url = StringField(max_length=250, required=True, primary_key=True)
    id = IntField()
    name = StringField(max_length=200)
    description = StringField(max_length=200)
    site = StringField(max_length=20, required=True)
    keywords = SortedListField(StringField(), default=list)
    picture = StringField(max_length=200)
    product_history = ListField(EmbeddedDocumentField(ProductHistory))
    last_price = DecimalField()
    last_scan_date = DateTimeField()
    priority = IntField(default=10)


    meta = {'collection': 'PRODUCT_COLLETION', 'allow_inheritance': True}

    def to_dict(self):
        return { "url" : self.url, "id": self.id, "name": self.name, "description" : self.description,  "site": self.site,
                 "keywords":self.keywords, "picture": self.picture, "product_history": self.produc_history.to_dict,
                 "last_price": self.last_price, "last_scan_date": self.last_scan_date, "priority": self.priority }

    def parse(self):
        if self.url:
            try:
                doc = self.crawl_HTML(self.url)
                self = self.get_parsed_content(doc)
            except Exception, e:
                print 'deu merda'
                print e
        return self

    def __str__(self):
        return "Produto(id=%s, nome=%s, site=%s, url=%s, last_scan_date=%s)" % (self.id, self.name, self.site, self.url, str(self.last_scan_date))

    def __repr__(self):
        return  self.__str__()

    def __hash__(self):
        return hash(self.id) ^ hash(self.url)


class AmericanasProduct(Product):

    meta = {'collection': 'AMERICANA_PRODUCTLIST_COLLETION'}

class NetshoesProduct(Product):

    meta = {'collection': 'NETSHOES_PRODUCTLIST_COLLETION'}

    pattern = '([0-9]+.[0-9]+)'

    def get_parsed_content(self, doc):
        self.name = self.get_HTML_info(doc, '//head/meta[@name="title"]/@content')[0]#tem que sliptar por |
        self.name, trash = self.name.split('|')
        self.name = self.name.strip()
        self.site='Netshoes'
        self.last_price = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/div/div[@class="price-holder"]/p[@class="new-price-holder"]/strong[@class="new-price"]')[0].text
        self.last_price = Decimal(re.search(self.pattern, self.last_price.replace(',', '.' )).group())
        self.last_scan_date = datetime.now()
        self.description = self.get_HTML_info(doc, '//head/meta[@name="description"]/@content')[0]
        self.picture = self.get_HTML_info(doc, '//head/meta[@property="og:image"]/@content')[0]
        self.product_history.append(ProductHistory(price=self.last_price))
        self.id = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/input[@name="skuId"]/@value')[0].replace("-", "")

        return self


class SubmarinoProduct(Product):

    meta = {'collection': 'SUBMARINO_PRODUCTLIST_COLLETION'}

class ExtraProduct(Product):

    meta = {'collection': 'EXTRA_PRODUCTLIST_COLLETION'}
