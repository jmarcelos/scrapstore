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
    scan_date = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, url=None, name=None, site=None, description=None, price=0.00, keywords=None, picture=None, product_history=None):
        self.url = url
        self.name = name
        self.description = description
        self.keywords.append(keywords)
        self.picture = picture
        self.price = price
        self.site = site
        self.product_history.append(product_history)

class ProductHistory(MongoCollection):

    data_scan = datetime.now().strftime("%Y-%m-%d")
    price = 0.00

    def __init__(self, price):
        self.price = price


class AmericanasProduct(Product):
    AMERICANAS_PRODUCTLIST_COLLETION = "AMERICANAS_PRODUCTLIST_COLLETION"

    def save_in_bulk(self, content_list):
        if content_list:
            super(AmericanasProduct, self).save_in_bulk(self.AMERICANAS_PRODUCTLIST_COLLETION, [c.to_dict() for c in content_list])
