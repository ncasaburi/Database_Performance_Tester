from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.Document.SubmenuMongoDocumentInsert import SubmenuMongoDocumentInsert
from src.menu.mongo.Document.SubmenuMongoDocumentUpdate import SubmenuMongoDocumentUpdate
from src.menu.mongo.Document.SubmenuMongoDocumentDelete import SubmenuMongoDocumentDelete
from src.logic.status import status

class SubmenuMongoDocument():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRow class"""
        
        #submenu definition
        self.submenu_mongo_document = ConsoleMenu("MongoDB Document Operations", status)
        
        #submenu items
        mongo_document_insert = SubmenuItem("Insert documents", SubmenuMongoDocumentInsert().get(), self.submenu_mongo_document)
        mongo_document_update = SubmenuItem("Update documents", SubmenuMongoDocumentUpdate().get(), self.submenu_mongo_document)
        mongo_document_delete = SubmenuItem("Delete documents", SubmenuMongoDocumentDelete().get(), self.submenu_mongo_document)

        #submenu appends
        self.submenu_mongo_document.append_item(mongo_document_insert)
        self.submenu_mongo_document.append_item(mongo_document_update)
        self.submenu_mongo_document.append_item(mongo_document_delete)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document