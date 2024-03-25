from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status

class SubmenuPostgresDatabaseConnect():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseConnect class"""
        
        #submenu definition
        self.submenu_postgres_database_connect = ConsoleMenu("PostgreSQL Database Connections", status)
        
        #submenu items
        postgres_database_connect_default = FunctionItem("Connect to default database", self.postgres_database_connect_fn, args=["default"]) 
        postgres_database_connect_custom = FunctionItem("Connect to a custom database", self.postgres_database_connect_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_connect.append_item(postgres_database_connect_default)
        self.submenu_postgres_database_connect.append_item(postgres_database_connect_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_connect
    
    def postgres_database_connect_fn(self, type:str):
        """This function allows the user to connect to a PostgreSQL database"""

        postgres = PostgreSQL()
        if type == "default":
            postgres.connect(Config().default_dbs["default_postgres_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("Enter the connection string: (example: postgresql://user:password@localhost:32768/)")
            postgre_connection_string = input()
            print("Enter the database name:")
            db_name = input()
            postgres.connect(postgre_connection_string,db_name)