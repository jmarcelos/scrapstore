from ConfigParser import SafeConfigParser

GLOBAL_CONFIG = SafeConfigParser()
#rodando o sitemap na mao
GLOBAL_CONFIG.read("scrapper/config.ini")
#rodando o sitemap pelo make
GLOBAL_CONFIG.read("config.ini")
