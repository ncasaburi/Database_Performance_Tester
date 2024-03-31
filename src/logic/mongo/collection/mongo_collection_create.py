from src.drivers.MongoDBDriver import MongoDB   
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger


def mongo_collection_create_fn(type:str):
    """This function allows the user to create a table"""
    try:
        if type == "default":
            # if MongoDB().status() == Config().default_dbs["default_database_name"]:
            if not MongoDB().exist_collection('patients'):
                MongoDB().create_collection('patients')

            if not MongoDB().exist_collection('doctors'):    
                MongoDB().create_collection('doctors')
            
            if not MongoDB().exist_collection('doctor_medical_records'):
                MongoDB().create_collection('doctor_medical_records')

            if not MongoDB().exist_collection('medical_records'):
                MongoDB().create_collection('medical_records')
            # else:
            #     SingleLogger().logger.info("Not exists default database ...")   

        else:
            print("Enter the collection name to create\n");
            collectionname = input()
            collectionname = collectionname.lower()
            if not MongoDB().exist_collection(collectionname):
                MongoDB().create_collection(collectionname)

    except:
        SingleLogger().logger.exception("MongoDB: Error while creating collections", exc_info=True)
