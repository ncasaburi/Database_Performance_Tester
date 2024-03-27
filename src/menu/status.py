from src.drivers.PostgreSQLDriver import PostgreSQL
from src.drivers.MongoDBDriver import MongoDB
from colors import color
from src.logger.SingleLogger import SingleLogger
import os

def status() -> str:
    
    db_status_PostgreSQL = PostgreSQL().status()
    db_status_MongoDB = MongoDB().status()
    
    current_log = os.path.basename(SingleLogger().logger.get_path())

    if db_status_PostgreSQL == "Disconnected":
        status_PostgreSQL = color(db_status_PostgreSQL, fg="red")
    else:
        status_PostgreSQL = color(db_status_PostgreSQL, fg="green")

    if db_status_MongoDB == "Disconnected":
        status_Mongo = color(db_status_MongoDB, fg="red")
    else:
        status_Mongo = color(db_status_MongoDB, fg="green")    

    return "Databases"+"\n - PostgreSQL: "+status_PostgreSQL+"\n - MongoDB: "+status_Mongo+"\nCurrent log: "+color(current_log, fg="green")