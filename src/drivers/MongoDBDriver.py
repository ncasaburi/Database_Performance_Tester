from src.logger.SingleLogger import SingleLogger
from pymongo import MongoClient
import sys
import time
import zipfile
import os

class MongoDB():
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """This function initialize the MongoDB class"""
            
        pass
    
    def status(self):
        """This function returns the database name if there is an already established connection"""

        try:
            if hasattr(self, 'db'):
                return self.__db_name
            else:
                return "Disconnected"
        except Exception:
            SingleLogger().logger.exception("Error while getting MongoDB connection status", exc_info=True)
            sys.exit(1)

    def exist(self, db_name):
        """This function checks whether the database exists or not"""

        try:
            SingleLogger().logger.info("Checking whether database "+db_name+" exist or not...")
            #self.connect(db_connection_string, "")
            list_databases = self.client.list_database_names()
            if db_name in list_databases:   
                SingleLogger().logger.info("Database "+db_name+" already exists")
                return True
            else:
                SingleLogger().logger.info("Database "+db_name+" doesn't exists")
                return False   
        except Exception:
            SingleLogger().logger.exception("Error while checking MongoDB database existence", exc_info=True)
            sys.exit(1)            

    def create(self, db_connection_string, db_name):
        """This function creates a database on MongoDB"""

        try:
            SingleLogger().logger.info("Creating database "+db_name+" on MongoDB...")

            if not self.exist(db_name):
                start_counter = time.time()
                self.connect(db_connection_string,db_name)
                self.db.create_collection('test')
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("Database "+db_name+" created")

        except Exception:
            SingleLogger().logger.exception("Error while connecting to MongoDB", exc_info=True)
            sys.exit(1)


    def connect(self, db_connection_string, db_name):
        try:
            SingleLogger().logger.info("Connecting to "+db_connection_string+db_name+" on MongoDB...")
            start_counter = time.time()
            self.client = MongoClient(db_connection_string)
            self.db = self.client[db_name]
            stop_counter = time.time()
            SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            SingleLogger().logger.info("Connection with "+db_connection_string+db_name+" has been established")
            self.__connection_string = db_connection_string
            self.__db_name = db_name
        except Exception as error:
            SingleLogger().logger.exception("Error while connecting to "+db_connection_string+db_name+" on MongoDB", exc_info=True)
            sys.exit(1)

    def execute_query_update(self, collection_default, query_update, update):
        try:
            collection = MongoDB().db[collection_default]
            SingleLogger().logger.info("Updating collection: "+collection_default)
            result = collection.update_many(query_update,update)
            SingleLogger().logger.info("Total documents updated: " + str(result.modified_count))
            SingleLogger().logger.info("Query executed successfully.")
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while executing query", exc_info=True)
            return None
        
    def execute_query_delete(self, collection_default, query_delete):
        try:
            collection = MongoDB().db[collection_default]
            SingleLogger().logger.info("Deleting collection: "+collection_default)
            result = collection.delete_many(query_delete)
            SingleLogger().logger.info("Total documents deleted: " + str(result.deleted_count))
            SingleLogger().logger.info("Query executed successfully.")
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while executing query", exc_info=True)
            return None

    def execute_operations_from_file(self, logger ,path, description):
        """Execute MongoDB operations from a file"""
       
        try:
            if not description == "":
                logger.info(description)
            with zipfile.ZipFile(path+'.zip', 'r') as zip_ref:
                file_path = os.path.basename(path+'.js')
                with zip_ref.open(file_path, 'r') as file:
                    start_counter = time.time()
                    for line in file:
                        line = line.decode()
                        self.execute_operation(line)
                    stop_counter = time.time()
                    logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
        except Exception:
            logger.exception("Error while running query from a file to MongoDB", exc_info=True)
            sys.exit(1)       
       

    def execute_operation(self,operation_str):

        # drop spaces
        operation_str = operation_str.strip()
        # split string
        parts = operation_str.split('.')
        # get collection
        collection_name = parts[1]
        # get method
        method = parts[2].split('(')[0]
        # get document
        document_str = ''.join(operation_str.split('(')[1:]).strip(')')
        document = eval(document_str)

        #print("Colección:", collection_name)
        #print("Método:", method)
        #print("Documento:", document)

        col = self.db[collection_name]
        if method == "insertOne":
            col.insert_one(document)
        if method == "insertMany":
            col.insert_many(document)
        return
    
    def drop(self, db_name):
        """This function drops a MongoDB database"""
        
        try:
            SingleLogger().logger.info("Dropping the database "+db_name+" from MongoDB...")
            if self.exist(db_name):
                start_counter = time.time()
                self.client.drop_database(db_name)
                self.__db_name = None
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("The database "+db_name+" has been dropped")
            #self.close()
        except Exception:
            SingleLogger().logger.exception("Error while dropping database on MongoDB", exc_info=True)
            sys.exit(1)

    def close(self):
        """This function closes the cursor and connection"""

        try:
            if hasattr(self, 'client'):
                self.client.close()
            self.__connection_string = None
            SingleLogger().logger.info("Connection closed\n")
        except Exception:
            SingleLogger().logger.exception("Error while closing MongoDB cursor and connection", exc_info=True)
            sys.exit(1)

    def create_collection(self, collection_name):
        try:
            self.db.create_collection(collection_name)
            SingleLogger().logger.info("Collection '{}' created successfully.".format(collection_name))
            return True
        except Exception as error:
            SingleLogger().logger.exception("Error while creating collection '{}'".format(collection_name), exc_info=True)
            return False

    def drop_collection(self, collection_name):
        try:
            self.db.drop_collection(collection_name)
            SingleLogger().logger.info("Collection '{}' droped successfully.".format(collection_name))
            return True
        except Exception as error:
            SingleLogger().logger.exception("Error while droping collection '{}'".format(collection_name), exc_info=True)
            return False

    def exist_collection(self, collection_name):
        """This function checks whether the collection exists or not"""

        try:
            SingleLogger().logger.info("Checking whether collection "+collection_name+" exist or not...")
            collections = self.db.list_collection_names() # Llamar al método para obtener la lista de colecciones
            if collections is not None and collection_name in collections:   
                SingleLogger().logger.info("Collection "+collection_name+" already exists")
                return True
            else:
                SingleLogger().logger.info("Collection "+collection_name+" doesn't exist")
                return False   
        except Exception:
            SingleLogger().logger.exception("Error while checking MongoDB Collection existence", exc_info=True)
            sys.exit(1)

   
    @property
    def connection_string(self):
        return self.__connection_string

    @connection_string.setter
    def logger(self, connection_string) -> None:
        self.__connection_string = connection_string