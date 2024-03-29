from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_collection_list_fn(enable_interaction:bool=True):
    """This function lists the collections"""

    try:
        mongo = MongoDB()
        collections = mongo.db.list_collection_names()
        print("Collections:\n")
        if collections == None:
            print("No Collections found")
            if enable_interaction:
                print("Press enter to continue...")
                input()
                return
        else:
            for collection in collections:
                print(" - "+str(collection)+" (documents: "+str(mongo.count_documents(collection))+", attributes: "+str(len(mongo.get_attribute_names(collection)))+", size: "+str(mongo.collection_space_occupied(collection))+" MB)")
                print("   ("+', '.join(mongo.get_attribute_names(collection))+")")
                print("")
            if enable_interaction:
                print("Press enter to continue...")
                input()
                return
        input()
        return
    except:
        SingleLogger().logger.exception("Error while listing MongoDB collections", exc_info=True)