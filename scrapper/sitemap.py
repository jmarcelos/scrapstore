from model.home import HomePageAmericanas, HomePage, HomePageExtra, HomePageNetshoes
from model.product import AmericanasProduct, NetshoesProduct
from helper.crawler import Crawler
import sys

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
            content_dict = self.readSitemap(sitemap_content, sitemap_key)
            total_inserted_aux = self.save_sitemap_content(content_dict)
            total_inserted += total_inserted_aux
        return total_inserted

    def save_sitemap_content(self, content_dict):
        total_inserted = 0

        for key, content_list in content_dict.iteritems():
            total_inserted_aux = 0
            if content_list:
                print 'tudao: ' + str(len (content_list))
                content_list = set(content_list)
                content_list = list(content_list)
                print 'reduzido: ' + str(len (content_list))
                total_inserted_aux = len(content_list[0].save_in_bulk(content_list))
            total_inserted += total_inserted_aux
        return total_inserted


    def readSitemap(self, localizacoes, sitemap_key):
        homepage_list = []
        product_list = []
        content_sitemap = {'product': product_list, 'homepage': homepage_list}
        for local in localizacoes:
            url = local.firstChild.nodeValue
            if "xml" in url:
                content_sitemap_aux = self.readSitemap(self.get_sitemap_content(url), sitemap_key)
                content_sitemap['product'] = content_sitemap['product'] + content_sitemap_aux['product']
                content_sitemap['homepage'] = content_sitemap['homepage'] + content_sitemap_aux['homepage']
            elif "/produto/" in url:
                # apenas a Netshoes tem paginas de produto dentro do sitemap
                product = NetshoesProduct(url=url, site="Netshoes")
                complete_product = product.parse()
                product_list.append(complete_product)
            else:
                homepage = HomePage(url=url, priority=10, site=sitemap_key)
                homepage_list.append(homepage)
        return content_sitemap

    def get_sitemap_content(self, url):
        xmldoc = self.crawler.crawl_XML(url)
        urls = self.crawler.get_XML_info(xmldoc, 'loc')
        return urls



if __name__ == '__main__':

    sites = {"Americanas":"http://www.americanas.com.br/sitemap_index_acom.xml",
            "Extra":"http://buscando.extra.com.br/sitemap.xml",
            "Netshoes": "http://www.netshoes.com.br/sitemap.xml",
            "Submarino": "http://www.submarino.com.br/sitemap_index_suba.xml" }
    if sys.argv and sys.argv[1] == 'sitemap-read':
        #gera as homepages a partir dos sitemaps
        try:
            sitemap = sites[sys.argv[2]]
            print "Opcao de leitura do sitemap, iniciando geracao das homes de produto do site %s" % sitemap
            x = SitemapReader({sys.argv[2]: sitemap})
            total_inserted = x.run()
            print "Foram lidas %d paginas, que podem ser homes e pagina de produtos" % total_inserted
        except Exception:
            print  'Formato de sitemap nao conhecido'
    elif sys.argv and sys.argv[1] == 'product-read':
        print "Inicia o processo de leitura das homes %s para gerar as paginas e produto" % sys.argv[2]

        module_path = "model.home"
        class_name = sys.argv[2]
        try:
            if class_name:
                module = __import__(module_path, fromlist=[class_name])
        except ImportError:
            raise ValueError("Module %s could not be imported" % (module_path))

        try:
            cls_ = getattr(module, class_name)
        except AttributeError:
            raise ValueError("Module %s has no class %s" % (module_path, class_name))

        home_page = cls_()
        homepage_list = home_page.get_list()
        import pdb; pdb.set_trace()
        for home in homepage_list:
            home_page.url = home['url']
            product_list_aux = home_page.parse()

            home_page.scanned().save()




        #gera a lista de produtos a partir do sitemap



# def generateProductPage():
# #roda homepage gerando produto
#     #a = HomePageAmericanas()
#     a = HomePageExtra()
#     homepage_list = ['http://buscando.extra.com.br/search?p=Q&srid=S1-USESD01&lbc=extra&ts=custom&w=Moto%20G&uid=420861237&method=and&isort=score&view=list&sli_jump=1&srt=12']#a.get_list()
#     set_product_ids = set()
#     for home in homepage_list:
#         #a.url = home['url']
#         a.url = home
#         product_list_aux = a.parse()
#         print product_list_aux
#         product_list = []
#         for product in product_list_aux:
#             import pdb; pdb.set_trace()
#             #prodAmericanas = AmericanasProduct(url=product)
#             prodExtra = ExtraProduct(url=product)
#             if not product[1] in set_product_ids:
#                 prodExtra.url = product[0]
#                 prodExtra.id = product[1]
#                 product_list.append(prodExtra)
#             else:
#                 print "Duplicado: " + str(prodExtra.id) + "  -  " + prodExtra.url
#         persistencia = ExtraProduct()
#
#         persistencia.save_in_bulk(product_list)

#generateProductPage()
# a = HomePageAmericanas(url="http://www.americanas.com.br/linha/267868/informatica/notebook")
# product_list = []
# product_list_aux = a.parse()
# for product in product_list_aux:
#     prodAmericanas = AmericanasProduct(url=product)
#     prodAmericanas.url = product[0]
#     prodAmericanas.id = product[1]
#     product_list.append(prodAmericanas)
#
# print [str(prodAmericanas.id) + " - " + prodAmericanas.url for prodAmericanas in product_list]
