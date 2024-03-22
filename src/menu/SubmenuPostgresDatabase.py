from consolemenu import *
from consolemenu.items import *
from src.menu.SubmenuPostgresDatabaseConnect import SubmenuPostgresDatabaseConnect
from src.menu.SubmenuPostgresDatabaseCreate import SubmenuPostgresDatabaseCreate
from src.menu.SubmenuPostgresDatabaseDrop import SubmenuPostgresDatabaseDrop
from src.menu.status import status

class SubmenuPostgresDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabase class"""
        
        #submenu definition
        self.submenu_postgres_database = ConsoleMenu("PostgreSQL Database Operations", status)
        
        #submenu items
        postgres_database_create = SubmenuItem("Create database", SubmenuPostgresDatabaseCreate().get(), self.submenu_postgres_database)
        postgres_database_connect = SubmenuItem("Connect to database", SubmenuPostgresDatabaseConnect().get(), self.submenu_postgres_database)
        postgres_database_drop = SubmenuItem("Drop database", SubmenuPostgresDatabaseDrop().get(), self.submenu_postgres_database)

        #submenu appends
        self.submenu_postgres_database.append_item(postgres_database_create)
        self.submenu_postgres_database.append_item(postgres_database_connect)
        self.submenu_postgres_database.append_item(postgres_database_drop)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database