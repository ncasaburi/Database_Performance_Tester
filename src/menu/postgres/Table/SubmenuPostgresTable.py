from consolemenu import *
from consolemenu.items import *
from src.menu.postgres.Table.SubmenuPostgresTableCreate import SubmenuPostgresTableCreate
from src.menu.postgres.Table.SubmenuPostgresTableDrop import SubmenuPostgresTableDrop
from src.logic.status import status
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn

class SubmenuPostgresTable():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTable class"""
        
        #submenu definition
        self.submenu_postgres_table = ConsoleMenu("PostgreSQL Table Operations", status)
        
        #submenu items
        postgres_table_create = SubmenuItem("Create a table", SubmenuPostgresTableCreate().get(), self.submenu_postgres_table)
        postgres_table_drop = SubmenuItem("Drop a table", SubmenuPostgresTableDrop().get(), self.submenu_postgres_table)
        postgres_table_list = FunctionItem("List available tables", postgres_table_list_fn)

        #submenu appends
        self.submenu_postgres_table.append_item(postgres_table_create)
        self.submenu_postgres_table.append_item(postgres_table_drop)
        self.submenu_postgres_table.append_item(postgres_table_list)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table