from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoDatabase import SubmenuMongoDatabase
from src.menu.mongo.SubmenuMongoCollection import SubmenuMongoCollection
from src.menu.mongo.SubmenuMongoDocument import SubmenuMongoDocument
from src.menu.status import status

class SubmenuMongo():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongo class"""

        #submenu definition
        self.submenu_mongo = ConsoleMenu("MongoDB", status)

        #submenu items
        mongo_database = SubmenuItem("Database", SubmenuMongoDatabase().get(), menu=self.submenu_mongo)
        mongo_collections = SubmenuItem("Collections", SubmenuMongoCollection().get(), menu=self.submenu_mongo)
        mongo_documents = SubmenuItem("Documents", SubmenuMongoDocument().get(), menu=self.submenu_mongo)
        mongo_files = SubmenuItem("Files", self.submenu_mongo, menu=self.submenu_mongo)

        #submenu appends
        self.submenu_mongo.append_item(mongo_database)
        self.submenu_mongo.append_item(mongo_collections)
        self.submenu_mongo.append_item(mongo_documents)
        self.submenu_mongo.append_item(mongo_files)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo
         