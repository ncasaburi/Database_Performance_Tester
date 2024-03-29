from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger

def postgres_database_connect_fn(type:str):
    """This function allows the user to connect to a PostgreSQL database"""

    try:
        postgres = PostgreSQL()
        if type == "default":
            postgres.connect(Config().default_dbs["default_postgres_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("Enter the connection string: (example: postgresql://user:password@localhost:32768/)")
            postgre_connection_string = input()
            print("Enter the database name:")
            db_name = input()
            postgres.connect(postgre_connection_string,db_name)
    except:
        SingleLogger().logger.exception("Error while creating a PostgreSQL database", exc_info=True)