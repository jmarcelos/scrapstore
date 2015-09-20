from datetime import datetime
from helper.mongomodel import MongoCollection
from helper.crawler import Crawler

class Product(MongoCollection, Crawler):

    url = None
    id = None
    name = None
    description = None
    site = None
    keywords = []
    picture = None
    product_history = []
    last_price = 0.0
    last_scan_date = datetime.now().strftime("%Y-%m-%d")
    priority = None

    def __init__(self, url=None, name=None, site=None, last_price=None, last_scan_date=None, description=None, keywords=None, picture=None, product_history=None):
        self.url = url
        self.name = name
        self.description = description
        self.keywords.append(keywords)
        self.picture = picture
        self.last_price = last_price
        self.last_scan_date = last_scan_date
        self.site = site
        self.product_history.append(product_history)
        Crawler.__init__(self)

    def parse(self):
        if self.url:
            try:
                doc = self.crawl_HTML(self.url)
                self = self.get_parsed_content(doc)
            except Exception, e:
                #caso tenha ocorrido o parse em uma pagina, eu escrevo a exception e continuo
                print e
        return self

    def __str__(self):
        return "Produto(id=%s, nome=%s, site=%s, url=%s, last_scan_date=%s)" % (self.id, self.name, self.site, self.url, str(self.last_scan_date))

    def __repr__(self):
        return  self.__str__()

    def __hash__(self):
        return hash(self.id) ^ hash(self.url)    

class ProductHistory(MongoCollection):

    scan_date = datetime.now().strftime("%Y-%m-%d")
    price = 0.00

    def __init__(self, price, scan_date):
        self.price = price
        self.scan_date = scan_date


class AmericanasProduct(Product):

    def save_in_bulk(self, content_list):
        return super(AmericanasProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, content_list)

class NetshoesProduct(Product):

    def save_in_bulk(self, content_list):
        return super(NetshoesProduct, self).save_in_bulk(self.NETSHOES_PRODUCTLIST_COLLETION, content_list)

    def get_parsed_content(self, doc):
        self.name = self.get_HTML_info(doc, '//head/meta[@name="title"]/@content')[0]#tem que sliptar por |
        self.name, trash = self.name.split('|')
        self.name = self.name.strip()
        self.site='Netshoes'
        self.last_price = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/div/div[@class="price-holder"]/p[@class="new-price-holder"]/strong[@class="new-price"]')[0].text
        self.last_scan_date = datetime.now().strftime("%Y-%m-%d")
        self.description = self.get_HTML_info(doc, '//head/meta[@name="description"]/@content')[0]
        self.picture = self.get_HTML_info(doc, '//head/meta[@property="og:image"]/@content')[0]
        self.product_history.append(ProductHistory(self.last_price, self.last_scan_date))
        self.id = self.get_HTML_info(doc, '//div[@class="product-buy-component "]/div[@class="product-buy-wrapper"]/div[@class="base-box buy-product-holder"]/form/input[@name="skuId"]/@value')[0].replace("-", "")
        return self


class SubmarinoProduct(Product):

    def save_in_bulk(self, content_list):
        super(SubmarinoProduct, self).save_in_bulk(self.SUBMARINO_PRODUCTLIST_COLLETION, content_list)


class ExtraProduct(Product):

    def save_in_bulk(self, content_list):
        super(ExtraProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, content_list)
