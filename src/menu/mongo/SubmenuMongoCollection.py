from consolemenu import *
from consolemenu.items import *
from src.menu.mongo.SubmenuMongoCollectionCreate import SubmenuMongoCollectionCreate
from src.menu.mongo.SubmenuMongoCollectionDrop import SubmenuMongoCollectionDrop
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.menu.status import status
import os


class SubmenuMongoCollection():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTable class"""
        
        #submenu definition
        self.submenu_mongo_collection = ConsoleMenu("MongoDB Collection Operations", status)
        
        #submenu items
        mongo_collection_create = SubmenuItem("Create a collection", SubmenuMongoCollectionCreate().get(), self.submenu_mongo_collection)
        mongo_collection_drop = SubmenuItem("Drop a collection", SubmenuMongoCollectionDrop().get(), self.submenu_mongo_collection)
        mongo_collection_list = FunctionItem("List available collections", self.mongo_collection_list_fn)

        #submenu appends
        self.submenu_mongo_collection.append_item(mongo_collection_create)
        self.submenu_mongo_collection.append_item(mongo_collection_drop)
        self.submenu_mongo_collection.append_item(mongo_collection_list)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_collection
    
    def mongo_collection_list_fn(self):
        """This function lists the tables"""

        postgres = PostgreSQL()
        print("Please enter the schema name: (if you don't know it, just press enter)")
        schema_name = input()
        if schema_name == "":
            schema_name = "'public'"
        table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = "+schema_name+" AND table_catalog = '"+postgres.status()+"';", expected_result=True)
        os.system('clear')
        if table_list == None:
            print("No tables found\n")
            print("Press enter to continue")
            input()
            return
        else:
            print("Tables:\n")
            for table in table_list:
                print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
                print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
                print("")
            print("Press enter to continue...")
            input()
            return