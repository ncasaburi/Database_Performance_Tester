from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.row.postgres_row_delete import postgres_row_delete_fn
import time
import os

def postgres_row_batch_delete_fn() -> None:
    """This function allows the user to execute batch row deletes into a PostgreSQL database"""

    try:
        postgres = PostgreSQL()
        
        print("Batch row deletes\n")

        actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","Calculating the number of rows in the doctors' table",expected_result=True)[0][0]
        actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","Calculating the number of rows in the patients' table",expected_result=True)[0][0]
        actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","Calculating the number of rows in the medical_records' table",expected_result=True)[0][0]
        actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","Calculating the number of rows in the doctor_medical_records' table",expected_result=True)[0][0]
        
        rows_left = min(actual_doctor_rows,actual_patient_rows,actual_medicalrecord_rows,actual_doctormedicalrecord_rows)
        
        confirmation_loop = True
        if rows_left > 0:
            while(confirmation_loop):
                os.system('clear')

                print("Batch row deletes     ("+str(rows_left)+" rows left)\n")
                
                total_requested_rows = int(input("  Total number of rows you want to delete: "))               
                rows_per_batch = int(input("  Number of rows you want to delete per batch: "))
                gap = float(input("  Gap between batch deletes (in seconds): "))

                if total_requested_rows > rows_left:
                    print("\nThe total number of rows to be deleted can't be greater than the number of rows left")
                    input("\n\nPress enter to continue...")
                    continue

                if total_requested_rows == 0:
                    print("\nThe total number of rows to be deleted must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue
                
                if rows_per_batch == 0:
                    print("\nThe number of rows per batch must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue

                if gap == 0:
                    print("\nThe gap between batch deletes must be greater than 0 seconds")
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
            os.system('clear')
            print("Batch row deletes")
            print("\n  Would you like to drop foreign constraints?\n  (this will decrease the time considerably, but the data consistency can be affected)\n")
            foreign_constraints = input("  Your answer (yes/no): ").lower()
            if foreign_constraints == "yes" or foreign_constraints == "y":
                postgres.run_query("ALTER TABLE medical_records DROP CONSTRAINT IF EXISTS medical_records_id_patient_fkey","Dropping foreign constraint medical_records_id_patient_fkey from table medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records DROP CONSTRAINT IF EXISTS doctor_medical_records_id_doctor_fkey","Dropping foreign constraint doctor_medical_records_id_doctor_fkey from table doctor_medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records DROP CONSTRAINT IF EXISTS doctor_medical_records_id_medical_record_fkey","Dropping foreign constraint doctor_medical_records_id_medical_record_fkey from table doctor_medical_records")
                os.system('clear')
                print("\n  Foreign constraints have been removed.\n  (They will be added back automatically once row deletion has been completed)\n\n")
                input("  Press enter to continue")

            if total_requested_rows % rows_per_batch != 0:
                for i in range(int(sets)-1):
                    postgres_row_delete_fn("default",rows_per_batch,i+1,int(sets))
                    os.system('clear')
                    print("\n  Waiting "+str(int(gap))+" seconds...")
                    time.sleep(int(gap))
                postgres_row_delete_fn("default",last_set_rows)
            else:
                for i in range(int(sets)):
                    postgres_row_delete_fn("default",rows_per_batch,i+1,int(sets))
                    if (i+1) < int(sets):
                        os.system('clear')
                        print("\n  Waiting "+str(int(gap))+" seconds...")
                        time.sleep(int(gap))
            if foreign_constraints == "yes" or foreign_constraints == "y":
                os.system('clear')
                print("Batch row deletes")
                postgres.run_query("ALTER TABLE medical_records ADD CONSTRAINT medical_records_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES patients(id_patient)","Adding foreign constraint medical_records_id_patient_fkey to table medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records ADD CONSTRAINT doctor_medical_records_id_doctor_fkey FOREIGN KEY (id_doctor) REFERENCES doctors(id_doctor)","Adding foreign constraint doctor_medical_records_id_doctor_fkey to table doctor_medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records ADD CONSTRAINT doctor_medical_records_id_medical_record_fkey FOREIGN KEY (id_medical_record) REFERENCES medical_records(id_medical_record)","Adding foreign constraint doctor_medical_records_id_medical_record_fkey to table doctor_medical_records")
                print("\n  Foreign constraints have been added back to the tables\n")
                input("Press enter to continue")  
        else:
            os.system('clear')
            print("\nPlease, populate the default tables")
            input("\nPress enter to go back to the menu")
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while executing batch rows deletes", exc_info=True)