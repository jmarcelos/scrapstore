from pymongo import MongoClient
from datetime import datetime
from config import GLOBAL_CONFIG

class MongoCollection(object):
    connection_string = GLOBAL_CONFIG.get('Mongo', 'conexao')
    database_name = GLOBAL_CONFIG.get('Mongo', 'database')    
    client = MongoClient(connection_string)
    db = client[database_name]

    def to_dict(self):
        return self.__dict__

    def save(self):
        self.db[self.__class__.__name__].insert_one(self.to_dict()).inserted_id

    def save_or_update(self, filter):
        self.db[self.__class__.__name__].update_one(filter,{"$set": self.to_dict()},True)
