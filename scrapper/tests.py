import unittest
from model.home import HomePageAmericanas, HomePage, HomePageExtra, HomePageNetshoes
from sitemap import HomePageReader

class TestHomeModel(unittest.TestCase):


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

    def test_first_product_insertition(self):
        x = HomePageReader()
        x.read_content(HomePageExtra())


if __name__ == '__main__':
    unittest.main()
