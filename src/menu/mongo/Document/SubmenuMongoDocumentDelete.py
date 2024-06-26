from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.document.mongo_document_delete import mongo_document_delete_fn
from src.logic.mongo.document.mongo_document_batch_delete import mongo_document_batch_delete_fn

class SubmenuMongoDocumentDelete():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDocumentDelete class"""
        
        #submenu definition
        self.submenu_mango_document_delete = ConsoleMenu("Mongo Document Delete", status)
        
        #submenu items
        mongo_document_delete_default = FunctionItem("Delete default document", mongo_document_delete_fn, args=["default"])
        mongo_document_batch_delete_default = FunctionItem("Batch default document delete", mongo_document_batch_delete_fn)
        mongo_document_delete_custom = FunctionItem("Delete custom document", mongo_document_delete_fn, args=["custom"])

        #submenu appends
        self.submenu_mango_document_delete.append_item(mongo_document_delete_default)
        self.submenu_mango_document_delete.append_item(mongo_document_batch_delete_default)
        self.submenu_mango_document_delete.append_item(mongo_document_delete_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mango_document_delete