from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger
from datetime import datetime

def mongo_document_update_fn(type:str):
    """This function allows the user to update rows into a PostgreSQL database"""       
    
    try:
        mongo = MongoDB()
        if type == "default":
            collection_default = 'patients'
            collection = mongo.db[collection_default]
            documents_left = collection.count_documents({})
            print("How many documents do you want to update?: ("+str(documents_left)+" documents available)")
            documents_to_update = input()


            if int(documents_to_update) > documents_left:
                print("The number of documents requested exceed the number of documents available.\nAs a result, "+str(documents_left)+" documents will be inserted")
                input("Press enter to continue")
                documents_to_update = documents_left

            id_minimo = int(1)
            id_maximo = int(documents_to_update)
            query_update = {"id_patient": {"$gte": id_minimo, "$lte": id_maximo}}
            update = {"$set": {"name": "Roberts"}}
            mongo.execute_query_update('patients',query_update,update, "Updating collection patients")
            query_update = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
            update = {"$set": {"name": "Mark"}}
            mongo.execute_query_update('doctors',query_update,update, "Updating collection doctors")
            query_update = {"id_medical_record": {"$gte": id_minimo, "$lte": id_maximo}}
            update = {"$set": {"discharge_date": datetime.now().strftime('%Y-%m-%d')}}
            mongo.execute_query_update('medical_records',query_update,update, "Updating collection medical_records")
        else:
            print("Enter your query to update documents: (if a field doesn't apply, press enter)\n")
            print("  Example:")
            print("    db.collectionname")
            print("    update.")
            print('    filter.{"field1": {"$gte": value1, "$lte": value2}}')
            print('    set.{"$set": {"field2": value}}')
            collectionname = input("\n\n  db.")
            print("    update.")
            query_update = input("filter.")
            update = input("set.")
            if not collectionname == "" and not query_update == "" and not update == "":
                MongoDB().execute_query_update(collectionname,query_update,update)
            else:
                print("Some of the inputs are empty...")
                input("")
    except:
        SingleLogger().logger.exception("MongoDB: Error while updating documents", exc_info=True)