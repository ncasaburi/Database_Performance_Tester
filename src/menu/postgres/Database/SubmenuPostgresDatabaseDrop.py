from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.database.postgres_database_drop import postgres_database_drop_fn

class SubmenuPostgresDatabaseDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseDrop class"""
        
        #submenu definition
        self.submenu_postgres_database_drop = ConsoleMenu("PostgreSQL Database Drop", status)
        
        #submenu items
        postgres_database_drop_default = FunctionItem("Drop default database", postgres_database_drop_fn, args=["default"]) 
        postgres_database_drop_current = FunctionItem("Drop current database", postgres_database_drop_fn, args=["current"]) 
        postgres_database_drop_custom = FunctionItem("Drop a custom database", postgres_database_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_default)
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_current)
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_drop