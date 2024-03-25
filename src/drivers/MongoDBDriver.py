# from pymongo import MongoClient

# def mongo_connection(db_connection_string, db_name):
#     """This function establishes the connection with Mongo"""
    
#     try:
#         conn = MongoClient(db_connection_string)
#         list_databases = conn.list_database_names()
#         print(list_databases)
#         if not db_name in list_databases:
#             print("The database: \""+db_name+"\" doesn't exist on Mongo. Creating database...")
#             db = conn[db_name]
#             print("Database created")
#             return db
#         db = conn[db_name]
#     except Exception as error:
#         print("Error while connecting to MongoDB:", error)
#     return db
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
    
    # def __init__(self, db_connection_string, logger, db_name):
    #     """This function establishes the connection with MongoDB"""
    #     try:
    #         conn = MongoClient(db_connection_string)
    #         list_databases = conn.list_database_names()
    #         print(list_databases)
    #         if not db_name in list_databases:
    #             logger.info("The database: \""+db_name+"\" doesn't exist on Mongo. Creating database...")
    #             logger.info("Database created")
    #         self.db = conn[db_name]
    #         print("Database "+db_name+" connected")
    #     except Exception as error:
    #         logger.exception("Error while connecting to MongoDB:", error)
    #         sys.exit(1)

    def status(self):
        """This function returns the database name if there is an already established connection"""

        try:
            if hasattr(self, 'conn'):
                return "hospital"
            else:
                return "Disconnected"
        except Exception:
            SingleLogger().logger.exception("Error while getting MongoDB connection status", exc_info=True)
            sys.exit(1)

    def exist(self, db_connection_string, db_name):
        """This function checks whether the database exists or not"""

        try:
            SingleLogger().logger.info("Checking whether database "+db_name+" exist or not...")
            self.connect(db_connection_string, "")
            list_databases = self.conn.list_database_names()
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

            if not self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.db = self.conn[db_name]
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("Database "+db_name+" created")
                self.connect(db_connection_string,db_name)
        except Exception:
            SingleLogger().logger.exception("Error while connecting to MongoDB", exc_info=True)
            sys.exit(1)



    def connect(self, db_connection_string, db_name):
        try:
            SingleLogger().logger.info("Connecting to "+db_connection_string+db_name+" on MongoDB...")
            start_counter = time.time()
            self.conn = MongoClient(db_connection_string)
            stop_counter = time.time()
            SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            SingleLogger().logger.info("Connection with "+db_connection_string+db_name+" has been established")
            self.__connection_string = db_connection_string
        except Exception as error:
            SingleLogger().logger.exception("Error while connecting to "+db_connection_string+db_name+" on MongoDB", exc_info=True)
            sys.exit(1)


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
    
    def drop(self, db_connection_string, db_name):
        """This function drops a MongoDB database"""
        
        try:
            SingleLogger().logger.info("Dropping the database "+db_name+" from MongoDB...")
            if self.exist(db_connection_string, db_name):
                start_counter = time.time()
                # self.cursor.execute('DROP DATABASE IF EXISTS '+db_name)
                self.conn.drop_database(db_name)
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("The database "+db_name+" has been dropped")
            self.close()
        except Exception:
            SingleLogger().logger.exception("Error while dropping database on MongoDB", exc_info=True)
            sys.exit(1)

    def close(self):
        """This function closes the cursor and connection"""

        try:
            if hasattr(self, 'conn'):
                self.conn.close()
            self.__connection_string = None
            SingleLogger().logger.info("Connection closed\n")
        except Exception:
            SingleLogger().logger.exception("Error while closing MongoDB cursor and connection", exc_info=True)
            sys.exit(1)

    @property
    def connection_string(self):
        return self.__connection_string

    @connection_string.setter
    def logger(self, connection_string) -> None:
        self.__connection_string = connection_string