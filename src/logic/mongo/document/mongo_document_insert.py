from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
import os
import re

def mongo_document_insert_fn(type:str, requested_documents:int=0, current_iteration:int=0, total_iterations:int=0):
    """This function allows the user to insert documents into a MongoDB database"""       
    
    try:
        mongo = MongoDB()
        if type == "default":
            default_document_set = int(Config().default_memory["default_insert_set"])
            default_number_files = int(Config().default_memory["default_insert_files"])

            if requested_documents == 0:
                actual_doctor_documents = mongo.count_documents("doctors")
                actual_patient_documents = mongo.count_documents("patients")
                actual_medicalrecord_documents = mongo.count_documents("medical_records")
                actual_doctormedicalrecord_documents = mongo.count_documents("doctor_medical_records")
                if actual_doctor_documents == 0 and actual_patient_documents == 0 and actual_medicalrecord_documents == 0 and actual_doctormedicalrecord_documents == 0:
                    Config().default_mongo_lines_read = 0
                    Config().default_mongo_last_file_read = 1

                documents_left = (default_document_set * default_number_files) - Config().default_mongo_lines_read

            #If there are documents left and tables count of documents is the same as the number stored on variable default_mongo_lines_read
            if (requested_documents > 0) or (documents_left > 0 and actual_doctor_documents == Config().default_mongo_lines_read and actual_patient_documents == Config().default_mongo_lines_read and actual_medicalrecord_documents == Config().default_mongo_lines_read and actual_doctormedicalrecord_documents == Config().default_mongo_lines_read):
                if requested_documents == 0:
                    os.system('clear')
                    print("Please, enter the number of documents you want to insert: ("+str(documents_left)+" documents left)")
                    requested_documents = int(input())

                    if requested_documents > documents_left:
                        print("The number of documents requested exceed the number of documents left.\nAs a result, "+str(documents_left)+" documents will be inserted")
                        input("Press enter to continue")
                        requested_documents = documents_left
                
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Doctors:") if total_iterations == 0 else print("Doctors:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_mql_content("Doctors", requested_documents, default_document_set, Config().default_mongo_lines_read, Config().default_mongo_last_file_read, mongo)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Patients:") if total_iterations == 0 else print("Patients:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_mql_content("Patients", requested_documents, default_document_set, Config().default_mongo_lines_read, Config().default_mongo_last_file_read, mongo)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("MedicalRecords:") if total_iterations == 0 else print("MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                load_mql_content("MedicalRecords", requested_documents, default_document_set, Config().default_mongo_lines_read, Config().default_mongo_last_file_read, mongo)
                os.system('clear')
                (lambda current_iteration, total_iterations: print("Doctors - MedicalRecords:") if total_iterations == 0 else print("Doctors - MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
                (requested_documents, default_document_set,Config().default_mongo_lines_read,Config().default_mongo_last_file_read) = load_mql_content("Doctor_MedicalRecords", requested_documents, default_document_set, Config().default_mongo_lines_read, Config().default_mongo_last_file_read, mongo)
            else:
                os.system('clear')
                print("\nPlease, clean the default collections")
                input("\nPress enter to go back to the menu")
        else:
            os.system('clear')
            print("Enter the query to insert the documents: \n")
            print("\n  Example:")
            print("    db.students.insertMany")
            print("    ([")
            print("    { atribute1: 'value1', atribute2: valuenumber, atribute3: ['value3', 'value4'] }")
            print("    ])")
            print("\n  Your query: (if a field doesn't apply, press enter)")
            collection_name = input("\n\n  db.")
            print("    ([")
            query = input()
            query = query.lower()
            query = query.replace("'", '"')
            print("    ])")
            mongo.execute_query_insert(re.split(r'\.', collection_name)[0],'['+query+']', "Inserting documents into collection: "+re.split(r'\.', collection_name)[0])
                
    except:
        SingleLogger().logger.exception("MongoDB: Error while inserting documents", exc_info=True)

def load_mql_content(element:str, requested_documents:int, default_document_set:int, default_mongo_lines_read, default_mongo_last_file_read, mongo) -> list:

    current_file_document = default_mongo_lines_read - ( ( default_mongo_last_file_read - 1) * default_document_set)
    pending_documents = requested_documents

    content_mongo = ""
    collection_name = ""
    
    print("\n  loading data...")
    #While the requested number of documents involves more than one file
    while current_file_document + pending_documents >= default_document_set:
        requested_documents_aux = default_document_set - current_file_document

        #Unzipping and storing mongodb documents
        if content_mongo == "": #If this is the first iteration

            content_mongo = content_mongo + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[current_file_document:default_document_set+1])).removesuffix("])")
            collection_name = re.search(r'db\.(\w+)\.', '\n'.join(map(str,Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[0:1]))).group(1)
            content_mongo = re.sub(r"db\.\w+\.insertMany\(\[", "", content_mongo)
        else:
            if content_mongo[-1] != ',':
                content_mongo += ','
            content_mongo = content_mongo +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[current_file_document:default_document_set])).removesuffix("])")
            content_mongo = re.sub(r"db\.\w+\.insertMany\(\[", "", content_mongo)

        default_mongo_lines_read = default_mongo_lines_read + requested_documents_aux
        pending_documents = pending_documents - requested_documents_aux
        current_file_document = 0
        default_mongo_last_file_read = default_mongo_last_file_read + 1

    #If there are still documents pending to be added but they are fewer than the number of documents per file
    if pending_documents > 0:
        max_document_number = pending_documents + current_file_document
        
        #Unzipping and storing documents
        if content_mongo == "": #If this is the first iteration
            content_mongo = content_mongo + '\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[current_file_document:max_document_number])).removesuffix("])")
            collection_name = re.search(r'db\.(\w+)\.', '\n'.join(map(str,Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[0:1]))).group(1)
            content_mongo = re.sub(r"db\.\w+\.insertMany\(\[", "", content_mongo)
        else:
            if content_mongo[-1] != ',':
                content_mongo += ','
            content_mongo = content_mongo +'\n'+'\n'.join(map(str, Zipper().unzip_content(Config().default_data["default_mongo_inserts"]+element+os.path.sep+str(default_document_set)+"_"+element.lower()+"_set"+str(default_mongo_last_file_read)+".zip","js").splitlines()[current_file_document:max_document_number])).removesuffix("])")
            content_mongo = re.sub(r"db\.\w+\.insertMany\(\[", "", content_mongo)

        default_mongo_lines_read = default_mongo_lines_read + pending_documents
        current_file_document = pending_documents + 1
        pending_documents = 0

    content_mongo = "[" + content_mongo
    content_mongo = content_mongo.rstrip(',') +'\n]'
    content_mongo = content_mongo.replace("'", '"')

    #Inserting documents
    print("  inserting documents...")
    mongo.execute_query_insert(collection_name,content_mongo,f"Inserting documents into collection: {collection_name}")
    return (requested_documents,default_document_set,default_mongo_lines_read,default_mongo_last_file_read)

