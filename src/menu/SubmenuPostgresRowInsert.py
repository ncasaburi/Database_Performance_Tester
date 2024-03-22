from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
import os

class SubmenuPostgresRowInsert():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowInsert class"""
        
        #submenu definition
        self.submenu_postgres_row_insert = ConsoleMenu("PostgreSQL Row Inserts", status)
        
        #submenu items
        postgres_row_insert_default = FunctionItem("Insert default rows", self.postgres_row_insert_fn, args=["default"]) 
        postgres_row_insert_custom = FunctionItem("Insert custom rows", self.postgres_row_insert_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_insert.append_item(postgres_row_insert_default)
        self.submenu_postgres_row_insert.append_item(postgres_row_insert_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_insert
    
    def postgres_row_insert_fn(self, type:str):
        """This function allows the user to insert rows into a PostgreSQL database"""       
        try:
            postgres = PostgreSQL()
            if type == "default":
                if Config().default_sql_doctors == "":
                    Config().default_sql_doctors = self._join_sql_row_inserts(Config().default_data["default_postgres_inserts"]+"Doctors"+os.path.sep+Config().default_memory["default_row_set"]+"_doctors_set",Config().default_memory["default_insert_files"])
                if Config().default_sql_patients == "":
                    Config().default_sql_patients = self._join_sql_row_inserts(Config().default_data["default_postgres_inserts"]+"Patients"+os.path.sep+Config().default_memory["default_row_set"]+"_patients_set",Config().default_memory["default_insert_files"])
                if Config().default_sql_medicalrecords == "":
                    Config().default_sql_medicalrecords = self._join_sql_row_inserts(Config().default_data["default_postgres_inserts"]+"MedicalRecords"+os.path.sep+Config().default_memory["default_row_set"]+"_medicalrecords_set",Config().default_memory["default_insert_files"])
                if Config().default_sql_doctor_medicalrecords == "":
                    Config().default_sql_doctor_medicalrecords = self._join_sql_row_inserts(Config().default_data["default_postgres_inserts"]+"Doctor_MedicalRecords"+os.path.sep+Config().default_memory["default_row_set"]+"_doctor_medicalrecords_set",Config().default_memory["default_insert_files"])
                
                actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0]
                actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","",expected_result=True)[0][0]
                actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","",expected_result=True)[0][0]
                actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","",expected_result=True)[0][0]
                if actual_doctor_rows == 0 and actual_patient_rows == 0 and actual_medicalrecord_rows == 0 and actual_doctormedicalrecord_rows == 0:
                    Config().default_lines_read = 0
                total_rows = int(Config().default_memory["default_insert_files"]) * int(Config().default_memory["default_row_set"])
                rows_left = total_rows-int(Config().default_lines_read)
                print("rows_left: "+str(rows_left))
                print("default_lines: "+str(Config().default_lines_read))
                if rows_left > 0 and actual_doctor_rows == Config().default_lines_read and actual_patient_rows == Config().default_lines_read and actual_medicalrecord_rows == Config().default_lines_read and actual_doctormedicalrecord_rows == Config().default_lines_read:
                    os.system('clear')
                    print("Please, enter the number of rows you want to insert: ("+str(rows_left)+" default rows left)")
                    requested_rows = int(input())
                    limit = int(Config().default_lines_read) + requested_rows
                    if requested_rows > rows_left:
                        print("The number of rows requested exceed the number of rows left")
                        print("As a result, "+str(rows_left)+" rows will be inserted")
                        limit = int(Config().default_lines_read)+rows_left
                        requested_rows = rows_left
                    postgres.run_query(' '.join(map(str, Config().default_sql_doctors[int(Config().default_lines_read)+1:limit+1])),"Adding "+str(requested_rows)+" doctors...")
                    postgres.run_query(' '.join(map(str, Config().default_sql_patients[int(Config().default_lines_read)+1:limit+1])),"Adding "+str(requested_rows)+" patients...")
                    postgres.run_query(' '.join(map(str, Config().default_sql_medicalrecords[int(Config().default_lines_read)+1:limit+1])),"Adding "+str(requested_rows)+" medical records...")
                    postgres.run_query(' '.join(map(str, Config().default_sql_doctor_medicalrecords[int(Config().default_lines_read)+1:limit+1])),"Adding "+str(requested_rows)+" relationships between doctors and medical records...")
                    Config().default_lines_read = limit
                else:
                    os.system('clear')
                    print("\nPlease clean the default tables")
            else:
                os.system('clear')
                print("Enter the query to insert the rows: \nExample: INSERT INTO tablename (colname1, colname2, colname3) VALUES ('value1','value2', 'value3');\n")
                query = input()
                query = query.lower()
                if query.startswith("insert into"):
                    postgres.run_query(query, "Inserting custom rows...")
                else:
                    print("\nThe query must begin with INSERT INTO")
            print("\nPress enter to go back to the menu")
            input()
        except:
            SingleLogger().logger.exception("Error while inserting default rows to PostgreSQL", exc_info=True)
    
    def _join_sql_row_inserts(self, filepath:str, number_of_files:int) -> str:
        """This function joins all files of the same type into one string variable"""
        
        draft_rows_inserts = ""
        for i in range(int(number_of_files)):
                draft_rows_inserts = draft_rows_inserts+"\n"+Zipper().unzip_content(filepath+str(i)+".zip","sql")
        return draft_rows_inserts.splitlines()