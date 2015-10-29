# coding=utf-8
import unittest
from model.home import HomePageAmericanas, HomePage, HomePageExtra, HomePageNetshoes
from sitemap import HomePageReader
from model.product import *
from helper.archive import Archive


class TestHomeModel(unittest.TestCase):
    pass


    # def test_leitura_prod_home(self):
    #     extra = HomePageExtra()
    #     extra.url = 'http://buscando.extra.com.br/search?p=Q&srid=S1-USESD01&lbc=extra&ts=custom&w=Moto%20G&uid=420861237&method=and&isort=score&view=list&sli_jump=1&srt=12'
    #     extra.site= 'Extra'
    #     product_list = []
    #     product_list_aux = extra.parse()
    #     return (True)
    # def test_save_in_bulk(self):
    #     extra = HomePageExtra(url = 'http://buscando.extra.com.br')
    #     extra.site= 'Extra'
    #     extra1 = HomePageExtra(url = 'http://buscando.extra.com.br/search')
    #     extra1.site= 'Extra'
    #     extra2 = HomePageExtra(url = 'http://buscando.extra.com.br/search?p=Q')
    #     extra2.site= 'Extra'
    #     print HomePage.objects.insert([extra1,extra2,extra])
    #     return (True)

    # def test_read_home(self):
    #     extra = HomePageExtra(url = 'http://buscando.extra.com.br/search?p=Q&srid=S1-USESD01&lbc=extra&ts=custom&w=Moto%20G&uid=420861237&method=and&isort=score&view=list&sli_jump=1&srt=12', site= 'Extra')
    #     extra.save()
    #     product_list = set()
    #     product_list_aux = set()
    #     for home in HomePageExtra.objects(url = 'http://buscando.extra.com.br/search?p=Q&srid=S1-USESD01&lbc=extra&ts=custom&w=Moto%20G&uid=420861237&method=and&isort=score&view=list&sli_jump=1&srt=12'):
    #         product_list = set(home.parse())
    #     total = len(product_list)
    #
    #     for home in HomePageExtra.objects(url = 'http://buscando.extra.com.br/search?p=Q&srid=S1-USESD01&lbc=extra&ts=custom&w=Moto%20G&uid=420861237&method=and&isort=score&view=list&sli_jump=1&srt=12'):
    #         product_list_aux = set(home.parse())
    #     total_final = len(product_list.union(product_list_aux))
    #     return total_final == total

    # def test_home_page_reader_americanas(self):
    #     home = HomePageAmericanas(url="http://www.americanas.com.br/sublinha/292159/beleza-e-saude/higiene-bucal/fio-dental")
    #     product_list = home.parse()
    #     self.assertEqual(12, len(product_list))
    #
    #     home = HomePageAmericanas(url="http://www.americanas.com.br/linha/292153/beleza-e-saude/higiene-bucal")
    #     product_list = home.parse()
    #     HomePageAmericanas.add_products(product_list)
    #     self.assertEqual(159, len(product_list))

#
#
class TestProductModel(unittest.TestCase):
    pass

    # def test_update_product_americanas(self):
    #     americanas_product = AmericanasProduct(url="http://www.americanas.com.br/produto/124258695/smartphone-samsung-galaxy-gran-prime-duos-dual-chip-android-tela-5-memoria-interna-8gb-3g-camera-8mp-dourado", prod_id=1)
    #     americanas_product.update_content()
    #     self.assertEqual(americanas_product.name, u'Smartphone Samsung Galaxy Gran Prime Duos Dual Chip Android Tela 5" Memória Interna 8GB 3G Câmera 8MP - Dourado')
    #     self.assertNotEqual(americanas_product.prod_id, 124258695)
    #     self.assertEqual(americanas_product.prod_id, 1)
    #     self.assertEqual(len(americanas_product.product_history), 1)
    #     americanas_product = AmericanasProduct.objects(prod_id =1)[0]
    #     americanas_product.update_content()
    #     self.assertEqual(americanas_product.name, u'Smartphone Samsung Galaxy Gran Prime Duos Dual Chip Android Tela 5" Memória Interna 8GB 3G Câmera 8MP - Dourado')
    #     self.assertNotEqual(americanas_product.prod_id, 124258695)
    #     self.assertEqual(americanas_product.prod_id, 1)
    #     self.assertEqual(len(americanas_product.product_history), 2)


    # def test_parse_americanas(self):
    #     americanas_product = AmericanasProduct(url="http://www.americanas.com.br/produto/124258695/smartphone-samsung-galaxy-gran-prime-duos-dual-chip-android-tela-5-memoria-interna-8gb-3g-camera-8mp-dourado")
    #     americanas_product = americanas_product.parse()
    #     americanas_product.save()
    #     self.assertEqual(americanas_product.name, u'Smartphone Samsung Galaxy Gran Prime Duos Dual Chip Android Tela 5" Memória Interna 8GB 3G Câmera 8MP - Dourado')

    #
    # def test_parse_Netshoes(self):
    #     netshoes_product = NetshoesProduct(url="http://www.netshoes.com.br/produto/tenis-mizuno-wave-ultima-6-149-0352-416")
    #     netshoes_product = netshoes_product.parse()
    #
    #
    #     self.assertEqual(netshoes_product.name.decode('utf-8'), u"Tênis Mizuno Wave Ultima 6 Pink e Amarelo")
    #
    # def test_parse_Submarino(self):
    #     submarino_product = SubmarinoProduct(url="http://www.submarino.com.br/produto/112941067/aparador-de-pelos-philips-multigroom-qg3340-16-com-acessorios")
    #     submarino_product = submarino_product.parse()
    #     self.assertEqual(submarino_product.name, u"Aparador de Pelos Philips Multigroom QG3340/16 com Acessórios")


# class TestArchive(unittest.TestCase):
#
#     def test_generate_image(self):
#         url = 'http://www.americanas.com.br/produto/124258695/smartphone-samsung-galaxy-gran-prime-duos-dual-chip-android-tela-5-memoria-interna-8gb-3g-camera-8mp-dourado'
#         archive = Archive()
#         content = archive.get_archived_url(url)
#         print content
#         self.assertTrue(None!=content)


if __name__ == '__main__':
    unittest.main()
