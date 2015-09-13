from crawl import Crawler
from lxml import html as lhtml
from product import Product
from re import sub
from archive import *

def parse(url):
	product = Product()
	html,headers = Crawler().get(url)
	doc = lhtml.fromstring(html)

	name = doc.cssselect('.a-main-product span[itemprop="name"]')[0].text
	price = doc.cssselect('.a-main-product span[itemprop="price"]')[0].text
	site = doc.cssselect('.spt-logo')[0].text
	product_history = ProductHistory(float(sub(r'[^\d,]', '', price).replace(",",".")))
	description = "PARSEAR A DESCRIPTION DO PRODUTO!!!!!"
	keywords = "PARSEAR AS KEYWORDS DO PRODUTO!!!!!"
	picture = "PARSEAR URL DA IMAGEM DO PRODUTO!!!!!"
	product = Product(url, name, site, description, keywords, picture, product_history)

	print product.to_dict()

	url_archive = archive(url)
	print url_archive

	# product.save()

parse("http://www.americanas.com.br/produto/124132603/smartphone-samsung-galaxy-j5-duos-dual-chip-desbloqueado-android-5.1-tela-5-16gb-3g-wi-fi-camera-13mp-branco")