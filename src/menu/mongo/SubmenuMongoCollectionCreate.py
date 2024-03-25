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
            db = mongo.conn(Config().default_dbs["default_database_name"])
            if type == "default":
                db.create_collection('patients')
                db.create_collection('doctors')
                db.create_collection('doctor_medical_records')
                db.create_collection('medical_records')
                SingleLogger().logger.info("Creating default collections...")
            else:
                print("Enter the query create collection \nExample: db.createCollection(collectionname)\n");
                collectionname = input()
                collectionname = collectionname.lower()
                if collectionname.startswith("db.createCollection"):
                    db.create_collection(collectionname)
                else:
                    print("\nThe query must begin with db.createCollection")
                    print("\nPress enter to go back to the menu")
                    input()            
        except:
            SingleLogger().logger.exception("Error while creating to a MongoDB collections", exc_info=True)

        # postgres = PostgreSQL()
        # if type == "default":
        #     content_sql = Zipper().unzip_content(Config().default_data["default_postgres_creates"]+"Tables.zip","sql")
        #     postgres.run_query(content_sql, "Creating default tables...")
        # else:
        #     print("Enter the table creation query: \nExample: CREATE TABLE tablename ( columnname1 SERIAL PRIMARY KEY, columenname2 VARCHAR(50), columnname3 VARCHAR(50) )\n");
        #     query = input()
        #     query = query.lower()
        #     if query.startswith("create table"):
        #         postgres.run_query(query, "Creating a new custom table...")
        #     else:
        #         print("\nThe query must begin with CREATE TABLE")
        #         print("\nPress enter to go back to the menu")
        #         input()