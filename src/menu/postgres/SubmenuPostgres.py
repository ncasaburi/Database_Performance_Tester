from consolemenu import *
from consolemenu.items import *
from src.menu.postgres.Database.SubmenuPostgresDatabase import SubmenuPostgresDatabase
from src.menu.postgres.Table.SubmenuPostgresTable import SubmenuPostgresTable
from src.menu.postgres.Row.SubmenuPostgresRow import SubmenuPostgresRow
from src.menu.postgres.Index.SubmenuPostgresIndex import SubmenuPostgresIndex
from src.logic.status import status

class SubmenuPostgres():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgres class"""

        #submenu definition
        self.submenu_postgres = ConsoleMenu("PostgreSQL", status)

        #submenu items
        postgres_database = SubmenuItem("Database", SubmenuPostgresDatabase().get(), menu=self.submenu_postgres)
        postgres_tables = SubmenuItem("Tables", SubmenuPostgresTable().get(), menu=self.submenu_postgres)
        postgres_rows = SubmenuItem("Rows", SubmenuPostgresRow().get(), menu=self.submenu_postgres)
        postgres_indexs = SubmenuItem("Indexes", SubmenuPostgresIndex().get(), menu=self.submenu_postgres)

        #submenu appends
        self.submenu_postgres.append_item(postgres_database)
        self.submenu_postgres.append_item(postgres_tables)
        self.submenu_postgres.append_item(postgres_rows)
        self.submenu_postgres.append_item(postgres_indexs)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres
         