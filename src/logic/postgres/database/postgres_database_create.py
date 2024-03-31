from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger
import os

def postgres_database_create_fn(type:str):
    """This function allows the user to create a PostgreSQL database"""

    try:
        os.system('clear')        
        print("Database creation\n\n")
        postgres = PostgreSQL()
        if type == "default":
            postgres.create(Config().default_dbs["default_postgres_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("  Example:\n")
            print("    Connection string: postgresql://user:password@localhost:5432")
            print("    Database name: postgres")
            print("\n  Your input:")
            postgres_connection_string = input("\n    Connection string: postgresql://")
            db_name = input("    Database name: ")
            if not postgres_connection_string.startswith("postgresql://"):
                postgres_connection_string = "postgresql://" + postgres_connection_string
            if not postgres_connection_string.endswith("/"):
                postgres_connection_string = postgres_connection_string + "/"
            postgres.create(postgres_connection_string,db_name)
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while creating a database", exc_info=True)