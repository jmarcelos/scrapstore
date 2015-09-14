from datetime import datetime
from mongomodel import MongoCollection

class Product(MongoCollection):
    url = None
    name = None
    description = None
    site = None
    keywords = []
    picture = None
    product_history = []
    last_price = 0.0
    last_scan_date = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, url, name, site, last_price, last_scan_date, description=None, keywords=None, picture=None, product_history=None):
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
    AMERICANAS_PRODUCTLIST_COLLETION = "AMERICANAS_PRODUCTLIST_COLLETION"

    def save_in_bulk(self, content_list):
        if content_list:
            super(AmericanasProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, [c.to_dict() for c in content_list])

    def getList(self):
        return super(AmericanasProduct, self).read_content(self.AMERICANAS_PRODUCTLIST_COLLETION)
