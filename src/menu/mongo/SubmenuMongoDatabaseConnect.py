from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger

class SubmenuMongoDatabaseConnect():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabaseConnect class"""
        
        #submenu definition
        self.submenu_mongo_database_connect = ConsoleMenu("MongoDB Database Connections", status)
        
        #submenu items
        mongo_database_connect_default = FunctionItem("Connect to default database", self.mongo_database_connect_fn, args=["default"]) 
        mongo_database_connect_custom = FunctionItem("Connect to a custom database", self.mongo_database_connect_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_database_connect.append_item(mongo_database_connect_default)
        self.submenu_mongo_database_connect.append_item(mongo_database_connect_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database_connect
    
    def mongo_database_connect_fn(self, type:str):
        """This function allows the user to connect to a MongoDB database"""

        try:
            mongo = MongoDB()
            if type == "default":
                pass
            else:
                print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
                mongo_connection_string = input()
                print("Enter the database name:")
                db_name = input()
                mongo.connect(mongo_connection_string,db_name)
        except:
            SingleLogger().logger.exception("Error while connecting to a MongoDB database", exc_info=True)