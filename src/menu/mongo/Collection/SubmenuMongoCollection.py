from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.Collection.SubmenuMongoCollectionCreate import SubmenuMongoCollectionCreate
from src.menu.mongo.Collection.SubmenuMongoCollectionDrop import SubmenuMongoCollectionDrop
from src.logic.status import status
from src.logic.mongo.collection.mongo_collection_list import mongo_collection_list_fn


class SubmenuMongoCollection():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoCollection class"""
        
        #submenu definition
        self.submenu_mongo_collection = ConsoleMenu("MongoDB Collection Operations", status)
        
        #submenu items
        mongo_collection_create = SubmenuItem("Create a collection", SubmenuMongoCollectionCreate().get(), self.submenu_mongo_collection)
        mongo_collection_drop = SubmenuItem("Drop a collection", SubmenuMongoCollectionDrop().get(), self.submenu_mongo_collection)
        mongo_collection_list = FunctionItem("List available collections", mongo_collection_list_fn)

        #submenu appends
        self.submenu_mongo_collection.append_item(mongo_collection_create)
        self.submenu_mongo_collection.append_item(mongo_collection_drop)
        self.submenu_mongo_collection.append_item(mongo_collection_list)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection