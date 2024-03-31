from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger

def postgres_database_drop_fn(type:str):
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
        SingleLogger().logger.exception("PostgreSQL: Error while dropping a database", exc_info=True)