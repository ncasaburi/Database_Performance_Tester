from consolemenu import *
from consolemenu.items import *
from src.menu.postgres.SubmenuPostgresDatabaseConnect import SubmenuPostgresDatabaseConnect
from src.menu.postgres.SubmenuPostgresDatabaseCreate import SubmenuPostgresDatabaseCreate
from src.menu.postgres.SubmenuPostgresDatabaseDrop import SubmenuPostgresDatabaseDrop
from src.menu.status import status
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger

class SubmenuPostgresDatabase():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabase class"""
        
        #submenu definition
        self.submenu_postgres_database = ConsoleMenu("PostgreSQL Database Operations", status)
        
        #submenu items
        postgres_database_create = SubmenuItem("Create database", SubmenuPostgresDatabaseCreate().get(), self.submenu_postgres_database)
        postgres_database_connect = SubmenuItem("Connect to database", SubmenuPostgresDatabaseConnect().get(), self.submenu_postgres_database)
        postgres_database_list = FunctionItem("List available databases", self.postgres_database_list_fn)
        postgres_database_drop = SubmenuItem("Drop database", SubmenuPostgresDatabaseDrop().get(), self.submenu_postgres_database)

        #submenu appends
        self.submenu_postgres_database.append_item(postgres_database_create)
        self.submenu_postgres_database.append_item(postgres_database_connect)
        self.submenu_postgres_database.append_item(postgres_database_list)
        self.submenu_postgres_database.append_item(postgres_database_drop)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database
    
    def postgres_database_list_fn(self) -> None:
        """This function allows the user to see all available PostgreSQL databases"""

        try:
            postgres = PostgreSQL()
            db_list = postgres.run_query("SELECT datname FROM pg_database","Listing all available Postgres databases", True)
            if db_list == None:
                print("No databases found\n")
                print("Press enter to continue")
                input()
                return
            else:
                print("Databases:\n")
                for db in db_list:
                    print(" - "+db[0])
                print("\nPress enter to continue...")
                input()
        except:
            SingleLogger().logger.exception("Error while listing available PostgreSQL databases", exc_info=True)

