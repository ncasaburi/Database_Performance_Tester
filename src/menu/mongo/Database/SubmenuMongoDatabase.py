from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.Database.SubmenuMongoDatabaseConnect import SubmenuMongoDatabaseConnect
from src.menu.mongo.Database.SubmenuMongoDatabaseCreate import SubmenuMongoDatabaseCreate
from src.menu.mongo.Database.SubmenuMongoDatabaseDrop import SubmenuMongoDatabaseDrop
from src.logic.mongo.database.mongo_database_list import mongo_database_list_fn
from src.logic.status import status

class SubmenuMongoDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDatabase class"""
        
        #submenu definition
        self.submenu_mongo_database = ConsoleMenu("Mongo Database Operations", status)
        
        #submenu items
        mongo_database_create = SubmenuItem("Create Database", SubmenuMongoDatabaseCreate().get(), self.submenu_mongo_database)
        mongo_database_connect = SubmenuItem("Connect to Database", SubmenuMongoDatabaseConnect().get(), self.submenu_mongo_database)
        mongo_database_list = FunctionItem("List available database", mongo_database_list_fn)
        mongo_database_drop = SubmenuItem("Drop Database", SubmenuMongoDatabaseDrop().get(), self.submenu_mongo_database)

        #submenu appends
        self.submenu_mongo_database.append_item(mongo_database_create)
        self.submenu_mongo_database.append_item(mongo_database_connect)
        self.submenu_mongo_database.append_item(mongo_database_list)
        self.submenu_mongo_database.append_item(mongo_database_drop)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_database