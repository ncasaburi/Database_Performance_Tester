from pymongo import MongoClient

def mongo_connection(db_connection_string, db_name):
    """This function establishes the connection with Mongo"""
    
    try:
        conn = MongoClient(db_connection_string)
        list_databases = conn.list_database_names()
        print(list_databases)
        if not db_name in list_databases:
            print("The database: \""+db_name+"\" doesn't exist on Mongo. Creating database...")
            db = conn[db_name]
            print("Database created")
            return db
        db = conn[db_name]
    except Exception as error:
        print("Error while connecting to MongoDB:", error)
    return db
