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
        postgres_row_select_default1 = FunctionItem("Default select (query 1)", postgres_row_select_fn, args=["default1"])
        postgres_row_select_default2 = FunctionItem("Default select (query 2)", postgres_row_select_fn, args=["default2"])
        postgres_row_select_default3 = FunctionItem("Default select (query 3)", postgres_row_select_fn, args=["default3"])  
        postgres_row_select_custom = FunctionItem("Custom select", postgres_row_select_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_select.append_item(postgres_row_select_default1)
        self.submenu_postgres_row_select.append_item(postgres_row_select_default2)
        self.submenu_postgres_row_select.append_item(postgres_row_select_default3)
        self.submenu_postgres_row_select.append_item(postgres_row_select_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_select