from pymongo import MongoClient
from datetime import datetime
from config import GLOBAL_CONFIG

class MongoCollection(object):
    connection_string = GLOBAL_CONFIG.get('Mongo', 'conexao')
    database_name = GLOBAL_CONFIG.get('Mongo', 'database')
    client = MongoClient(connection_string)
    db = client[database_name]
    HOMELIST_COLLETION = "HOMELIST_COLLETION"
    PRODUCTLIST_COLLETION = "PRODUCTLIST_COLLETION"

    def to_dict(self):
        return self.__dict__

    def save(self, collecion_name):
        return self.db[collection_name].insert_one(self.to_dict()).inserted_id

    def save_in_bulk(self, collecion_name, list_content_dict):
        return self.db[collecion_name].insert_many(list_content_dict).inserted_ids

    def read_home_page_list(self, collection_name, parameters):
        return self.db[collection_name].find()
