from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger

def postgres_database_list_fn() -> None:
    """This function allows the user to see all available PostgreSQL databases"""

    try:
        postgres = PostgreSQL()
        db_list = postgres.run_query("SELECT datname FROM pg_database","Listing all available Postgres databases", True)
        if db_list == None:
            print("No databases found\n")
            print("Press enter to continue")
            input()
            return
        else:
            print("Databases:\n")
            for db in db_list:
                print(" - "+db[0])
            print("\nPress enter to continue...")
            input()
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while listing available databases", exc_info=True)
