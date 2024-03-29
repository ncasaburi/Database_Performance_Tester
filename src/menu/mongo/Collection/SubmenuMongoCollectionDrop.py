from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.collection.mongo_collection_drop import mongo_collection_drop_fn

class SubmenuMongoCollectionDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoCollectionDrop class"""
        
        #submenu definition
        self.submenu_mongo_collection_drop = ConsoleMenu("MongoDB Collection Drop", status)
        
        #submenu items
        mongo_collection_drop_default = FunctionItem("Drop default collections", mongo_collection_drop_fn, args=["default"]) 
        mongo_collection_drop_custom = FunctionItem("Drop a custom collection", mongo_collection_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_collection_drop.append_item(mongo_collection_drop_default)
        self.submenu_mongo_collection_drop.append_item(mongo_collection_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection_drop