from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger
import os
import re

def mongo_document_delete_fn(type:str, requested_documents:int=0, current_iteration:int=0, total_iterations:int=0) -> None:
    """This function allows the user to delete documents in a collection"""

    try:
        mongo = MongoDB()
        if type == "default":
            confirmation_loop = True
            if total_iterations == 0:

                actual_doctor_documents = mongo.count_documents("doctors")
                actual_patient_documents = mongo.count_documents("patients")
                actual_medicalrecord_documents = mongo.count_documents("medical_records")
                actual_doctormedicalrecord_documents = mongo.count_documents("doctor_medical_records")

                documents_left = min(actual_doctor_documents, actual_patient_documents, actual_medicalrecord_documents, actual_doctormedicalrecord_documents)

                while(confirmation_loop):
                    os.system('clear')
                    print("Document delete\n")
                    print("  How many documents do you want to delete? ("+str(documents_left)+" documents left)\n")
                    documents_to_delete = int(input("\n  Your answer: "))
                    if documents_to_delete <= 0:
                        print("\nThe number of documents per batch must be greater than 0")
                        input("\n\nPress enter to continue")
                        continue
                    else:
                        confirmation_loop = False
            
            else:
                documents_to_delete = requested_documents
                print("Batch row documents")

            os.system('clear')
            (lambda current_iteration, total_iterations: print("Doctors - MedicalRecords:") if total_iterations == 0 else print("Doctors - MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(documents_to_delete)+" rows...")
            mongo.execute_query_delete("doctor_medical_records",description="Deleting "+str(documents_to_delete)+" relationships between doctors and medical records", limit_number=documents_to_delete)
            os.system('clear')
            (lambda current_iteration, total_iterations: print("MedicalRecords:") if total_iterations == 0 else print("MedicalRecords:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(documents_to_delete)+" rows...")
            mongo.execute_query_delete("medical_records",description="Deleting "+str(documents_to_delete)+" medical records", limit_number=documents_to_delete)
            os.system('clear')
            (lambda current_iteration, total_iterations: print("Doctors:") if total_iterations == 0 else print("Doctors:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(documents_to_delete)+" rows...")
            mongo.execute_query_delete("doctors",description="Deleting "+str(documents_to_delete)+" doctors", limit_number=documents_to_delete)          
            os.system('clear')
            (lambda current_iteration, total_iterations: print("Patients:") if total_iterations == 0 else print("Patients:   (batch "+str(current_iteration)+"/"+str(total_iterations)+")"))(current_iteration, total_iterations)
            print("\n  Deleting "+str(documents_to_delete)+" rows...")
            mongo.execute_query_delete("patients",description="Deleting "+str(documents_to_delete)+" patients", limit_number=documents_to_delete)          
        else:
            os.system('clear')
            print("Enter the query to delete the documents: \n")
            print("\n  Example:")
            print("    db.students.delete_Many")
            print("    { atribute1: 'value1' }")
            print("\n  Your query: (if a field doesn't apply, press enter)")
            collection_name = input("\n\n  db.")
            filter = input("    {")
            filter = filter.lower()
            filter = filter.replace("'", '"')
            if not filter == "" and not filter.startswith("{"):
                filter = "{" + filter
            if not filter == "" and not filter.endswith("}"):
                filter = filter + "}"
            mongo.execute_query_delete(collection_name,dict(filter), "Deleting documents from collection: "+re.split(r'\.', collection_name)[0])
    except:
        SingleLogger().logger.exception("MongoDB: Error while deleting documents", exc_info=True)