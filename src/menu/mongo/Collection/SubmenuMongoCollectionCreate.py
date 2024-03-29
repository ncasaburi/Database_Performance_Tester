from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.collection.mongo_collection_create import mongo_collection_create_fn

class SubmenuMongoCollectionCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoCollectionCreate class"""
        
        #submenu definition
        self.submenu_mongo_collection_create = ConsoleMenu("Mongo Collection Creation", status )
        
        #submenu items
        mongo_collection_create_default = FunctionItem("Create default collections", mongo_collection_create_fn, args=["default"]) 
        mongo_collection_create_custom = FunctionItem("Create a custom collection", mongo_collection_create_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_collection_create.append_item(mongo_collection_create_default)
        self.submenu_mongo_collection_create.append_item(mongo_collection_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection_create