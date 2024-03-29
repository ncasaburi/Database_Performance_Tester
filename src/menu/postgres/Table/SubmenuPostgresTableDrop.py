from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.table.postgres_table_drop import postgres_table_drop_fn

class SubmenuPostgresTableDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTableDrop class"""
        
        #submenu definition
        self.submenu_postgres_table_drop = ConsoleMenu("PostgreSQL Table Drop", status)
        
        #submenu items
        postgres_table_drop_default = FunctionItem("Drop default tables", postgres_table_drop_fn, args=["default"]) 
        postgres_table_drop_custom = FunctionItem("Drop a custom table", postgres_table_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_table_drop.append_item(postgres_table_drop_default)
        self.submenu_postgres_table_drop.append_item(postgres_table_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table_drop