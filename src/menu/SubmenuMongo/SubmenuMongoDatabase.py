from consolemenu import *
from consolemenu.items import *
from src.menu.SubmenuMongo.SubmenuMongoDatabaseConnect import SubmenuMongoDatabaseConnect
from src.menu.SubmenuMongo.SubmenuMongoDatabaseCreate import SubmenuMongoDatabaseCreate
from src.menu.SubmenuMongo.SubmenuMongoDatabaseDrop import SubmenuMongoDatabaseDrop
from src.menu.status import status
from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

class SubmenuMongoDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabase class"""
        
        #submenu definition
        self.submenu_mongo_database = ConsoleMenu("Mongo Database Operations", status)
        
        #submenu items
        mongo_database_create = SubmenuItem("Create database", SubmenuMongoDatabaseCreate().get(), self.submenu_mongo_database)
        mongo_database_connect = SubmenuItem("Connect to database", SubmenuMongoDatabaseConnect().get(), self.submenu_mongo_database)
        mongo_database_list = FunctionItem("List available databases", self.mongo_database_list_fn)
        mongo_database_drop = SubmenuItem("Drop database", SubmenuMongoDatabaseDrop().get(), self.submenu_mongo_database)

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

