from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn
import os

def postgres_row_delete_fn(type:str, requested_rows:int=0, current_iteration:int=0, total_iterations:int=0) -> None:
    """This function allows the user to delete rows in a table"""

    try:
        postgres = PostgreSQL()
        os.system('clear')
        foreign_constraints = "No"
        if type == "default":
            
            actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","Calculating the number of rows in the doctors' table",expected_result=True)[0][0]
            actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","Calculating the number of rows in the patients' table",expected_result=True)[0][0]
            actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","Calculating the number of rows in the medical_records' table",expected_result=True)[0][0]
            actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","Calculating the number of rows in the doctor_medical_records' table",expected_result=True)[0][0]
            
            rows_left = min(actual_doctor_rows,actual_patient_rows,actual_medicalrecord_rows,actual_doctormedicalrecord_rows)

            confirmation_loop = True
            if total_iterations == 0:
                while(confirmation_loop):
                    os.system('clear')
                    print("Row delete\n")
                    print("  How many rows do you want to delete? ("+str(rows_left)+" rows left)\n")
                    rows_to_delete = int(input("\n  Your answer: "))
                    if rows_to_delete <= 0:
                        print("\nThe number of rows per batch must be greater than 0")
                        input("\n\nPress enter to continue")
                        continue
                    else:
                        confirmation_loop = False

                print("\n  Would you like to drop foreign constraints?\n  (this will decrease the time considerably, but the data consistency can be affected)\n")
                foreign_constraints = input("  Your answer (yes/no): ").lower()
                if foreign_constraints == "yes" or foreign_constraints == "y":
                    postgres.run_query("ALTER TABLE medical_records DROP CONSTRAINT IF EXISTS medical_records_id_patient_fkey","Dropping foreign constraint medical_records_id_patient_fkey from table medical_records")
                    postgres.run_query("ALTER TABLE doctor_medical_records DROP CONSTRAINT IF EXISTS doctor_medical_records_id_doctor_fkey","Dropping foreign constraint doctor_medical_records_id_doctor_fkey from table doctor_medical_records")
                    postgres.run_query("ALTER TABLE doctor_medical_records DROP CONSTRAINT IF EXISTS doctor_medical_records_id_medical_record_fkey","Dropping foreign constraint doctor_medical_records_id_medical_record_fkey from table doctor_medical_records")
                    os.system('clear')
                    print("\n  Foreign constraints have been removed.\n  (They will be added back automatically once row deletion has been completed)\n\n")
                    input("  Press enter to continue")

            else:
                rows_to_delete = requested_rows
                print("Batch row deletes")
            
            os.system('clear')
            (lambda current_iteration, total_iterations: print("Doctors - MedicalRecords:") if total_iterations == 0 else print("Doctors - MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(rows_to_delete)+" rows...")
            postgres.run_query("DELETE FROM doctor_medical_records WHERE id_doctor IN ( SELECT id_doctor FROM doctor_medical_records ORDER BY id_medical_record ASC, id_doctor ASC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" relationships between doctors and medical records")
            os.system('clear')
            (lambda current_iteration, total_iterations: print("MedicalRecords:") if total_iterations == 0 else print("MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(rows_to_delete)+" rows...")
            postgres.run_query("DELETE FROM medical_records WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_patient ASC, id_medical_record ASC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" medical records")
            os.system('clear')
            (lambda current_iteration, total_iterations: print("Doctors:") if total_iterations == 0 else print("Doctors:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(rows_to_delete)+" rows...")
            postgres.run_query("DELETE FROM doctors WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor ASC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" doctors")            
            os.system('clear')
            (lambda current_iteration, total_iterations: print("Patients:") if total_iterations == 0 else print("Patients:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(rows_to_delete)+" rows...")
            postgres.run_query("DELETE FROM patients WHERE id_patient IN ( SELECT id_patient FROM patients ORDER BY id_patient ASC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" patients")            
            
            if total_iterations == 0 and (foreign_constraints == "yes" or foreign_constraints == "y"):
                os.system('clear')
                print("Row delete\n")
                postgres.run_query("ALTER TABLE medical_records ADD CONSTRAINT medical_records_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES patients(id_patient)","Adding foreign constraint medical_records_id_patient_fkey to table medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records ADD CONSTRAINT doctor_medical_records_id_doctor_fkey FOREIGN KEY (id_doctor) REFERENCES doctors(id_doctor)","Adding foreign constraint doctor_medical_records_id_doctor_fkey to table doctor_medical_records")
                postgres.run_query("ALTER TABLE doctor_medical_records ADD CONSTRAINT doctor_medical_records_id_medical_record_fkey FOREIGN KEY (id_medical_record) REFERENCES medical_records(id_medical_record)","Adding foreign constraint doctor_medical_records_id_medical_record_fkey to table doctor_medical_records")
                print("\n  Foreign constraints have been added back to the tables\n")
                input("Press enter to continue")           
        else:
            postgres_table_list_fn(enable_interaction=False)
            print("Enter your query to delete rows:\n")
            print("  Example:\n")
            print("    DELETE FROM tablename WHERE condition")
            print("  \n  Your query:\n")
            query = input("    DELETE FROM ")
            if not query.startswith("DELETE FROM") or not query.startswith("delete from"):
                query = "DELETE FROM " + query
            postgres.run_query(query,"Executing custom delete on PostgreSQL")
            print("\nDone!\n")
            print("\nPress enter to continue")
            input()
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while deleting rows", exc_info=True)