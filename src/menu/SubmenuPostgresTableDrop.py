from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status

class SubmenuPostgresTableDrop():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTableDrop class"""
        
        #submenu definition
        self.submenu_postgres_table_drop = ConsoleMenu("PostgreSQL Table Drop", status)
        
        #submenu items
        postgres_table_drop_default = FunctionItem("Drop default tables", self.postgres_table_drop_fn, args=["default"]) 
        postgres_table_drop_custom = FunctionItem("Drop a custom table", self.postgres_table_drop_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_table_drop.append_item(postgres_table_drop_default)
        self.submenu_postgres_table_drop.append_item(postgres_table_drop_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table_drop
    
    def postgres_table_drop_fn(self, type:str):
        """This function allows the user to drop a table"""

        postgres = PostgreSQL()
        if type == "default":
            postgres.run_query_from_zip(Config().default_data["default_postgres_drops"]+"Tables.zip", True, "Dropping default tables...")
        else:
            print("Enter the query to drop a table: \nExample: DROP TABLE schemaname.tablename\n");
            query = input()
            query = query.lower()
            if query.startswith("drop table"):
                postgres.run_query(query, "Dropping a custom table...")
            else:
                print("\nThe query must begin with DROP TABLE")
                print("Press enter to go back to the menu")
                input()