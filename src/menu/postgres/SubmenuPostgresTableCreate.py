from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper

class SubmenuPostgresTableCreate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTableCreate class"""
        
        #submenu definition
        self.submenu_postgres_table_create = ConsoleMenu("PostgreSQL Table Creation", status )
        
        #submenu items
        postgres_table_create_default = FunctionItem("Create default tables", self.postgres_table_create_fn, args=["default"]) 
        postgres_table_create_custom = FunctionItem("Create a custom table", self.postgres_table_create_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_table_create.append_item(postgres_table_create_default)
        self.submenu_postgres_table_create.append_item(postgres_table_create_custom)

    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table_create
    
    def postgres_table_create_fn(self, type:str):
        """This function allows the user to create a table"""
        
        postgres = PostgreSQL()
        if type == "default":
            content_sql = Zipper().unzip_content(Config().default_data["default_postgres_creates"]+"Tables.zip","sql")
            postgres.run_query(content_sql, "Creating default tables...")
        else:
            print("Enter the table creation query: \nExample: CREATE TABLE tablename ( columnname1 SERIAL PRIMARY KEY, columenname2 VARCHAR(50), columnname3 VARCHAR(50) )\n");
            query = input()
            query = query.lower()
            if query.startswith("create table"):
                postgres.run_query(query, "Creating a new custom table...")
            else:
                print("\nThe query must begin with CREATE TABLE")
                print("\nPress enter to go back to the menu")
                input()