from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.row.postgres_row_insert import postgres_row_insert_fn
import os
import time

def postgres_row_batch_insert_fn():
    """This function allows the user to execute batch row inserts into a PostgreSQL database"""       
    
    try:
        postgres = PostgreSQL()
        default_insert_set = int(Config().default_memory["default_insert_set"])
        default_number_files = int(Config().default_memory["default_insert_files"])

        actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0]
        actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","",expected_result=True)[0][0]
        actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","",expected_result=True)[0][0]
        actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","",expected_result=True)[0][0]
        if actual_doctor_rows == 0 and actual_patient_rows == 0 and actual_medicalrecord_rows == 0 and actual_doctormedicalrecord_rows == 0:
            Config().default_postgres_lines_read = 0
            Config().default_postgres_last_file_read = 1

        rows_left = (default_insert_set * default_number_files) - Config().default_postgres_lines_read
        
        confirmation_loop = True
        #If there are rows left and the number of rows on each table is the same as the number stored on default_postgres_lines_read
        if rows_left > 0 and actual_doctor_rows == Config().default_postgres_lines_read and actual_patient_rows == Config().default_postgres_lines_read and actual_medicalrecord_rows == Config().default_postgres_lines_read and actual_doctormedicalrecord_rows == Config().default_postgres_lines_read:
            while(confirmation_loop):
                os.system('clear')

                print("Batch row inserts     ("+str(rows_left)+" rows left)\n")
                
                total_requested_rows = int(input("  Total number of rows you want to insert: "))               
                rows_per_batch = int(input("  Number of rows you want to insert per batch: "))
                gap = float(input("  Gap between batch inserts (in seconds): "))

                if total_requested_rows > rows_left:
                    print("\nThe total number of rows to be inserted can't be greater than the number of rows left")
                    input("\n\nPress enter to continue...")
                    continue

                if total_requested_rows == 0:
                    print("\nThe total number of rows to be inserted must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue
                
                if rows_per_batch == 0:
                    print("\nThe number of rows per batch must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue

                if gap == 0:
                    print("\nThe gap between batch inserts must be greater than 0 seconds")
                    input("\n\nPress enter to continue...")
                    continue
                    
                if rows_per_batch > total_requested_rows:
                    print("\nThe total number of rows requested must be greater than the number of rows per batch")
                    input("\n\nPress enter to continue...")
                    continue

                sets = total_requested_rows / rows_per_batch
                if total_requested_rows % rows_per_batch != 0:
                    last_set_rows = total_requested_rows - (rows_per_batch * int(set))
                    sets = sets + 1
                    print("\n  As a result:")
                    print("    "+str(int(sets))+" batchs are going to be processed:")
                    print("        "+str(int(sets)-1)+" batchs of "+str(rows_per_batch)+" rows each")
                    print("        1 batch of "+str(last_set_rows)+" rows")
                    print("    The gap between each execution is set to "+str(int(gap))+" seconds")
                else:
                    print("\n  As a result:")
                    print("    "+str(int(sets))+" batchs of "+str(rows_per_batch)+" rows each are going to be processed")
                    print("    The gap between each execution is set to "+str(int(gap))+" seconds")

                confirmation = input("\n\nAre you sure? [yes,no,exit]: ").lower()
                if confirmation == "exit":
                    return
                if confirmation == "yes" or confirmation == "y":
                    confirmation_loop = False
            if total_requested_rows % rows_per_batch != 0:
                for i in range(int(sets)-1):
                    postgres_row_insert_fn("default",rows_per_batch,i+1,int(sets))
                    os.system('clear')
                    print("\n  Waiting "+str(int(gap))+" seconds...")
                    time.sleep(int(gap))
                postgres_row_insert_fn("default",last_set_rows)
            else:
                for i in range(int(sets)):
                    postgres_row_insert_fn("default",rows_per_batch,i+1,int(sets))
                    if (i+1) < int(sets):
                        os.system('clear')
                        print("\n  Waiting "+str(int(gap))+" seconds...")
                        time.sleep(int(gap))
        else:
            os.system('clear')
            print("\nPlease, clean the default tables")
            input("\nPress enter to go back to the menu")
    except:
        SingleLogger().logger.exception("Error while executing batch rows inserts in PostgreSQL", exc_info=True)

