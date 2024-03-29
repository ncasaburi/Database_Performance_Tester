from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.row.postgres_row_select import postgres_row_select_fn

class SubmenuPostgresRowSelect():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowSelect class"""
        
        #submenu definition
        self.submenu_postgres_row_select = ConsoleMenu("PostgreSQL Row Select", status)
        
        #submenu items
        postgres_row_select_default = FunctionItem("Insert default rows", postgres_row_select_fn, args=["default"]) 
        postgres_row_select_custom = FunctionItem("Insert custom rows", postgres_row_select_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_select.append_item(postgres_row_select_default)
        self.submenu_postgres_row_select.append_item(postgres_row_select_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_select