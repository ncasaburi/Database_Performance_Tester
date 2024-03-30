from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.index.postgres_index_create import postgres_index_create_fn

class SubmenuPostgresIndex():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresIndexCreate class"""
        
        #submenu definition
        self.submenu_postgres_index_create = ConsoleMenu("PostgreSQL Index Creates", status)
        
        #submenu items
        postgres_index_create_default = FunctionItem("Create default indexs", postgres_index_create_fn, args=["default"]) 
        postgres_index_create_custom = FunctionItem("Create custom indexs", postgres_index_create_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_index_create.append_item(postgres_index_create_default)
        self.submenu_postgres_index_create.append_item(postgres_index_create_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_index_create