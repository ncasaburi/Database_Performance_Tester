from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger

def mongo_database_create_fn(type:str):
    """This function allows the user to create a MongoDB database"""

    try:
        mongo = MongoDB()
        if type == "default":
            mongo.create(Config().default_dbs["default_mongo_connection_string"],Config().default_dbs["default_database_name"])
        else:
            print("Enter the connection string: (example: mongodb://user:password@localhost:27017/)")
            mongo_connection_string = input()
            print("Enter the database name:")
            db_name = input()
            mongo.create(mongo_connection_string,db_name)
    except:
        SingleLogger().logger.exception("Error while creating a MongoDB database", exc_info=True)