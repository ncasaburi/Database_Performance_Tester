from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger

def postgres_table_drop_fn(type:str):
    """This function allows the user to drop a table"""

    try:
        postgres = PostgreSQL()
        if type == "default":
            content_sql = Zipper().unzip_content(Config().default_data["default_postgres_drops"]+"Tables.zip","sql")
            postgres.run_query(content_sql, "Dropping default tables...")
        else:
            table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = '"+postgres.status()+"';", expected_result=True)
            print("Tables:\n")
            for table in table_list:
                print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
                print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
            print("")
            print("Enter your query to drop a table:\n")
            print("  Example:")
            print("    DROP TABLE schemaname.tablename")
            schemaname_tablename = input("\n\n  DROP TABLE ")
            query = ""
            if not schemaname_tablename == "":
                query = "DROP TABLE "+schemaname_tablename
                postgres.run_query(query)
    except:
        SingleLogger().logger.exception("Error while dropping a PostgreSQL table", exc_info=True)