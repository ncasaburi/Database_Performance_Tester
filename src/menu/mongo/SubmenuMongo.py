from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.Database.SubmenuMongoDatabase import SubmenuMongoDatabase
from src.menu.mongo.Collection.SubmenuMongoCollection import SubmenuMongoCollection
from src.menu.mongo.Document.SubmenuMongoDocument import SubmenuMongoDocument
from src.menu.mongo.Index.SubmenuMongoIndex import SubmenuMongoIndex
from src.logic.status import status

class SubmenuMongo():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongo class"""

        #submenu definition
        self.submenu_mongo = ConsoleMenu("MongoDB", status)

        #submenu items
        mongo_database = SubmenuItem("Database", SubmenuMongoDatabase().get(), menu=self.submenu_mongo)
        mongo_collections = SubmenuItem("Collections", SubmenuMongoCollection().get(), menu=self.submenu_mongo)
        mongo_documents = SubmenuItem("Documents", SubmenuMongoDocument().get(), menu=self.submenu_mongo)
        mongo_indexes = SubmenuItem("Indexes", SubmenuMongoIndex().get(), menu=self.submenu_mongo)
        mongo_files = SubmenuItem("Files", self.submenu_mongo, menu=self.submenu_mongo)

        #submenu appends
        self.submenu_mongo.append_item(mongo_database)
        self.submenu_mongo.append_item(mongo_collections)
        self.submenu_mongo.append_item(mongo_documents)
        self.submenu_mongo.append_item(mongo_indexes)
        self.submenu_mongo.append_item(mongo_files)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo
         