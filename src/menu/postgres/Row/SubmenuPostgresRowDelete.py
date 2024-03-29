from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.row.postgres_row_delete import postgres_row_delete_fn

class SubmenuPostgresRowDelete():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowDelete class"""
        
        #submenu definition
        self.submenu_postgres_row_delete = ConsoleMenu("PostgreSQL Row Delete", status)
        
        #submenu items
        postgres_row_delete_default = FunctionItem("Delete default rows", postgres_row_delete_fn, args=["default"])
        postgres_row_delete_custom = FunctionItem("Delete custom rows", postgres_row_delete_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_delete.append_item(postgres_row_delete_default)
        self.submenu_postgres_row_delete.append_item(postgres_row_delete_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_delete