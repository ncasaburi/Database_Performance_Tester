from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.database.mongo_database_connect import mongo_database_connect_fn

class SubmenuMongoDatabaseConnect():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseConnect class"""
        
        #submenu definition
        self.submenu_mongo_database_connect = ConsoleMenu("MongoDB Database Connections", status)
        
        #submenu items
        mongo_database_connect_default = FunctionItem("Connect to default database", mongo_database_connect_fn, args=["default"]) 
        mongo_database_connect_custom = FunctionItem("Connect to a custom database", mongo_database_connect_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_connect.append_item(mongo_database_connect_default)
        self.submenu_mongo_database_connect.append_item(mongo_database_connect_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_connect