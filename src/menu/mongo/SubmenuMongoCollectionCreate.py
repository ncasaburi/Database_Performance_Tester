from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB   
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper

class SubmenuMongoCollectionCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoCollectionCreate class"""
        
        #submenu definition
        self.submenu_mongo_collection_create = ConsoleMenu("Mongo Collection Creation", status )
        
        #submenu items
        mongo_collection_create_default = FunctionItem("Create default collections", self.mongo_collection_create_fn, args=["default"]) 
        mongo_collection_create_custom = FunctionItem("Create a custom collection", self.mongo_collection_create_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_collection_create.append_item(mongo_collection_create_default)
        self.submenu_mongo_collection_create.append_item(mongo_collection_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection_create
    
    def mongo_collection_create_fn(self, type:str):
        """This function allows the user to create a table"""
        try:
            mongo = MongoDB()
            mongo.connect(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
            if type == "default":
                SingleLogger().logger.info("Creating default collections...")                
                if not mongo.exist_collection('patients'):
                    mongo.create_collection('patients')

                if not mongo.exist_collection('doctors'):    
                    mongo.create_collection('doctors')
                 
                if not mongo.exist_collection('doctor_medical_records'):
                    mongo.create_collection('doctor_medical_records')

                if not mongo.exist_collection('medical_records'):
                    mongo.create_collection('medical_records')


            else:
                SingleLogger().logger.info("Creating custom collection...")                
                print("Enter the name collection to create\n");
                collectionname = input()
                collectionname = collectionname.lower()
                if not mongo.exist_collection(collectionname):
                    mongo.create_collection(collectionname)

        except:
            SingleLogger().logger.exception("Error while creating to a MongoDB collections", exc_info=True)
