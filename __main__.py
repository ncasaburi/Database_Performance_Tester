from Queries.PostgreSQL.postgresql import PostgreSQL
from Queries.Mongo.mongo import mongo_connection
from logger import CustomLogger
import datetime
import os

####################### DB CONNECTIONS ###########################

mongodb_connection_string = "mongodb://admin:secret@localhost:27017/"
postgre_connection_string = "postgresql://admin:secret@localhost:32768/"

database_name = "hospital"
logs_directory = "Logs"

##################################################################

def main():
    """Start the application"""

    # Check if the log directory exists
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Initializing logger
    custom_logger = CustomLogger('LOG', log_dir=logs_directory+os.path.sep+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.log')

    #mongo = mongo_connection(mongodb_connection_string, database_name)
    
    number_of_rows = 1000
    custom_logger.info("Number of rows: "+str(number_of_rows))
    postgres = PostgreSQL(postgre_connection_string, custom_logger, database_name)
    postgres.run_query_from_file('Queries/PostgreSQL/Creates/Tables',custom_logger,'Creating tables...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctors',custom_logger,'Populating doctors table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patients',custom_logger,'Populating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecords',custom_logger,'Populating medical records table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_PatientDoctorMedicalRecord',custom_logger,'Populating relationships table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Patients',custom_logger,'Updating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Doctors',custom_logger,'Updating doctors table...')
    postgres.close(custom_logger)

    number_of_rows = 5000
    custom_logger.info("Number of rows: "+str(number_of_rows))
    postgres = PostgreSQL(postgre_connection_string, custom_logger, database_name)
    postgres.run_query_from_file('Queries/PostgreSQL/Creates/Tables',custom_logger,'Creating tables...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctors',custom_logger,'Populating doctors table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patients',custom_logger,'Populating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecords',custom_logger,'Populating medical records table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_PatientDoctorMedicalRecord',custom_logger,'Populating relationships table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Patients',custom_logger,'Updating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Doctors',custom_logger,'Updating doctors table...')
    postgres.close(custom_logger)

    number_of_rows = 10000
    custom_logger.info("Number of rows: "+str(number_of_rows))
    postgres = PostgreSQL(postgre_connection_string, custom_logger, database_name)
    postgres.run_query_from_file('Queries/PostgreSQL/Creates/Tables',custom_logger,'Creating tables...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctors',custom_logger,'Populating doctors table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patients',custom_logger,'Populating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecords',custom_logger,'Populating medical records table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_PatientDoctorMedicalRecord',custom_logger,'Populating relationships table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Patients',custom_logger,'Updating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Doctors',custom_logger,'Updating doctors table...')
    postgres.close(custom_logger)

    number_of_rows = 50000
    custom_logger.info("Number of rows: "+str(number_of_rows))
    postgres = PostgreSQL(postgre_connection_string, custom_logger, database_name)
    postgres.run_query_from_file('Queries/PostgreSQL/Creates/Tables',custom_logger,'Creating tables...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctors',custom_logger,'Populating doctors table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patients',custom_logger,'Populating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecords',custom_logger,'Populating medical records table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_PatientDoctorMedicalRecord',custom_logger,'Populating relationships table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Patients',custom_logger,'Updating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Doctors',custom_logger,'Updating doctors table...')
    postgres.close(custom_logger)

    number_of_rows = 100000
    custom_logger.info("Number of rows: "+str(number_of_rows))
    postgres = PostgreSQL(postgre_connection_string, custom_logger, database_name)
    postgres.run_query_from_file('Queries/PostgreSQL/Creates/Tables',custom_logger,'Creating tables...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Doctors',custom_logger,'Populating doctors table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_Patients',custom_logger,'Populating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_MedicalRecords',custom_logger,'Populating medical records table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Inserts/'+str(number_of_rows)+os.path.sep+str(number_of_rows)+'_PatientDoctorMedicalRecord',custom_logger,'Populating relationships table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Patients',custom_logger,'Updating patients table...')
    postgres.run_query_from_file('Queries/PostgreSQL/Updates/Doctors',custom_logger,'Updating doctors table...')
    postgres.close(custom_logger)
    
main()