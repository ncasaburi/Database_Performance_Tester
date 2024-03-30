from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper

def postgres_index_create_fn(type:str):
    """This function allows the user to create a index"""
    
    try:
        postgres = PostgreSQL()
        if type == "default":
            print("Creating default indexes...")
            content_sql = Zipper().unzip_content(Config().default_data["default_postgres_indexes"]+"Indexes.zip","sql")
            postgres.run_query(content_sql, "Creating default indexes...")
        else:
            print("Enter the table creation query: \nExample: CREATE INDEX indexname ON tablename ( columnname1, columname2 ...);")
            query = input()
            query = query.lower()
            if query.startswith("create index"):
                postgres.run_query(query, "Creating a new custom index...")
            else:
                print("\nThe query must begin with CREATE INDEX")
                print("\nPress enter to go back to the menu")
                input()
    except:
        SingleLogger().logger.exception("Error while creating a MongoDB index", exc_info=True)