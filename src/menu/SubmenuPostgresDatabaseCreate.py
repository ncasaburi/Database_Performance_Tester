from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status

class SubmenuPostgresDatabaseCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseCreate class"""
        
        #submenu definition
        self.submenu_postgres_database_create = ConsoleMenu("PostgreSQL Database Creation", status)
        
        #submenu items
        postgres_database_create_default = FunctionItem("Create default database", self.postgres_database_create_fn, args=["default"]) 
        postgres_database_create_custom = FunctionItem("Create a custom database", self.postgres_database_create_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_create.append_item(postgres_database_create_default)
        self.submenu_postgres_database_create.append_item(postgres_database_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_create
    
    def postgres_database_create_fn(self, type:str):
        """This function allows the user to create a PostgreSQL database"""

        postgres = PostgreSQL()
        if type == "default":
            postgres.create(Config().default_dbs["default_postgres_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("Enter the connection string: (example: postgresql://user:password@localhost:32768/)")
            postgre_connection_string = input()
            print("Enter the database name:")
            db_name = input()
            postgres.create(postgre_connection_string,db_name)