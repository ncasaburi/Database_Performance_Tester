from consolemenu import *
from consolemenu.items import *
from src.menu.postgres.Database.SubmenuPostgresDatabase import SubmenuPostgresDatabase
from src.menu.postgres.Table.SubmenuPostgresTable import SubmenuPostgresTable
from src.menu.postgres.Row.SubmenuPostgresRow import SubmenuPostgresRow
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
        postgres_files = SubmenuItem("Files", self.submenu_postgres, menu=self.submenu_postgres)

        #submenu appends
        self.submenu_postgres.append_item(postgres_database)
        self.submenu_postgres.append_item(postgres_tables)
        self.submenu_postgres.append_item(postgres_rows)
        self.submenu_postgres.append_item(postgres_files)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres
         