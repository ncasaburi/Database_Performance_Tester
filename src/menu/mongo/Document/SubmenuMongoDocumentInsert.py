from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.document.mongo_document_insert import mongo_document_insert_fn
from src.logic.mongo.document.mongo_document_batch_insert import mongo_document_batch_insert_fn

class SubmenuMongoDocumentInsert():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDocumentInsert class"""
        
        #submenu definition
        self.submenu_mongo_document_insert = ConsoleMenu("MongoDB Document Inserts", status)
        
        #submenu items
        mongo_document_insert_default = FunctionItem("Insert default documents", mongo_document_insert_fn, args=["default"])
        mongo_document_batch_insert_default = FunctionItem("Batch default document insert", mongo_document_batch_insert_fn)  
        mongo_document_insert_custom = FunctionItem("Insert custom documents", mongo_document_insert_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_document_insert.append_item(mongo_document_insert_default)
        self.submenu_mongo_document_insert.append_item(mongo_document_batch_insert_default)
        self.submenu_mongo_document_insert.append_item(mongo_document_insert_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document_insert