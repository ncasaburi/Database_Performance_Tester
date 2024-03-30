from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.index.mongo_index_create import mongo_index_create_fn

class SubmenuMongoIndex():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoIndexCreate class"""
        
        #submenu definition
        self.submenu_mongo_index_create = ConsoleMenu("MongoDB Index Creates", status)
        
        #submenu items
        mongo_index_create_default = FunctionItem("Create default indexes", mongo_index_create_fn, args=["default"]) 
        mongo_index_create_custom = FunctionItem("Create custom indexes", mongo_index_create_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_index_create.append_item(mongo_index_create_default)
        self.submenu_mongo_index_create.append_item(mongo_index_create_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_index_create