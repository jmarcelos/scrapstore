from mongoengine import *
from config import GLOBAL_CONFIG
connection_string = GLOBAL_CONFIG.get('Mongo', 'conexao')
connect(host=connection_string)
