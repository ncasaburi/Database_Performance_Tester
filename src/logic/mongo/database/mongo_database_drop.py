from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger


def mongo_database_drop_fn(type:str):
    """This function allows the user to drop a MongoDB database"""

    try:
        mongo = MongoDB()
        if type == "default":
            mongo.drop(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
        elif type == "current":
            mongo.drop(mongo.connection_string ,mongo.status())
        else:
            print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
            connection_string = input("mongodb://")
            db_name = input("Enter the database name: ")
            if not connection_string.startswith("mongodb://"):
                connection_string = "mongodb://" + connection_string
            mongo.drop(connection_string, db_name)
    except:
        SingleLogger().logger.exception("Error while dropping a MongoDB database", exc_info=True)