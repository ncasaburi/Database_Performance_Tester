from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper

def postgres_table_create_fn(type:str):
    """This function allows the user to create a table"""
    
    try:
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
    except:
        SingleLogger().logger.exception("Error while creating a MongoDB table", exc_info=True)