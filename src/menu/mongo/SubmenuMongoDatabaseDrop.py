from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger

class SubmenuMongoDatabaseDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseDrop class"""
        
        #submenu definition
        self.submenu_mongo_database_drop = ConsoleMenu("MongoDB Database Drop", status)
        
        #submenu items
        mongo_database_drop_default = FunctionItem("Drop default database", self.mongo_database_drop_fn, args=["default"]) 
        mongo_database_drop_current = FunctionItem("Drop current database", self.mongo_database_drop_fn, args=["current"]) 
        mongo_database_drop_custom = FunctionItem("Drop a custom database", self.mongo_database_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_default)
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_current)
        self.submenu_mongo_database_drop.append_item(mongo_database_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_drop
    
    def mongo_database_drop_fn(self, type:str):
        """This function allows the user to drop a MongoDB database"""

        try:
            if type == "default":
                MongoDB().drop(Config().default_dbs["default_database_name"])
            elif type == "current":
                MongoDB().drop(MongoDB().status())
            else:
                print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
                print("Enter the database name:")
                db_name = input()
                MongoDB().drop(db_name)
        except:
            SingleLogger().logger.exception("Error while dropping a MongoDB database", exc_info=True)