from pymongo import MongoClient
import pymongo
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
        return {}

    def save(self, collection_name):
        collection_name = self.__collection_name(collection_name)
        id = self._id
        if id:
            self.db[collection_name].update({'_id':id}, self.to_dict(), True)
        self.db[collection_name].insert_one(self.to_dict()).inserted_id

    #def save_or_update(self, filter):
    #    self.db[self.__class__.__name__].update_one(filter,{"$set": self.to_dict()},True)

    def save_in_bulk(self, collection_name, content_list):
        if content_list:
            collection_name = self.__collection_name(collection_name)
            print 'Salvando %s' % collection_name
            return self.db[collection_name].insert_many([c.to_dict() for c in content_list]).inserted_ids

    def read_content(self, collection_name, parameters=None, sorting=None):
        content_list = []
        collection_name = self.__collection_name(collection_name)
        print "query: %s %s" % (collection_name, sorting)
        if sorting:
            cursor = self.db[collection_name].find(parameters).sort(sorting, pymongo.ASCENDING)
        else:
            cursor = self.db[collection_name].find(parameters)

        for item in cursor:
            content_list.append(item)
        return content_list

    def __collection_name(self, collection_name):
        if not collection_name:
            collection_name = self.__class__.__name__
        return  collection_name
