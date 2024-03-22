from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.CustomLogger import CustomLogger
from src.logger.SingleLogger import SingleLogger
from src.menu.MainMenu import MainMenu
from src.config.Config import Config
import datetime
import os

def main():
    """Start the application"""

    # Initializing logger
    SingleLogger().logger = CustomLogger(name=Config().default_logs["default_log_name"], log_dir=Config().default_logs["default_log_path"]+os.path.sep+str(datetime.datetime.now().strftime(Config().default_logs["default_log_time_format"]))+'.log')

    postgres = PostgreSQL()

    MainMenu()

    postgres.close()
    
main()