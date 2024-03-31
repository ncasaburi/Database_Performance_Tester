from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_collection_drop_fn(type:str):
    """This function allows the user to drop a collection"""

    try:
        if type == "default":
            if MongoDB().exist_collection('doctor_medical_records'):
                MongoDB().drop_collection('doctor_medical_records')
            if MongoDB().exist_collection('patients'):
                MongoDB().drop_collection('patients')
            if MongoDB().exist_collection('doctors'):
                MongoDB().drop_collection('doctors')
            if MongoDB().exist_collection('medical_records'):
                MongoDB().drop_collection('medical_records')
        else:
            print("Enter your name collection to drop:\n")
            collectionname = input()            
            MongoDB().drop_collection(collectionname)
    except:
        SingleLogger().logger.exception("MongoDB: Error while dropping collections", exc_info=True)