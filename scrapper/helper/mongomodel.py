from pymongo import MongoClient
from datetime import datetime
from config import GLOBAL_CONFIG

class MongoCollection(object):
    connection_string = GLOBAL_CONFIG.get('Mongo', 'conexao')
    database_name = GLOBAL_CONFIG.get('Mongo', 'database')
    client = MongoClient(connection_string)
    db = client[database_name]

    HOMELIST_COLLETION = "HOMELIST_COLLETION"
    AMERICANAS_PRODUCTLIST_COLLETION = "AMERICANAS_PRODUCTLIST_COLLETION"
    EXTRA_PRODUCTLIST_COLLETION = "EXTRA_PRODUCTLIST_COLLETION"
    SUBMARINO_PRODUCTLIST_COLLETION = "SUBMARINO_PRODUCTLIST_COLLETION"
    NETSHOES_PRODUCTLIST_COLLETION = "NETSHOES_PRODUCTLIST_COLLETION"

    def to_dict(self):
        return self.__dict__

    def save(self):
        self.db[self.__class__.__name__].insert_one(self.to_dict()).inserted_id

    def save_or_update(self, filter):
        self.db[self.__class__.__name__].update_one(filter,{"$set": self.to_dict()},True)

    #def save_in_bulk(self, content_list):
        #if content_list:
            #return self.db[self.__class__.__name__].insert_many([c.to_dict() for c in content_list]).inserted_ids

    def save_in_bulk(self, collection_name, content_list):
        if content_list:
            print 'Salvando %s' % collection_name
            return self.db[collection_name].insert_many([c.to_dict() for c in content_list]).inserted_ids


    def read_content(self, parameters=None):
        content_list = []
        cursor = self.db[self.__class__.__name__].find(parameters)
        for item in cursor:
            content_list.append(item)
        return content_list

    def read_content(self, collection_name, parameters=None):
        content_list = []
        cursor = self.db[collection_name].find(parameters)

        for item in cursor:
            content_list.append(item)
        return content_list
