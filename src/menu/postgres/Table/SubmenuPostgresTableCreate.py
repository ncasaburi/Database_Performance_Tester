from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.table.postgres_table_create import postgres_table_create_fn

class SubmenuPostgresTableCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTableCreate class"""
        
        #submenu definition
        self.submenu_postgres_table_create = ConsoleMenu("PostgreSQL Table Creation", status )
        
        #submenu items
        postgres_table_create_default = FunctionItem("Create default tables", postgres_table_create_fn, args=["default"]) 
        postgres_table_create_custom = FunctionItem("Create a custom table", postgres_table_create_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_table_create.append_item(postgres_table_create_default)
        self.submenu_postgres_table_create.append_item(postgres_table_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table_create