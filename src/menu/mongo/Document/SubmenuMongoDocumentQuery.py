from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.mongo.document.mongo_document_query_find import mongo_document_query_find_fn
from src.logic.mongo.document.mongo_document_query_aggregation import mongo_document_query_aggregation_fn

class SubmenuMongoDocumentQuery():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDocumentQuery class"""
        
        #submenu definition
        self.submenu_mongo_document_query = ConsoleMenu("MongoDB Document Query", status)
        
        #submenu items
        mongo_document_query_find_default = FunctionItem("Default find", mongo_document_query_find_fn, args=["default"]) 
        mongo_document_query_find_custom = FunctionItem("Custom find", mongo_document_query_find_fn, args=["custom"])
        mongo_document_query_aggregation_default = FunctionItem("Default aggregation", mongo_document_query_aggregation_fn, args=["default"]) 
        mongo_document_query_aggregation_custom = FunctionItem("Custom aggregation", mongo_document_query_aggregation_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_document_query.append_item(mongo_document_query_find_default)
        self.submenu_mongo_document_query.append_item(mongo_document_query_find_custom)
        self.submenu_mongo_document_query.append_item(mongo_document_query_aggregation_default)
        self.submenu_mongo_document_query.append_item(mongo_document_query_aggregation_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document_query