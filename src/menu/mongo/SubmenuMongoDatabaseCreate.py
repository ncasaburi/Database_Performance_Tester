from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger

class SubmenuMongoDatabaseCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseCreate class"""
        
        #submenu definition
        self.submenu_mongo_database_create = ConsoleMenu("MongoDB Database Creation", status)
        
        #submenu items
        mongo_database_create_default = FunctionItem("Create default database", self.mongo_database_create_fn, args=["default"]) 
        mongo_database_create_custom = FunctionItem("Create a custom database", self.mongo_database_create_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_create.append_item(mongo_database_create_default)
        self.submenu_mongo_database_create.append_item(mongo_database_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_create
    
    def mongo_database_create_fn(self, type:str):
        """This function allows the user to create a MongoDB database"""

        try:
            if type == "default":
                MongoDB().connect(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
            else:
                print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
                mongo_connection_string = input()
                print("Enter the database name:")
                db_name = input()
                MongoDB().create(mongo_connection_string,db_name)
        except:
            SingleLogger().logger.exception("Error while creating a MongoDB database", exc_info=True)