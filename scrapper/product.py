from datetime import datetime
from mongomodel import MongoCollection

class Product(MongoCollection):

    url = None
    name = None
    price = 0
    scan_date = None
    site = None

    def __init__(self, url=None, name=None, price=0, scan_date=None, site=None):
        self.url = url
        self.name = name
        self.price = price
        self.scan_date = scan_date
        self.site = site
