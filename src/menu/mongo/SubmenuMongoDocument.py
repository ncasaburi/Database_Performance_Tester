from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoDocumentInsert import SubmenuMongoDocumentInsert
from src.menu.mongo.SubmenuMongoDocumentUpdate import SubmenuMongoDocumentUpdate
from src.menu.mongo.SubmenuMongoDocumentDelete import SubmenuMongoDocumentDelete
from src.menu.status import status

class SubmenuMongoDocument():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRow class"""
        
        #submenu definition
        self.submenu_mongo_document = ConsoleMenu("PostgreSQL Row Operations", status)
        
        #submenu items
        mongo_document_insert = SubmenuItem("Insert rows", SubmenuMongoDocumentInsert().get(), self.submenu_mongo_document)
        mongo_document_update = SubmenuItem("Update rows", SubmenuMongoDocumentUpdate().get(), self.submenu_mongo_document)
        mongo_document_delete = SubmenuItem("Delete rows", SubmenuMongoDocumentDelete().get(), self.submenu_mongo_document)

        #submenu appends
        self.submenu_mongo_document.append_item(mongo_document_insert)
        self.submenu_mongo_document.append_item(mongo_document_update)
        self.submenu_mongo_document.append_item(mongo_document_delete)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document