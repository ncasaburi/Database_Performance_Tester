from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
from src.logic.mongo.document.mongo_document_insert import mongo_document_insert_fn
import os
import time

def mongo_document_batch_insert_fn():
    """This function allows the user to execute batch document inserts into a MongoDB database"""       
    
    try:
        mongo = MongoDB()
        default_document_set = int(Config().default_memory["default_insert_set"])
        default_number_files = int(Config().default_memory["default_insert_files"])

        actual_doctor_documents = mongo.count_documents("doctors")
        actual_patient_documents = mongo.count_documents("patients")
        actual_medicalrecord_documents = mongo.count_documents("medical_records")
        actual_doctormedicalrecord_documents = mongo.count_documents("doctor_medical_records")
        if actual_doctor_documents == 0 and actual_patient_documents == 0 and actual_medicalrecord_documents == 0 and actual_doctormedicalrecord_documents == 0:
            Config().default_mongo_lines_read = 0
            Config().default_mongo_last_file_read = 1

        documents_left = (default_document_set * default_number_files) - Config().default_mongo_lines_read

        confirmation_loop = True
        #If there are documents left and the number of documents on each collection is the same as the number stored on default_mongo_lines_read
        if documents_left > 0 and actual_doctor_documents == Config().default_mongo_lines_read and actual_patient_documents == Config().default_mongo_lines_read and actual_medicalrecord_documents == Config().default_mongo_lines_read and actual_doctormedicalrecord_documents == Config().default_mongo_lines_read:
            while(confirmation_loop):
                os.system('clear')

                print("Batch document inserts     ("+str(documents_left)+" documents left)\n")
                
                total_requested_documents = int(input("  Total number of documents you want to insert: "))               
                documents_per_batch = int(input("  Number of documents you want to insert per batch: "))
                gap = float(input("  Gap between batch inserts (in seconds): "))

                if total_requested_documents > documents_left:
                    print("\nThe total number of documents to be inserted can't be greater than the number of documents left")
                    input("\n\nPress enter to continue...")
                    continue

                if total_requested_documents == 0:
                    print("\nThe total number of documents to be inserted must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue
                
                if documents_per_batch == 0:
                    print("\nThe number of documents per batch must be greater than 0")
                    input("\n\nPress enter to continue...")
                    continue

                if gap == 0:
                    print("\nThe gap between batch inserts must be greater than 0 seconds")
                    input("\n\nPress enter to continue...")
                    continue
                    
                if documents_per_batch > total_requested_documents:
                    print("\nThe total number of documents requested must be greater than the number of documents per batch")
                    input("\n\nPress enter to continue...")
                    continue

                sets = total_requested_documents / documents_per_batch
                if total_requested_documents % documents_per_batch != 0:
                    last_set_documents = total_requested_documents - (documents_per_batch * int(set))
                    sets = sets + 1
                    print("\n  As a result:")
                    print("    "+str(int(sets))+" batchs are going to be processed:")
                    print("        "+str(int(sets)-1)+" batchs of "+str(documents_per_batch)+" documents each")
                    print("        1 batch of "+str(last_set_documents)+" documents")
                    print("    The gap between each execution is set to "+str(int(gap))+" seconds")
                else:
                    print("\n  As a result:")
                    print("    "+str(int(sets))+" batchs of "+str(documents_per_batch)+" documents each are going to be processed")
                    print("    The gap between each execution is set to "+str(int(gap))+" seconds")

                confirmation = input("\n\nAre you sure? [yes,no,exit]: ").lower()
                if confirmation == "exit":
                    return
                if confirmation == "yes" or confirmation == "y":
                    confirmation_loop = False
            if total_requested_documents % documents_per_batch != 0:
                for i in range(int(sets)-1):
                    mongo_document_insert_fn("default",documents_per_batch,i+1,int(sets))
                    os.system('clear')
                    print("\n  Waiting "+str(int(gap))+" seconds...")
                    time.sleep(int(gap))
                mongo_document_insert_fn("default",last_set_documents)
            else:
                for i in range(int(sets)):
                    mongo_document_insert_fn("default",documents_per_batch,i+1,int(sets))
                    if (i+1) < int(sets):
                        os.system('clear')
                        print("\n  Waiting "+str(int(gap))+" seconds...")
                        time.sleep(int(gap))
        else:
            os.system('clear')
            print("\nPlease, clean the default collections")
            input("\nPress enter to go back to the menu")
    except:
        SingleLogger().logger.exception("MongoDB: Error while executing batch document inserts", exc_info=True)

