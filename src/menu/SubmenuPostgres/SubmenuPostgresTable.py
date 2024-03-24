from consolemenu import *
from consolemenu.items import *
from src.menu.SubmenuPostgres.SubmenuPostgresTableCreate import SubmenuPostgresTableCreate
from src.menu.SubmenuPostgres.SubmenuPostgresTableDrop import SubmenuPostgresTableDrop
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.menu.status import status
import os


class SubmenuPostgresTable():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresTable class"""
        
        #submenu definition
        self.submenu_postgres_table = ConsoleMenu("PostgreSQL Table Operations", status)
        
        #submenu items
        postgres_table_create = SubmenuItem("Create a table", SubmenuPostgresTableCreate().get(), self.submenu_postgres_table)
        postgres_table_drop = SubmenuItem("Drop a table", SubmenuPostgresTableDrop().get(), self.submenu_postgres_table)
        postgres_table_list = FunctionItem("List available tables", self.postgres_table_list_fn)

        #submenu appends
        self.submenu_postgres_table.append_item(postgres_table_create)
        self.submenu_postgres_table.append_item(postgres_table_drop)
        self.submenu_postgres_table.append_item(postgres_table_list)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_table
    
    def postgres_table_list_fn(self):
        """This function lists the tables"""

        postgres = PostgreSQL()
        print("Please enter the schema name: (if you don't know it, just press enter)")
        schema_name = input()
        if schema_name == "":
            schema_name = "'public'"
        table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = "+schema_name+" AND table_catalog = '"+postgres.status()+"';", expected_result=True)
        os.system('clear')
        if table_list == None:
            print("No tables found\n")
            print("Press enter to continue")
            input()
            return
        else:
            print("Tables:\n")
            for table in table_list:
                print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
                print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
                print("")
            print("Press enter to continue...")
            input()
            return