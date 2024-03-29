from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger


def mongo_database_drop_fn(type:str):
    """This function allows the user to drop a MongoDB database"""

    try:
        if type == "default":
            MongoDB().drop(Config().default_dbs["default_database_name"])
        elif type == "current":
            MongoDB().drop(MongoDB().status())
        else:
            print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
            print("Enter the database name:")
            db_name = input()
            MongoDB().drop(db_name)
    except:
        SingleLogger().logger.exception("Error while dropping a MongoDB database", exc_info=True)