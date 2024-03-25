from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoDatabaseConnect import SubmenuMongoDatabaseConnect
from src.menu.mongo.SubmenuMongoDatabaseCreate import SubmenuMongoDatabaseCreate
from src.menu.mongo.SubmenuMongoDatabaseDrop import SubmenuMongoDatabaseDrop
from src.config.Config import Config
from src.menu.status import status
from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

class SubmenuMongoDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabase class"""
        
        #submenu definition
        self.submenu_mongo_database = ConsoleMenu("Mongo Database Operations", status)
        
        #submenu items
        mongo_database_create = SubmenuItem("Create Database", SubmenuMongoDatabaseCreate().get(), self.submenu_mongo_database)
        mongo_database_connect = SubmenuItem("Connect to Database", SubmenuMongoDatabaseConnect().get(), self.submenu_mongo_database)
        mongo_database_list = FunctionItem("List available database", self.mongo_database_list_fn)
        mongo_database_drop = SubmenuItem("Drop Database", SubmenuMongoDatabaseDrop().get(), self.submenu_mongo_database)

        #submenu appends
        self.submenu_mongo_database.append_item(mongo_database_create)
        self.submenu_mongo_database.append_item(mongo_database_connect)
        self.submenu_mongo_database.append_item(mongo_database_list)
        self.submenu_mongo_database.append_item(mongo_database_drop)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database
    
    def mongo_database_list_fn(self) -> None:
        """This function allows the user to see all available MongoDB databases"""

        try:
            mongo = MongoDB()
            mongo.connect(Config().default_dbs["default_mongo_connection_string"],"")
            list_databases = mongo.conn.list_database_names()
            print("Databases:\n")
            for db in list_databases:
                print(" - "+db)
                print("\nPress enter to continue...")
                input()

            # db_list = mongo.run_query("SELECT datname FROM pg_database","Listing all available Mongo databases", True)
            # if db_list == None:
            #     print("No databases found\n")
            #     print("Press enter to continue")
            #     input()
            #     return
            # else:
            #     print("Databases:\n")
            #     for db in db_list:
            #         print(" - "+db[0])
            #     print("\nPress enter to continue...")
            #     input()
        except:
            SingleLogger().logger.exception("Error while listing available MongoDB databases", exc_info=True)

