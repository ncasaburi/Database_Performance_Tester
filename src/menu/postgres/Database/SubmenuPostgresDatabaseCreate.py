from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.database.postgres_database_create import postgres_database_create_fn

class SubmenuPostgresDatabaseCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseCreate class"""
        
        #submenu definition
        self.submenu_postgres_database_create = ConsoleMenu("PostgreSQL Database Creation", status)
        
        #submenu items
        postgres_database_create_default = FunctionItem("Create default database", postgres_database_create_fn, args=["default"]) 
        postgres_database_create_custom = FunctionItem("Create a custom database", postgres_database_create_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_create.append_item(postgres_database_create_default)
        self.submenu_postgres_database_create.append_item(postgres_database_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_create