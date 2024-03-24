from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger

class SubmenuPostgresDatabaseDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresDatabaseDrop class"""
        
        #submenu definition
        self.submenu_postgres_database_drop = ConsoleMenu("PostgreSQL Database Drop", status)
        
        #submenu items
        postgres_database_drop_default = FunctionItem("Drop default database", self.postgres_database_drop_fn, args=["default"]) 
        postgres_database_drop_current = FunctionItem("Drop current database", self.postgres_database_drop_fn, args=["current"]) 
        postgres_database_drop_custom = FunctionItem("Drop a custom database", self.postgres_database_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_default)
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_current)
        self.submenu_postgres_database_drop.append_item(postgres_database_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_database_drop
    
    def postgres_database_drop_fn(self, type:str):
        """This function allows the user to drop a PostgreSQL database"""

        try:
            postgres = PostgreSQL()
            if type == "default":
                postgres.drop(Config().default_dbs["default_postgres_connection_string"],Config().default_dbs["default_database_name"])
            elif type == "current":
                postgres.drop(postgres.connection_string,postgres.status())
            else:
                print("Enter the connection string: (example: postgresql://user:password@localhost:32768/)")
                postgre_connection_string = input()
                print("Enter the database name:")
                db_name = input()
                postgres.drop(postgre_connection_string,db_name)
        except:
            SingleLogger().logger.exception("Error while dropping a PostgreSQL database", exc_info=True)