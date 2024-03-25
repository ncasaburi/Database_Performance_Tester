from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
from src.config.Zipper import Zipper

class SubmenuMongoCollectionDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTableDrop class"""
        
        #submenu definition
        self.submenu_mongo_collection_drop = ConsoleMenu("MongoDB Collection Drop", status)
        
        #submenu items
        mongo_collection_drop_default = FunctionItem("Drop default collections", self.mongo_collection_drop_fn, args=["default"]) 
        mongo_collection_drop_custom = FunctionItem("Drop a custom collection", self.mongo_collection_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_collection_drop.append_item(mongo_collection_drop_default)
        self.submenu_mongo_collection_drop.append_item(mongo_collection_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection_drop
    
    def mongo_collection_drop_fn(self, type:str):
        """This function allows the user to drop a collection"""

        mongo = MongoDB()
        mongo.connect(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
        if type == "default":
            mongo.drop_collection('doctor_medical_records')
            mongo.drop_collection('patients')
            mongo.drop_collection('doctors')
            mongo.drop_collection('medical_records')
        else:
            print("Enter your name collection to drop:\n")
            collectionname = input()            
            mongo.drop_collection(collectionname)
