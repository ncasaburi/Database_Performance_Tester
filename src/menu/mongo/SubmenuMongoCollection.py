from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoCollectionCreate import SubmenuMongoCollectionCreate
from src.menu.mongo.SubmenuMongoCollectionDrop import SubmenuMongoCollectionDrop
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
import os


class SubmenuMongoCollection():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoCollection class"""
        
        #submenu definition
        self.submenu_mongo_collection = ConsoleMenu("MongoDB Collection Operations", status)
        
        #submenu items
        mongo_collection_create = SubmenuItem("Create a collection", SubmenuMongoCollectionCreate().get(), self.submenu_mongo_collection)
        mongo_collection_drop = SubmenuItem("Drop a collection", SubmenuMongoCollectionDrop().get(), self.submenu_mongo_collection)
        mongo_collection_list = FunctionItem("List available collections", self.mongo_collection_list_fn)

        #submenu appends
        self.submenu_mongo_collection.append_item(mongo_collection_create)
        self.submenu_mongo_collection.append_item(mongo_collection_drop)
        self.submenu_mongo_collection.append_item(mongo_collection_list)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection
    
    def mongo_collection_list_fn(self):
        """This function lists the collections"""

        collections = MongoDB().db.list_collection_names()
        print("Collections:\n")
        if collections == None:
            print("No Collections found")
        else:
            for collection in collections:
                print(collection+"\n")
        input()
        return