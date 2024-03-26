from consolemenu import *
from consolemenu.items import *
from src.drivers.PostgreSQLDriver import PostgreSQL
from src.config.Config import Config
from src.menu.status import status
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
import os

class SubmenuMongoDocumentInsert():

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
                default_row_set = int(Config().default_memory["default_row_set"])
                default_number_files = int(Config().default_memory["default_insert_files"])

                actual_doctor_rows = postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0]
                actual_patient_rows = postgres.run_query("SELECT COUNT(*) FROM patients","",expected_result=True)[0][0]
                actual_medicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM medical_records","",expected_result=True)[0][0]
                actual_doctormedicalrecord_rows = postgres.run_query("SELECT COUNT(*) FROM doctor_medical_records","",expected_result=True)[0][0]
                if actual_doctor_rows == 0 and actual_patient_rows == 0 and actual_medicalrecord_rows == 0 and actual_doctormedicalrecord_rows == 0:
                    Config().default_lines_read = 0
                    Config().default_last_file_read = 0

                rows_left = (default_row_set * default_number_files) - Config().default_lines_read

                #If there are rows left and tables count of rows is the same as the number stored on variable default_lines_read
                if rows_left > 0 and actual_doctor_rows == Config().default_lines_read and actual_patient_rows == Config().default_lines_read and actual_medicalrecord_rows == Config().default_lines_read and actual_doctormedicalrecord_rows == Config().default_lines_read:
                    os.system('clear')
                    print("Please, enter the number of rows you want to insert: ("+str(rows_left)+" rows left)")
                    requested_rows = int(input())

                    if requested_rows > rows_left:
                        print("The number of rows requested exceed the number of rows left.\nAs a result, "+str(rows_left)+" rows will be inserted")
                        input("Press enter to continue")
                        requested_rows = rows_left
                    
                    os.system('clear')
                    print("Doctors:")
                    self._load_sql_content("Doctors", requested_rows, default_row_set, Config().default_lines_read, Config().default_last_file_read, postgres)
                    os.system('clear')
                    print("Patients:")
                    self._load_sql_content("Patients", requested_rows, default_row_set, Config().default_lines_read, Config().default_last_file_read, postgres)
                    os.system('clear')
                    print("MedicalRecords:")
                    self._load_sql_content("MedicalRecords", requested_rows, default_row_set, Config().default_lines_read, Config().default_last_file_read, postgres)
                    os.system('clear')
                    print("Doctors - MedicalRecords:")
                    (requested_rows, default_row_set,Config().default_lines_read,Config().default_last_file_read) = self._load_sql_content("Doctor_MedicalRecords", requested_rows, default_row_set, Config().default_lines_read, Config().default_last_file_read, postgres)
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
                    postgres.run_query(query, "Inserting custom rows...")
                else:
                    print("\nThe query must begin with INSERT INTO")
                    input("\nPress enter to go back to the menu")
        except:
            SingleLogger().logger.exception("Error while inserting rows to PostgreSQL", exc_info=True)

    def _load_sql_content(self, element:str, requested_rows:int, default_row_set:int, default_lines_read, default_last_file_read, postgres) -> list:

        current_file_row = default_lines_read - (default_last_file_read* default_row_set)
                
        content_sql = ""        
        pending_rows = requested_rows

        print("\n  loading data...")
        #While the requested number of rows involves more than one file
        while current_file_row + pending_rows >= default_row_set:
            requested_rows_aux = default_row_set - current_file_row

            #Unzipping and storing rows
            if content_sql == "": #If this is the first iteration
                content_sql = content_sql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_row_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","sql").splitlines()[current_file_row:default_row_set]))
            else:
                content_sql = content_sql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_row_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","sql").splitlines()[current_file_row:default_row_set]))
                
            default_lines_read = default_lines_read + requested_rows_aux
            pending_rows = pending_rows - requested_rows_aux
            current_file_row = 0
            default_last_file_read = default_last_file_read + 1

        #If there are still rows pending to be added but they are fewer than the number of rows per file
        if pending_rows > 0:
            max_row_number = pending_rows + current_file_row
            
            #Unzipping and storing rows
            if content_sql == "": #If this is the first iteration
                content_sql = content_sql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_row_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","sql").splitlines()[current_file_row:max_row_number]))
            else:
                content_sql = content_sql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_row_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","sql").splitlines()[current_file_row:max_row_number]))
                
            default_lines_read = default_lines_read + pending_rows
            current_file_row = pending_rows + 1
            pending_rows = 0                
        #Inserting rows
        print("  inserting rows...")
        postgres.run_query(content_sql,"Adding "+str(len(content_sql.splitlines()))+" "+element.lower()+"...")
        return (requested_rows,default_row_set,default_lines_read,default_last_file_read)

