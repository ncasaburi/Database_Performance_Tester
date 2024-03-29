from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.database.postgres_database_connect import postgres_database_connect_fn

class SubmenuPostgresDatabaseConnect():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseConnect class"""
        
        #submenu definition
        self.submenu_postgres_database_connect = ConsoleMenu("PostgreSQL Database Connections", status)
        
        #submenu items
        postgres_database_connect_default = FunctionItem("Connect to default database", postgres_database_connect_fn, args=["default"]) 
        postgres_database_connect_custom = FunctionItem("Connect to a custom database", postgres_database_connect_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_connect.append_item(postgres_database_connect_default)
        self.submenu_postgres_database_connect.append_item(postgres_database_connect_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_connect