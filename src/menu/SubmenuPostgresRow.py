from consolemenu import *
from consolemenu.items import *
from src.menu.SubmenuPostgresRowInsert import SubmenuPostgresRowInsert
from src.menu.SubmenuPostgresRowUpdate import SubmenuPostgresRowUpdate
from src.menu.SubmenuPostgresRowDelete import SubmenuPostgresRowDelete
from src.menu.status import status

class SubmenuPostgresRow():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRow class"""
        
        #submenu definition
        self.submenu_postgres_row = ConsoleMenu("PostgreSQL Row Operations", status)
        
        #submenu items
        postgres_row_insert = SubmenuItem("Insert rows", SubmenuPostgresRowInsert().get(), self.submenu_postgres_row)
        postgres_row_update = SubmenuItem("Update rows", SubmenuPostgresRowUpdate().get(), self.submenu_postgres_row)
        postgres_row_delete = SubmenuItem("Delete rows", SubmenuPostgresRowDelete().get(), self.submenu_postgres_row)

        #submenu appends
        self.submenu_postgres_row.append_item(postgres_row_insert)
        self.submenu_postgres_row.append_item(postgres_row_update)
        self.submenu_postgres_row.append_item(postgres_row_delete)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row