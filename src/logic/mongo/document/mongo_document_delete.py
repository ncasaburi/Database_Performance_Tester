from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_document_delete_fn(type:str) -> None:
    """This function allows the user to delete rows ina a table"""

    try:
        if type == "default":
            collection_default = 'doctor_medical_records'
            collection = MongoDB().db[collection_default]
            documents_left = collection.count_documents({})
            print("How many documents do you want to delete?: ("+str(documents_left)+" documents available)")
            documents_to_delete = input()
            if int(documents_to_delete) > documents_left:
                print("The number of documents requested exceed the number of documents available.\nAs a result, "+str(documents_left)+" documents will be inserted")
                input("Press enter to continue")
                documents_to_delete = documents_left

            id_minimo = int(1)
            id_maximo = int(documents_to_delete)
            query_delete = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('doctor_medical_records',query_delete)
            query_delete = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('doctors',query_delete)
            query_delete = {"id_patient": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('patients',query_delete)
            query_delete = {"id_medical_record": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('medical_records',query_delete)
        else:
            print("Enter your query to delete documents: (if a field doesn't apply, press enter)\n")
            print("  Example:")
            print("    db.collectionname")
            print("    delete")
            print('    filter.{"field1": {"$gte": value1, "$lte": value2}}')
            collectionname = input("\n\n  db.")
            print("    delete")
            query_update = input("filter.")
            if not collectionname == "" and not query_update == "":
                MongoDB().execute_query_delete(collectionname,query_update)
            else:
                print("Some of the inputs are empty...")
                input("")
    except:
        SingleLogger().logger.exception("Error while deleting documents to MongoDB", exc_info=True)