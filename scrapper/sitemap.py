from model.home import HomePageAmericanas, HomePage, HomePageExtra, HomePageNetshoes
from model.product import AmericanasProduct, NetshoesProduct
from helper.crawler import Crawler
import sys


def getHomePageClass(name):
    module_path = "model.home"
    name = "HomePage" + name
    try:
        module = __import__(module_path, fromlist=[name])
    except ImportError:
        raise ValueError("Module %s could not be imported" % (module_path))

    try:
        cls_ = getattr(module, name)
    except AttributeError:
        raise ValueError("Module %s has no class %s" % (module_path, class_name))

    return cls_

class SitemapReader():

    sitemap = []
    site = None

    def __init__(self, sitemaps):
        self.sitemaps = sitemaps
        self.crawler = Crawler()

    def run(self):
        full_homepage = {'product' : [], 'homepage': []}
        total_inserted = 0
        for sitemap_key in self.sitemaps:
            total_inserted_aux = 0
            url = self.sitemaps[sitemap_key]
            sitemap_content = self.get_sitemap_content(url)
            content_dict = self.read_sitemap(sitemap_content, sitemap_key)
            total_inserted_aux = self.save_sitemap_content(content_dict)
            total_inserted += total_inserted_aux
        return total_inserted

    def save_sitemap_content(self, content_dict):
        total_inserted = 0

        for key, content_list in content_dict.iteritems():
            total_inserted_aux = 0
            if content_list:
                content_list = set(content_list)
                content_list = list(content_list)
                if key == 'homepage':
                    total_inserted_aux = len(HomePage.objects.insert(content_list))
                else:
                    total_inserted_aux = len(NetshoesProduct.objects.insert(content_list))
            total_inserted += total_inserted_aux
        return total_inserted


    def read_sitemap(self, localizacoes, sitemap_key):
        homepage_list = []
        product_list = []
        content_sitemap = {'product': product_list, 'homepage': homepage_list}
        for local in localizacoes:
            url = local.firstChild.nodeValue
            if "xml" in url:
                content_sitemap_aux = self.read_sitemap(self.get_sitemap_content(url), sitemap_key)
                content_sitemap['product'] = content_sitemap['product'] + content_sitemap_aux['product']
                content_sitemap['homepage'] = content_sitemap['homepage'] + content_sitemap_aux['homepage']
            elif "/produto/" in url:
                # apenas a Netshoes tem paginas de produto dentro do sitemap
                product = NetshoesProduct(url=url, site=sitemap_key)
                complete_product = product.parse()
                product_list.append(complete_product)
            else:
                home_page_class = getHomePageClass(sitemap_key)
                homepage = home_page_class(url=url, priority=10, site=sitemap_key)
                homepage_list.append(homepage)
        return content_sitemap

    def get_sitemap_content(self, url):
        xmldoc = self.crawler.crawl_XML(url)
        urls = self.crawler.get_XML_info(xmldoc, 'loc')
        return urls


class HomePageReader(object):

    def read_content(self, homepage_class_name):
        product_list = []
        i = 0
        for home in homepage_class_name.objects(priority__lte=5):
            product_list.extend(home.parse())
            i+=1
            print 'Total parcial: %d homes lidas e %d produtos' %(i, len(product_list))

        new_products_set = set(product_list)
        new_products_list = list(new_products_set)

        print "Foram lidos %d" % len(homepage.add_products(new_products_list))
        return


if __name__ == '__main__':

    sites = {"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml",
            "Extra":"http://buscando.extra.com.br/sitemap.xml",
            "Netshoes": "http://www.netshoes.com.br/sitemap.xml",
            "Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml" }
    if sys.argv and sys.argv[1] == 'sitemap-read':
        #gera as homepages a partir dos sitemaps
        sitemap = sites[sys.argv[2]]
        print "Opcao de leitura do sitemap, iniciando geracao das homes de produto do site %s" % sitemap
        x = SitemapReader({sys.argv[2]: sitemap})
        total_inserted = x.run()
        print "Foram lidas %d paginas, que podem ser homes e pagina de produtos" % total_inserted
    elif sys.argv and sys.argv[1] == 'product-read':
        print "Inicia o processo de leitura das homes %s para gerar as paginas e produto" % sys.argv[2]

        cls_ = getHomePageClass(sys.argv[2])

        home_page_reader = HomePageReader()
        home_page_reader.read_content(cls_)
