from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.database.mongo_database_drop import mongo_database_drop_fn

class SubmenuMongoDatabaseDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseDrop class"""
        
        #submenu definition
        self.submenu_mongo_database_drop = ConsoleMenu("MongoDB Database Drop", status)
        
        #submenu items
        mongo_database_drop_default = FunctionItem("Drop default database", mongo_database_drop_fn, args=["default"]) 
        mongo_database_drop_current = FunctionItem("Drop current database", mongo_database_drop_fn, args=["current"]) 
        mongo_database_drop_custom = FunctionItem("Drop a custom database", mongo_database_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_default)
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_current)
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_drop