from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.document.mongo_document_update import mongo_document_update_fn

class SubmenuMongoDocumentUpdate():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDocumentUpdate class"""
        
        #submenu definition
        self.submenu_mongo_document_update = ConsoleMenu("MongoDB Document Updates", status)
        
        #submenu items
        mongo_document_update_default = FunctionItem("Update default rows", mongo_document_update_fn, args=["default"]) 
        mongo_document_update_custom = FunctionItem("Update custom rows", mongo_document_update_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_document_update.append_item(mongo_document_update_default)
        self.submenu_mongo_document_update.append_item(mongo_document_update_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document_update