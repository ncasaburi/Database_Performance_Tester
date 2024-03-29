from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_collection_list_fn():
    """This function lists the collections"""

    try:
        collections = MongoDB().db.list_collection_names()
        print("Collections:\n")
        if collections == None:
            print("No Collections found")
        else:
            for collection in collections:
                print(collection+"\n")
        input()
        return
    except:
        SingleLogger().logger.exception("Error while listing MongoDB collections", exc_info=True)