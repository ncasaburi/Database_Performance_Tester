from consolemenu import *
from consolemenu.items import *
from src.menu.postgres.Database.SubmenuPostgresDatabaseConnect import SubmenuPostgresDatabaseConnect
from src.menu.postgres.Database.SubmenuPostgresDatabaseCreate import SubmenuPostgresDatabaseCreate
from src.menu.postgres.Database.SubmenuPostgresDatabaseDrop import SubmenuPostgresDatabaseDrop
from src.logic.status import status
from src.logic.postgres.database.postgres_database_list import postgres_database_list_fn

class SubmenuPostgresDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabase class"""
        
        #submenu definition
        self.submenu_postgres_database = ConsoleMenu("PostgreSQL Database Operations", status)
        
        #submenu items
        postgres_database_create = SubmenuItem("Create database", SubmenuPostgresDatabaseCreate().get(), self.submenu_postgres_database)
        postgres_database_connect = SubmenuItem("Connect to database", SubmenuPostgresDatabaseConnect().get(), self.submenu_postgres_database)
        postgres_database_list = FunctionItem("List available databases", postgres_database_list_fn)
        postgres_database_drop = SubmenuItem("Drop database", SubmenuPostgresDatabaseDrop().get(), self.submenu_postgres_database)

        #submenu appends
        self.submenu_postgres_database.append_item(postgres_database_create)
        self.submenu_postgres_database.append_item(postgres_database_connect)
        self.submenu_postgres_database.append_item(postgres_database_list)
        self.submenu_postgres_database.append_item(postgres_database_drop)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database

