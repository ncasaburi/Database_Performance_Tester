from src.drivers.PostgreSQLDriver import PostgreSQL
from src.drivers.MongoDriver import MongoDB
from src.logger.CustomLogger import CustomLogger
from src.logger.SingleLogger import SingleLogger
from src.menu.MainMenu import MainMenu
from src.config.Config import Config
import datetime
import os

def main():
    """Start the application"""
    #Configuración MongoDB
    mongodb_connection_string = "mongodb://admin:secret@localhost:27017/"
    database_name = "hospital"
    logs_directory = "logs"

    # Initializing logger
    custom_logger = CustomLogger('LOG', log_dir=logs_directory+os.path.sep+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.log')
    
    # Create MongoDB instance
    mongo = MongoDB(mongodb_connection_string, custom_logger, database_name)
    # Execute operations from 500_Doctors.zip file
    number_of_rows = 100
    custom_logger.info("MongoDB Stress Test - Number of transaction: "+str(number_of_rows))
    custom_logger.info("*********************************************************")
    mongo.execute_operations_from_file(custom_logger,'data/Mongo/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patient_Documents','Populating Patient_Documents collection...')
    mongo.execute_operations_from_file(custom_logger,'data/Mongo/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctor_Documents','Populating Doctor_Documents collection...')
    mongo.execute_operations_from_file(custom_logger,'data/Mongo/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecord_Documents','Populating medical record documents collection...')
    mongo.execute_operations_from_file(custom_logger,'data/Mongo/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_DoctorMedicalRecord_Documents','Populating relationships documents collection...')


    #Fin Configuración Mongo

    # Initializing logger
    SingleLogger().logger = CustomLogger(name=Config().default_logs["default_log_name"], log_dir=Config().default_logs["default_log_path"]+os.path.sep+str(datetime.datetime.now().strftime(Config().default_logs["default_log_time_format"]))+'.log')


    postgres = PostgreSQL()

    MainMenu()

    postgres.close()
    
main()