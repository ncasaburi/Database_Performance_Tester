from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn

def postgres_table_drop_fn(type:str):
    """This function allows the user to drop a table"""

    try:
        postgres = PostgreSQL()
        if type == "default":
            content_sql = Zipper().unzip_content(Config().default_data["default_postgres_drops"]+"Tables.zip","sql")
            postgres.run_query(content_sql, "Dropping default tables")
        else:
            postgres_table_list_fn(enable_interaction=False)
            print("Enter your query to drop a table:\n")
            print("  Example:")
            print("    DROP TABLE schemaname.tablename")
            schemaname_tablename = input("\n\n  DROP TABLE ")
            query = ""
            if not schemaname_tablename == "":
                query = "DROP TABLE "+schemaname_tablename
                postgres.run_query(query,f"Dropping table {query}")
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while dropping a table", exc_info=True)