import urllib2
from xml.dom import minidom
from pymongo import MongoClient
from datetime import datetime
from config import GLOBAL_CONFIG

class Sitemap:

    url = None
    prioridade = 0
    data_scan = None
    site = None

    def __init__(self, url=None, site=None, prioridade=10, data_scan=None):
        self.url = url
        self.prioridade = prioridade
        self.data_scan = data_scan
        self.site = site

    def to_dict(self):
        return self.__dict__

class SitemapReader:

    sitemap = []
    persiste = None
    site = None
    def __init__(self, sitemaps):
        print "iniciando a leitura"
        self.sitemaps = sitemaps
        self.persiste = PersistenceSiteMap(GLOBAL_CONFIG.get('Mongo', 'conexao'), GLOBAL_CONFIG.get('Mongo', 'database'))

    def run(self):
        for sitemap_key in self.sitemaps:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]

            file = opener.open(self.sitemaps[sitemap_key])
            file_content = file.read()
            file.close()
            xmldoc = minidom.parseString(file_content)

            localizacoes = xmldoc.getElementsByTagName('loc')

            for local in localizacoes:
                conteudo = Sitemap(url=local.firstChild.nodeValue, prioridade=10, site=self.site)
                self.persiste.insere_sitemap(conteudo=conteudo.__dict__)


class PersistenceSiteMap:

    client = None
    db = None
    def __init__(self, connection_string=None, db=None):
        self.client = MongoClient(connection_string)
        self.db = self.client[db]

    def insere_sitemap(self, collection="sitemap", conteudo=None):
        print conteudo
        self.db['collection'].insert_one(conteudo).inserted_id

x = SitemapReader({"Extra":"http://buscando.extra.com.br/sitemap.xml"})
x.run()
