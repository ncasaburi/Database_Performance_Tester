from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.menu.status import status
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
import os

class SubmenuMongoDocumentInsert():

    def __init__(self) -> None:
        """This function initializes the SubmenuMongoDocumentInsert class"""
        
        #submenu definition
        self.submenu_mongo_document_insert = ConsoleMenu("Mongo Document Inserts", status)
        
        #submenu items
        mongo_document_insert_default = FunctionItem("Insert default documents", self.mongo_document_insert_fn, args=["default"]) 
        mongo_document_insert_custom = FunctionItem("Insert custom documents", self.mongo_document_insert_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_document_insert.append_item(mongo_document_insert_default)
        self.submenu_mongo_document_insert.append_item(mongo_document_insert_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document_insert

    def mongo_document_insert_fn(self, type:str):
        """This function allows the user to insert documents into a MongoDB database"""       
        
        try:
            if type == "default":
                
                default_document_set = int(Config().default_memory["default_document_set"])
                default_number_files = int(Config().default_memory["default_insert_files"])

                documents , actual_doctor_documents = MongoDB().execute_query_find('doctors',{})
                documents , actual_patient_documents = MongoDB().execute_query_find('patients',{})
                documents , actual_medicalrecord_documents = MongoDB().execute_query_find('medical_records',{})
                documents , actual_doctormedicalrecord_documents = MongoDB().execute_query_find('doctor_medical_records',{})

                if actual_doctor_documents == 0 and actual_patient_documents == 0 and actual_medicalrecord_documents == 0 and actual_doctormedicalrecord_documents == 0:
                    Config().default_lines_read = 0
                    Config().default_last_file_read = 0

                documents_left = (default_document_set * default_number_files) - Config().default_lines_read

                #If there are documents left and tables count of documents is the same as the number stored on variable default_lines_read
                if documents_left > 0 and actual_doctor_documents == Config().default_lines_read and actual_patient_documents == Config().default_lines_read and actual_medicalrecord_documents == Config().default_lines_read and actual_doctormedicalrecord_documents == Config().default_lines_read:
                    os.system('clear')
                    print("Please, enter the number of documents you want to insert: ("+str(documents_left)+" documents left)")
                    requested_documents = int(input())

                    if requested_documents > documents_left:
                        print("The number of documents requested exceed the number of documents left.\nAs a result, "+str(documents_left)+" documents will be inserted")
                        input("Press enter to continue")
                        requested_documents = documents_left
                    
                    os.system('clear')
                    print("Doctors:")
                    self._load_mql_content("Doctors", requested_documents, default_document_set, Config().default_lines_read, Config().default_last_file_read)
                    os.system('clear')
                    print("Patients:")
                    self._load_mql_content("Patients", requested_documents, default_document_set, Config().default_lines_read, Config().default_last_file_read)
                    os.system('clear')
                    print("MedicalRecords:")
                    self._load_mql_content("MedicalRecords", requested_documents, default_document_set, Config().default_lines_read, Config().default_last_file_read)
                    os.system('clear')
                    print("Doctors - MedicalRecords:")
                    #(requested_documents, default_document_set,Config().default_lines_read,Config().default_last_file_read) = self._load_mql_content("Doctor_MedicalRecords", requested_documents, default_document_set, Config().default_lines_read, Config().default_last_file_read)
                    self._load_mql_content("Doctor_MedicalRecords", requested_documents, default_document_set, Config().default_lines_read, Config().default_last_file_read)
                else:
                    os.system('clear')
                    print("\nPlease, clean the default collections")
                    input("\nPress enter to go back to the menu")
            else:
                os.system('clear')
                # print("Enter the query to insert the documents: \nExample: INSERT INTO tablename (colname1, colname2, colname3) VALUES ('value1','value2', 'value3');\n")
                # query = input()
                # query = query.lower()
                # if query.startswith("insert into"):
                #     postgres.run_query(query, "Inserting custom documents...")
                # else:
                #     print("\nThe query must begin with INSERT INTO")
                #     input("\nPress enter to go back to the menu")
        except:
            SingleLogger().logger.exception("Error while inserting documents to MongoDB", exc_info=True)

    def _load_mql_content(self, element:str, requested_documents:int, default_document_set:int, default_lines_read, default_last_file_read) -> list:

        current_file_document = default_lines_read - (default_last_file_read* default_document_set)

        content_mql = ""        
        pending_documents = requested_documents

        print("\n  loading data...")
        #While the requested number of documents involves more than one file
        while current_file_document + pending_documents >= default_document_set:
            requested_documents_aux = default_document_set - current_file_document

            #Unzipping and storing documents

            if content_mql == "": #If this is the first iteration
                content_mql = content_mql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","js").splitlines()[current_file_document:default_document_set]))
            else:
                content_mql = content_mql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","js").splitlines()[current_file_document:default_document_set]))
                
            default_lines_read = default_lines_read + requested_documents_aux
            pending_documents = pending_documents - requested_documents_aux
            current_file_document = 0
            default_last_file_read = default_last_file_read + 1

        #If there are still documents pending to be added but they are fewer than the number of documents per file
        if pending_documents > 0:
            max_document_number = pending_documents + current_file_document
            
            #Unzipping and storing documents
            if content_mql == "": #If this is the first iteration
                content_mql = content_mql + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","js").splitlines()[current_file_document:max_document_number]))
            else:
                content_mql = content_mql +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_postgres_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_last_file_read)+".zip","js").splitlines()[current_file_document:max_document_number]))
                
            default_lines_read = default_lines_read + pending_documents
            current_file_document = pending_documents + 1
            pending_documents = 0               
         
        #Inserting documents
        print("  inserting documents...")
        # drop spaces
        content_mql = content_mql.strip()
        # split string
        parts = content_mql.split('.')
        # get collection
        collection_name = parts[1]
        # get method
        method = parts[2].split('(')[0]
        # get document
        document_str = ''.join(content_mql.split('(')[1:]).strip(')')
        document = eval(document_str)
        MongoDB().execute_query_insert(collection_name,document)
        #postgres.run_query(content_mql,"Adding "+str(len(content_mql.splitlines()))+" "+element.lower()+"...")
        return (requested_documents,default_document_set,default_lines_read,default_last_file_read)

