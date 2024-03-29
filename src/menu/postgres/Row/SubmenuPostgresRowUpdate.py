from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.row.postgres_row_update import postgres_row_update_fn

class SubmenuPostgresRowUpdate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowUpdate class"""
        
        #submenu definition
        self.submenu_postgres_row_update = ConsoleMenu("PostgreSQL Row Updates", status)
        
        #submenu items
        postgres_row_update_default = FunctionItem("Update default rows", postgres_row_update_fn, args=["default"]) 
        postgres_row_update_custom = FunctionItem("Update custom rows", postgres_row_update_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_update.append_item(postgres_row_update_default)
        self.submenu_postgres_row_update.append_item(postgres_row_update_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_update