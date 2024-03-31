from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
import os

def postgres_row_insert_fn(type:str, requested_rows:int=0, current_iteration:int=0, total_iterations:int=0):
    """This function allows the user to insert rows into a PostgreSQL database"""       
    
    try:
        postgres = PostgreSQL()
        if type == "default":
            default_insert_set = int(Config().default_memory["default_insert_set"])
            default_number_files = int(Config().default_memory["default_insert_files"])

            if requested_rows == 0:
                actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","Calculating the number of rows in the doctors' table",expected_result=True)[0][0]
                actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","Calculating the number of rows in the patients' table",expected_result=True)[0][0]
                actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","Calculating the number of rows in the medical_records' table",expected_result=True)[0][0]
                actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","Calculating the number of rows in the doctor_medical_records' table",expected_result=True)[0][0]
                if actual_doctor_rows == 0 and actual_patient_rows == 0 and actual_medicalrecord_rows == 0 and actual_doctormedicalrecord_rows == 0:
                    Config().default_postgres_lines_read = 0
                    Config().default_postgres_last_file_read = 1

                rows_left = (default_insert_set * default_number_files) - Config().default_postgres_lines_read

            #If there are rows left and the number of rows on each table is the same as the number stored on default_postgres_lines_read
            if (requested_rows > 0) or (rows_left > 0 and actual_doctor_rows == Config().default_postgres_lines_read and actual_patient_rows == Config().default_postgres_lines_read and actual_medicalrecord_rows == Config().default_postgres_lines_read and actual_doctormedicalrecord_rows == Config().default_postgres_lines_read):
                if requested_rows == 0:
                    os.system('clear')
                    print("Please, enter the number of rows you want to insert: ("+str(rows_left)+" rows left)")
                    requested_rows = int(input())

                    if requested_rows > rows_left:
                        print("The number of rows requested exceed the number of rows left.\nAs a result, "+str(rows_left)+" rows will be inserted")
                        input("Press enter to continue")
                        requested_rows = rows_left
                
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Doctors:") if total_iterations == 0 else print("Doctors:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_sql_content("Doctors", requested_rows, default_insert_set, Config().default_postgres_lines_read, Config().default_postgres_last_file_read, postgres)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Patients:") if total_iterations == 0 else print("Patients:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_sql_content("Patients", requested_rows, default_insert_set, Config().default_postgres_lines_read, Config().default_postgres_last_file_read, postgres)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("MedicalRecords:") if total_iterations == 0 else print("MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_sql_content("MedicalRecords", requested_rows, default_insert_set, Config().default_postgres_lines_read, Config().default_postgres_last_file_read, postgres)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Doctors - MedicalRecords:") if total_iterations == 0 else print("Doctors - MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                (requested_rows, default_insert_set,Config().default_postgres_lines_read,Config().default_postgres_last_file_read) = load_sql_content("Doctor_MedicalRecords", requested_rows, default_insert_set, Config().default_postgres_lines_read, Config().default_postgres_last_file_read, postgres)
            else:
                os.system('clear')
                print("\nPlease, clean the default tables")
                input("\nPress enter to go back to the menu")
        else:
            os.system('clear')
            print("Enter the query to insert the rows: \nExample: INSERT INTO tablename (colname1, colname2, colname3) VALUES ('value1','value2', 'value3');\n")
            query = input()
            query = query.lower()
            if query.startswith("insert into"):
                postgres.run_query(query, "Inserting custom rows")
            else:
                print("\nThe query must begin with INSERT INTO")
                input("\nPress enter to go back to the menu")
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while inserting rows", exc_info=True)

def load_sql_content(element:str, requested_rows:int, default_insert_set:int, default_postgres_lines_read, default_postgres_last_file_read, postgres) -> list:
    """This function iterates over data files until all requested rows are gathered and then inserts them into the database"""

    try:
        current_file_row = default_postgres_lines_read - ( (default_postgres_last_file_read - 1) * default_insert_set)
                
        content_sql = ""        
        pending_rows = requested_rows

        print("\n  loading data...")
        #While the requested number of rows involves more than one file
        while current_file_row + pending_rows >= default_insert_set:
            requested_rows_aux = default_insert_set - current_file_row

            #Unzipping and storing rows
            if content_sql == "": #If this is the first iteration
                content_sql = content_sql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_insert_set)+"_"+element.lower()+"_set"+str(default_postgres_last_file_read)+".zip","sql").splitlines()[current_file_row:default_insert_set]))
            else:
                content_sql = content_sql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_insert_set)+"_"+element.lower()+"_set"+str(default_postgres_last_file_read)+".zip","sql").splitlines()[current_file_row:default_insert_set]))
                
            default_postgres_lines_read = default_postgres_lines_read + requested_rows_aux
            pending_rows = pending_rows - requested_rows_aux
            current_file_row = 0
            default_postgres_last_file_read = default_postgres_last_file_read + 1

        #If there are still rows pending to be added but they are fewer than the number of rows per file
        if pending_rows > 0:
            max_row_number = pending_rows + current_file_row
            
            #Unzipping and storing rows
            if content_sql == "": #If this is the first iteration
                content_sql = content_sql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_insert_set)+"_"+element.lower()+"_set"+str(default_postgres_last_file_read)+".zip","sql").splitlines()[current_file_row:max_row_number]))
            else:
                content_sql = content_sql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_insert_set)+"_"+element.lower()+"_set"+str(default_postgres_last_file_read)+".zip","sql").splitlines()[current_file_row:max_row_number]))
                
            default_postgres_lines_read = default_postgres_lines_read + pending_rows
            current_file_row = pending_rows + 1
            pending_rows = 0                
        #Inserting rows
        print("  inserting rows...")
        postgres.run_query(content_sql,"Adding "+str(len(content_sql.splitlines()))+" "+element.lower())
        return (requested_rows,default_insert_set,default_postgres_lines_read,default_postgres_last_file_read)
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while loading sql content", exc_info=True)

