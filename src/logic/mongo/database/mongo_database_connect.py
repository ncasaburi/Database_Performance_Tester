from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger

def mongo_database_connect_fn(type:str):
    """This function allows the user to connect to a MongoDB database"""

    try:
        mongo = MongoDB()
        if type == "default":
            mongo.connect(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
            mongo_connection_string = input()
            print("Enter the database name:")
            db_name = input()
            mongo.connect(mongo_connection_string,db_name)
    except:
        SingleLogger().logger.exception("MongoDB: Error while connecting to a database", exc_info=True)