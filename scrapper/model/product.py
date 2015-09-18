from datetime import datetime
from helper.mongomodel import MongoCollection

class Product(MongoCollection):
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

class ProductHistory(MongoCollection):

    scan_date = datetime.now().strftime("%Y-%m-%d")
    price = 0.00

    def __init__(self, price, scan_date):
        self.price = price
        self.scan_date = scan_date


class AmericanasProduct(Product):

    def save_in_bulk(self, content_list):
        super(AmericanasProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, content_list)


class SubmarinoProduct(Product):

    def save_in_bulk(self, content_list):
        super(AmericanasProduct, self).save_in_bulk(self.SUBMARINO_PRODUCTLIST_COLLETION, content_list)


class ExtraProduct(Product):

    def save_in_bulk(self, content_list):
        super(AmericanasProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, content_list)
