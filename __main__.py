from postgresql import postgres_connection
from mongo import mongo_connection
import time
####################### DB CONNECTIONS ###########################

mongodb_connection_string = "mongodb://admin:secret@localhost:27017/"
postgre_connection_string = "postgresql://admin:secret@localhost:32768/"

database_name = "hospital"

##################################################################

def main():
    """Start the application"""
    
    #mongo = mongo_connection(mongodb_connection_string, database_name)
    postgres = postgres_connection(postgre_connection_string)

    print("Removing database if already exists...")
    with open('Queries/PostgreSQL/Drops/DatabaseDrop.sql', 'r') as file:
        query = file.read()
        postgres.execute(query+" "+database_name)

    print("\nCreating database...")
    with open('Queries/PostgreSQL/Creates/DatabaseCreation.sql', 'r') as file:
        query = file.read()
        start_counter = time.time()
        postgres.execute(query+" "+database_name)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")

    postgres = postgres_connection(postgre_connection_string, database_name)

    print("\nCreating tables...")
    with open('Queries/PostgreSQL/Creates/TablesCreation.sql', 'r') as file:
        sql_query = file.read()
        start_counter = time.time()
        postgres.execute(sql_query)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")

    print("\nPopulating doctors table...")
    with open('Queries/PostgreSQL/Inserts/InsertDoctors10000.sql', 'r') as file:
        sql_query = file.read()
        start_counter = time.time()
        postgres.execute(sql_query)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")

    print("\nPopulating patients table...")
    with open('Queries/PostgreSQL/Inserts/InsertPatients10000.sql', 'r') as file:
        sql_query = file.read()
        start_counter = time.time()
        postgres.execute(sql_query)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
        
    print("\nPopulating medical records table...")
    with open('Queries/PostgreSQL/Inserts/InsertMedicalRecords10000.sql', 'r') as file:
        sql_query = file.read()
        start_counter = time.time()
        postgres.execute(sql_query)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")

    print("\nPopulating relationships table...")
    with open('Queries/PostgreSQL/Inserts/InsertPatientDoctorMedicalRecord10000.sql', 'r') as file:
        sql_query = file.read()
        start_counter = time.time()
        postgres.execute(sql_query)
        stop_counter = time.time()
        print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")

main()