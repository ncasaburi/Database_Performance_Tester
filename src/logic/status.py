from src.drivers.PostgreSQLDriver import PostgreSQL
from src.drivers.MongoDBDriver import MongoDB
from colors import color
from src.logger.SingleLogger import SingleLogger
from src.config.Config import Config
from src.logic.miscellaneous.miscellaneous_autoconnect import autoconnect_read
import os

def status() -> str:
    
    current_log = os.path.basename(SingleLogger().logger.get_path())
    default_db = Config().default_dbs["default_database_name"]
    db_status_PostgreSQL, autoconnect = database_check(PostgreSQL, autoconnect_read(), Config().default_dbs["default_postgres_connection_string"], default_db)
    db_status_MongoDB, autoconnect = database_check(MongoDB, autoconnect_read(), Config().default_dbs["default_mongo_connection_string"], default_db)

    return "Databases (autoconnect: "+autoconnect+")"+"\n - PostgreSQL: "+db_status_PostgreSQL+"\n - MongoDB: "+db_status_MongoDB+"\nCurrent log: "+color(current_log, fg="green")


def database_check(db, default_database_autoconnect:bool, default_connection_string:str, default_database_name:str) -> list:
    """This function checks whether there is a database connection established. Also, the function autoconnects to a default database if this option is enabled"""

    current_stauts = db().status()

    if current_stauts == "Disconnected":
        if default_database_autoconnect == True:
            db().connect(default_connection_string,default_database_name)
            current_stauts = db().status()

    if current_stauts == "Disconnected":
        current_stauts = color(current_stauts, fg="red")
    else:
        current_stauts = color(current_stauts, fg="green")

    if default_database_autoconnect == True:
        autoconnect = color("on", fg="green")
    else:
        autoconnect = color("off", fg="red")

    return current_stauts, autoconnect