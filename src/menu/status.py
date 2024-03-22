from src.drivers.PostgreSQLDriver import PostgreSQL
from colors import color
from src.logger.SingleLogger import SingleLogger
import os

def status() -> str:
    
    db_status = PostgreSQL().status()
    current_log = os.path.basename(SingleLogger().logger.get_path())

    if db_status == "Disconnected":
        return "Current database: "+color(db_status, fg="red")+"\nCurrent log: "+color(current_log, fg="green")
    else:
        return "Current database: "+color(db_status+" (PostgreSQL)", fg="green")+"\nCurrent log: "+color(current_log, fg="green")