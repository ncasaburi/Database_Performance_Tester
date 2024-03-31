from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
import os


def postgres_table_list_fn(enable_interaction:bool=True):
    """This function lists the tables"""

    try:
        schema_name = ""
        postgres = PostgreSQL()
        if enable_interaction:
            print("Please enter the schema name: (if you don't know it, just press enter)")
            schema_name = input()
        if schema_name == "":
            schema_name = "'public'"
        table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = "+schema_name+" AND table_catalog = '"+postgres.status()+"';", "Listing all available tables", expected_result=True)
        os.system('clear')
        if table_list == None:
            print("No tables found\n")
            if enable_interaction:
                print("Press enter to continue...")
                input()
                return
        else:
            print("Tables:\n")
            for table in table_list:
                print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),f"Counting the number of rows on table {table[0]}",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';",f"Counting the number of columns on table {table[0]}",expected_result=True)[0][0])+", size: "+str(postgres.table_space_occupied(str(table[0])))+" MB)")
                print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"' ORDER BY ordinal_position","Getting column names of table "+str(table[0]),expected_result=True))+")")
                print("")
            if enable_interaction:
                print("Press enter to continue...")
                input()
                return
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while listing tables", exc_info=True)