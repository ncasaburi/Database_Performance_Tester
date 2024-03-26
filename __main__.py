from src.drivers.PostgreSQLDriver import PostgreSQL
from src.drivers.MongoDBDriver import MongoDB
from src.logger.CustomLogger import CustomLogger
from src.logger.SingleLogger import SingleLogger
from src.menu.MainMenu import MainMenu
from src.config.Config import Config
import datetime
import os

def main():
    """Start the application"""

    mongo = MongoDB()

    postgres = PostgreSQL()

    MainMenu()

    postgres.close()
    
    mongo.close()
main()