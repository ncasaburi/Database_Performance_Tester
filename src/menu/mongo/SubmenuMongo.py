from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoDatabase import SubmenuMongoDatabase
#from src.menu.mongo.SubmenuMongoTable import SubmenuMongoTable
#from src.menu.mongo.SubmenuMongoRow import SubmenuMongoRow
from src.menu.status import status

class SubmenuMongo():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongo class"""

        #submenu definition
        self.submenu_mongo = ConsoleMenu("MongoDB", status)

        #submenu items
        mongo_database = SubmenuItem("Database", SubmenuMongoDatabase().get(), menu=self.submenu_mongo)
        mongo_tables = SubmenuItem("Tables", SubmenuMongoDatabase().get(), menu=self.submenu_mongo)
        mongo_rows = SubmenuItem("Rows", SubmenuMongoDatabase().get(), menu=self.submenu_mongo)
        mongo_files = SubmenuItem("Files", self.submenu_mongo, menu=self.submenu_mongo)

        #submenu appends
        self.submenu_mongo.append_item(mongo_database)
        self.submenu_mongo.append_item(mongo_tables)
        self.submenu_mongo.append_item(mongo_rows)
        self.submenu_mongo.append_item(mongo_files)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo
         