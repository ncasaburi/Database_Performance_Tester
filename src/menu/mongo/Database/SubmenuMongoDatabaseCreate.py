from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.database.mongo_database_create import mongo_database_create_fn

class SubmenuMongoDatabaseCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseCreate class"""
        
        #submenu definition
        self.submenu_mongo_database_create = ConsoleMenu("MongoDB Database Creation", status)
        
        #submenu items
        mongo_database_create_default = FunctionItem("Create default database", mongo_database_create_fn, args=["default"]) 
        mongo_database_create_custom = FunctionItem("Create a custom database", mongo_database_create_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_create.append_item(mongo_database_create_default)
        self.submenu_mongo_database_create.append_item(mongo_database_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_create