from src.logger.SingleLogger import SingleLogger
from pymongo import MongoClient
import sys
import time
import json
import ast

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
                return self.db.name
            else:
                return "Disconnected"
        except Exception:
            SingleLogger().logger.exception("Error while getting MongoDB connection status", exc_info=True)
            sys.exit(1)

    def exist(self, db_connection_string, db_name):
        """This function checks whether the database exists or not"""

        try:
            if not db_name == "":
                SingleLogger().logger.info("Checking Mongo database "+db_name+" existence...")
                client_temp = MongoClient(db_connection_string)
                list_databases = client_temp.list_database_names()
                if db_name in list_databases:   
                    SingleLogger().logger.info("Mongo database "+db_name+" already exists")
                    client_temp.close()
                    del client_temp
                    return True
                else:
                    SingleLogger().logger.info("Mongo database "+db_name+" doesn't exists")
                    return False
            else:
                try:
                    client_temp = MongoClient(db_connection_string)
                    client_temp.close()
                    del client_temp
                    return True
                except Exception:
                    SingleLogger().logger.info("The connection with "+db_connection_string+" couldn't be established")
                    return False    
        except Exception:
            SingleLogger().logger.info("Mongo database "+db_name+" doesn't exists")
            return False          

    def create(self, db_connection_string, db_name):
        """This function creates a database on MongoDB"""

        try:
            SingleLogger().logger.info("Creating database "+db_name+" on MongoDB...")
            self.close()
            if not self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.connect(db_connection_string,db_name)
                self.create_collection("test")
                stop_counter = time.time()
                server_status = self.db.command('serverStatus')
                resident_memory_mb = server_status['mem']['resident']
                virtual_memory_mb = server_status['mem']['virtual']
                SingleLogger().logger.info("Database "+db_name+" created")
                SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")    
        except Exception:
            SingleLogger().logger.exception("Error while connecting to MongoDB", exc_info=True)
            sys.exit(1)

    def connect(self, db_connection_string, db_name):
        """This function establishes a connection with a MongoDB database"""

        try:
            self.close()
            if self.exist(db_connection_string, db_name):
                SingleLogger().logger.info("Connecting to "+db_connection_string+db_name+" on MongoDB...")
                start_counter = time.time()
                self.client = MongoClient(db_connection_string)
                self.db = self.client[db_name]
                stop_counter = time.time()
                server_status = self.db.command('serverStatus')
                resident_memory_mb = server_status['mem']['resident']
                virtual_memory_mb = server_status['mem']['virtual']
                SingleLogger().logger.info("Connection with "+db_connection_string+db_name+" has been established")
                SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
                self.__connection_string = db_connection_string
        except Exception as error:
            SingleLogger().logger.exception("Error while connecting to "+db_connection_string+db_name+" on MongoDB", exc_info=True)
            sys.exit(1)

    def execute_query_update(self, collection_name, query_update, update):
        """This function updates documents on a MongoDB collection"""

        try:
            collection = self.db[collection_name]
            SingleLogger().logger.info("Updating documents in collection: "+collection_name)
            start_counter = time.time()
            result = collection.update_many(query_update,update)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Total documents updated: " + str(result.modified_count))
            SingleLogger().logger.info("Query executed successfully.")
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while updating documents on MongoBD", exc_info=True)
            return None
        
    def execute_query_delete(self, collection_name, query_delete):
        """This function deletes documents from a MongoDB collection"""

        try:
            collection = self.db[collection_name]
            SingleLogger().logger.info("Deleting documents in collection: "+collection_name)
            start_counter = time.time()
            result = collection.delete_many(query_delete)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Total documents deleted: " + str(result.deleted_count))
            SingleLogger().logger.info("Query executed successfully.")
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while deleting documents on MongoDB", exc_info=True)
            return None

    def execute_query_find(self, collection_name, query:dict):
        """This function executy a query to find documents"""

        try:
            collection = self.db[collection_name]
            SingleLogger().logger.info("Executing find in collection: " + collection_name)
            start_counter = time.time()
            result = collection.find(query)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Number of documents found " + str(self.count_documents(collection_name)))
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            return list(result)
        except Exception as error:
            SingleLogger().logger.exception("Error while executing find query", exc_info=True)
            return None

    def execute_query_insert(self, collection_name:str, query_insert:str):
        """This function inserts documents into a MongoDB collection"""

        try:           
            SingleLogger().logger.info("Inserting documents into collection: "+collection_name+" on MongoDB...")
            collection = self.db[collection_name]
            documents = json.loads(query_insert)
            start_counter = time.time()
            result = collection.insert_many(documents)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Number of documents inserted: " + str(len(result.inserted_ids)))            
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while inserting documents on MongoDB", exc_info=True)
            sys.exit(1)

    def execute_aggregate(self, collection_name,pipeline):
        """This function performs an aggregation of documents on a MongoDB collection"""

        try:
            SingleLogger().logger.info("Executing aggregate on collection: "+collection_name+" on MongoDB...")
            collection = self.db[collection_name]
            start_counter = time.time()
            result = collection.aggregate(pipeline)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Aggregation executed successfully.")
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            return list(result)
        except Exception as error:
            SingleLogger().logger.exception("Error while performing aggregation of documents on MongoDB", exc_info=True)
            sys.exit(1)
    
    def create_index(self, collection_name, index):
        """This function creates an index on a MongoDB collection"""    

        try:
            SingleLogger().logger.info("Creating index on collection: "+collection_name+" on MongoDB...")
            collection = self.db[collection_name]
            start_counter = time.time()
            collection.create_index(index)
            stop_counter = time.time()
            server_status = self.db.command('serverStatus')
            resident_memory_mb = server_status['mem']['resident']
            virtual_memory_mb = server_status['mem']['virtual']
            SingleLogger().logger.info("Index creation executed successfully.")
            SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
        except Exception as error:
            SingleLogger().logger.exception("Error while creating an index on a MongoDB collection", exc_info=True)
            sys.exit(1)

        
    def count_documents(self, collection_name:str, filter={}):
        """This function counts the number of documents from a MongoDB collection"""

        try:
            collection = self.db[collection_name]
            result = collection.count_documents(filter)
            return result
        except Exception as error:
            SingleLogger().logger.exception("Error while counting documents on MongoDB", exc_info=True)
            sys.exit(1)

    def drop(self, db_name):
        """This function drops a MongoDB database"""
        
        try:
            SingleLogger().logger.info("Dropping the database "+db_name+" from MongoDB...")
            if self.exist(db_name):
                start_counter = time.time()
                self.client.drop_database(db_name)
                stop_counter = time.time()
                server_status = self.db.command('serverStatus')
                resident_memory_mb = server_status['mem']['resident']
                virtual_memory_mb = server_status['mem']['virtual']
                SingleLogger().logger.info("The database "+db_name+" has been dropped")
                SingleLogger().logger.info(f"Elapsed time: {round(stop_counter - start_counter, 3)} seconds, Resident memory: {resident_memory_mb} MB, Virtual memory: {virtual_memory_mb} MB")
            self.close()
        except Exception:
            SingleLogger().logger.exception("Error while dropping database on MongoDB", exc_info=True)
            sys.exit(1)

    def close(self):
        """This function closes the cursor and connection"""

        try:
            if hasattr(self, 'client'):
                self.client.close()
                del self.client
            if hasattr(self, 'db'):
                del self.db
            self.__connection_string = None
            SingleLogger().logger.info("Connection closed")
        except Exception:
            SingleLogger().logger.exception("Error while closing MongoDB cursor and connection", exc_info=True)
            sys.exit(1)

    def create_collection(self, collection_name):
        """This function creates a collection"""
        
        try:
            self.db.create_collection(collection_name)
            SingleLogger().logger.info("Collection "+collection_name+" created successfully.")
            return True
        except Exception as error:
            SingleLogger().logger.exception("Error while creating "+collection_name+" collection on MongoDB", exc_info=True)
            return False

    def drop_collection(self, collection_name):
        """This function drops a collection"""

        try:
            self.db.drop_collection(collection_name)
            SingleLogger().logger.info("Collection "+collection_name+" dropped successfully.")
            return True
        except Exception as error:
            SingleLogger().logger.exception("Error while dropping the collection "+collection_name+" on MongoDB", exc_info=True)
            return False

    def exist_collection(self, collection_name):
        """This function checks whether the collection exists or not"""

        try:
            SingleLogger().logger.info("Checking collection "+collection_name+" existence...")
            collections = self.db.list_collection_names() # Llamar al método para obtener la lista de colecciones
            if collections is not None and collection_name in collections:   
                SingleLogger().logger.info("Collection "+collection_name+" already exists")
                return True
            else:
                SingleLogger().logger.info("Collection "+collection_name+" doesn't exist")
                return False   
        except Exception:
            SingleLogger().logger.exception("Error while checking MongoDB collection existence", exc_info=True)
            sys.exit(1)

    def collection_space_occupied(self, collection_name):
        """This function returns the space occupied by a collection in MB"""

        try:
            storage_size = self.db.command("collStats", collection_name)["storageSize"]
            return round( storage_size / (1024 * 1024), 3)
        except Exception:
            SingleLogger().logger.exception("Error while getting space occupied by the collection: "+str(collection_name), exc_info=True)
            sys.exit(1)

    def get_attribute_names(self, collection_name):
        """This function returns the attributes names of a collection"""

        try:
            collection = self.db[collection_name]
            sample_document = collection.find_one()
            if sample_document:
                return list(sample_document.keys())
            else:
                return []
        except Exception:
            SingleLogger().logger.exception("Error while getting the attribute names of the collection: "+str(collection_name), exc_info=True)
            sys.exit(1)

    @property
    def connection_string(self):
        return self.__connection_string

    @connection_string.setter
    def logger(self, connection_string) -> None:
        self.__connection_string = connection_string