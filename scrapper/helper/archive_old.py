# -*- coding: utf-8 -*-

from crawl import Crawler
from lxml import html as lhtml
from datetime import datetime
import json
from crawl import Crawler
from lxml import html as lhtml
from model import Product, ProductHistory
from re import sub



class Archive(Crawler):
	archive_host = "http://web.archive.org"
	archive_save = archive_host+"/save/"
	archive_search = "http://archive.org/wayback/available?"
	timestamp_mask = '%Y%m%d%H%M%S'

	url = None
	url_archive = None
	date = None
	timestamp = None

	def __init__(self, url, url_archive=None, date=None):
		self.url = url
		self.url_archive = url_archive
		self.date = date


	def to_dict(self):
		return self.__dict__

	def save(self):
		html,headers = Crawler().get(self.archive_save+self.url)
		for header in headers.split("\r\n"):
			dados = header.split(": ")
			if dados[0] == "Content-Location":
				self.url_archive=self.archive_host+dados[1]
				self.timestamp = dados[1].split("/")[2]
				self.date = datetime.strptime(self.timestamp, self.timestamp_mask)
				self.date = self.timestamp

	def findOne(self):
		search = "url=%s&timestamp=%s" % (self.url,self.date.strftime(self.timestamp))
		html,headers = Crawler().get(self.archive_search+search)
		data = json.loads(html)
		self.url_archive = data['archived_snapshots']['closest']['url']


def parse(url):
	html,headers = Crawler().get(url)
	doc = lhtml.fromstring(html)

	name = doc.cssselect('.a-main-product span[itemprop="name"]')[0].text
	price = doc.cssselect('.a-main-product span[itemprop="price"]')[0].text
	site = doc.cssselect('.spt-logo')[0].text
	description = doc.cssselect('meta[name="description"]')[0].get('content')
	keywords = doc.cssselect('meta[name="keywords"]')[0].get('content')
	picture = doc.cssselect('.a-carousel-item img[itemprop="thumbnail"]')[0].get('src')
	price = float(sub(r'[^\d,]', '', price).replace(",","."))
	archive = Archive(url)
	archive.save()

	product_history = ProductHistory(price, archive.date)
	product_history.save()

	product = Product(url, name, site, price, archive.date, description, keywords, picture, product_history )
	product.save_or_update({'url':url})

parse("http://www.americanas.com.br/produto/124132603/smartphone-samsung-galaxy-j5-duos-dual-chip-desbloqueado-android-5.1-tela-5-16gb-3g-wi-fi-camera-13mp-branco")
