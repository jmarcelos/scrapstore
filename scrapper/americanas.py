from crawl import Crawler
from lxml import html as lhtml
from product import Product, ProductHistory
from re import sub
from archive import Archive

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


