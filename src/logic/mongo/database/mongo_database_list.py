from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_database_list_fn() -> None:
    """This function allows the user to see all available MongoDB databases"""

    try:
        if MongoDB().status() == "Disconnected":
            print("Database disconnected")
        else:
            list_databases = MongoDB().client.list_database_names()
        print("Databases:\n")
        for db in list_databases:
            print(" - "+db)
        print("\nPress enter to continue...")
        input()
    except:
        SingleLogger().logger.exception("Error while listing MongoDB databases", exc_info=True)