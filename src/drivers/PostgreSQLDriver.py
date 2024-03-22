from src.logger.SingleLogger import SingleLogger
import psycopg2
from tqdm import tqdm
#from psycopg2 import errors
import time
import sys
import zipfile
import os

class PostgreSQL():
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """This function initialize the PostgreSQL class"""
            
        pass

    def status(self):
        """This function returns the database name if there is an already established connection"""

        try:
            if hasattr(self, 'cursor') and self.cursor:
                return self.cursor.connection.get_dsn_parameters()["dbname"]
            else:
                return "Disconnected"
        except Exception:
            SingleLogger().logger.exception("Error while getting PostgreSQL connection status", exc_info=True)
            sys.exit(1)

    def exist(self, db_connection_string, db_name):
        """This function checks whether the database exists or not"""

        try:
            SingleLogger().logger.info("Checking whether database "+db_name+" exist or not...")
            self.connect(db_connection_string, "")
            self.cursor.execute("SELECT datname FROM pg_database")
            databases = self.cursor.fetchall()
            if (db_name,) in databases:
                SingleLogger().logger.info("Database "+db_name+" already exists")
                return True
            else:
                SingleLogger().logger.info("Database "+db_name+" doesn't exists")
                return False   
        except Exception:
            SingleLogger().logger.exception("Error while checking PostgreSQL database existence", exc_info=True)
            sys.exit(1)            

    def create(self, db_connection_string, db_name):
        """This function creates a database on PostgreSQL"""

        try:
            SingleLogger().logger.info("Creating database "+db_name+" on postgreSQL...")
            if hasattr(self, 'cursor') and self.cursor:
                self.close()
            if not self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.cursor.execute('CREATE DATABASE '+db_name)
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("Database "+db_name+" created")
                self.connect(db_connection_string,db_name)
        except Exception:
            SingleLogger().logger.exception("Error while connecting to PostgreSQL", exc_info=True)
            sys.exit(1)

    def connect(self, db_connection_string, db_name):
        """This function establishes a connection with a postgreSQL database"""
        
        try:
            SingleLogger().logger.info("Connecting to "+db_connection_string+db_name+" on postgreSQL...")
            start_counter = time.time()
            self.conn = psycopg2.connect(db_connection_string+db_name)
            stop_counter = time.time()
            self.conn.set_session(autocommit=True)
            self.cursor = self.conn.cursor()
            SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            SingleLogger().logger.info("Connection with "+db_connection_string+db_name+" has been established")
            self.__connection_string = db_connection_string
        except Exception:
            SingleLogger().logger.exception("Error while connecting to "+db_connection_string+db_name+" on PostgreSQL", exc_info=True)
            sys.exit(1)
    
    def drop(self, db_connection_string, db_name):
        """This function drops a postgreSQL database"""
        
        try:
            SingleLogger().logger.info("Dropping the database "+db_name+" from postgreSQL...")
            if self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.cursor.execute('DROP DATABASE IF EXISTS '+db_name)
                stop_counter = time.time()
                SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                SingleLogger().logger.info("The database "+db_name+" has been dropped")
            self.close()
        except Exception:
            SingleLogger().logger.exception("Error while dropping database on PostgreSQL", exc_info=True)
            sys.exit(1)

    def run_query(self, query:str, description:str="", expected_result:bool=False):
        """This function executes a query and prints the description and returns a list with the results"""

        try:
            SingleLogger().logger.info("Executing sql query...")
            if not description == "":
                SingleLogger().logger.info(description)
            start_counter = time.time()
            self.cursor.execute(query)
            stop_counter = time.time()
            SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            SingleLogger().logger.info("The sql query has been executed")
            if expected_result == True and self.cursor.rowcount > 0:
                return self.cursor.fetchall()
        except Exception:
            SingleLogger().logger.exception("Error while running query to PostgreSQL", exc_info=True)
            sys.exit(1)
            
    # def run_query(self, transactions:list, description:str="", expected_result:bool=False):
    #     """This function executes a query and prints the description and returns a list with the results"""

    #     try:
    #         SingleLogger().logger.info("Executing sql query...")
    #         if not description == "":
    #             SingleLogger().logger.info(description)
    #         start_counter = time.time()
    #         with tqdm(total=len(transactions)) as pbar:
    #             for i in range(len(transactions)):
    #                 self.cursor.execute(transactions[i])
    #                 pbar.update(1)
    #         stop_counter = time.time()
    #         SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
    #         SingleLogger().logger.info("The sql query has been executed")
    #         if expected_result == True and self.cursor.rowcount > 0:
    #             return self.cursor.fetchall()
    #     except Exception:
    #         SingleLogger().logger.exception("Error while running query to PostgreSQL", exc_info=True)
    #         sys.exit(1)

    def run_query_from_file(self, path:str, internal:bool, internal_description:str=""):
        """This function executes a query from a sql file and prints the description and returns a list with the results"""

        try:
            (base,extension) = os.path.basename(path)
            if extension != ".sql":
                raise Exception("The file must be sql")
            if not internal_description == "" and internal == True:
                SingleLogger().logger.info(internal_description)
            elif internal == False:
                SingleLogger().logger.info("Executing the sql file "+os.path.basename(path)+"...")
            with open(path, 'r') as file:
                query = file.read()
                start_counter = time.time()
                self.cursor.execute(query)
                stop_counter = time.time()
                print("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                if internal == False:
                    SingleLogger().logger.info("The sql file "+os.path.basename(path)+" has been executed")
            if self.cursor.rowcount > 0:
                return self.cursor.fetchall()
        except:
            SingleLogger().logger.exception("Error while running query from the sql file "+os.path.basename(path)+" to PostgreSQL", exc_info=True)
            sys.exit(1)

    def run_query_from_zip(self, path, internal:bool, internal_description:str=""):
        """This function executes a query from a sql zipped file and prints the description. The sql file must have the same name as the zip. This function returns a list with the resoults"""

        try:
            base,extension = os.path.splitext(path)
            if extension != ".zip":
                raise Exception("The file must be zip")
            if not internal_description == "" and internal == True:
                SingleLogger().logger.info(internal_description)
            elif internal == False:
                SingleLogger().logger.info("Executing the zip file "+os.path.basename(path)+"...")
            with zipfile.ZipFile(path, 'r') as zip_ref:
                path, extension = os.path.splitext(path)
                file_path = os.path.basename(path+'.sql')
                with zip_ref.open(file_path, 'r') as file:
                    query = file.read()
                    start_counter = time.time()
                    self.cursor.execute(query)
                    stop_counter = time.time()
                    SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
                    if internal == False:
                        SingleLogger().logger.info("The zip file "+os.path.basename(path)+" has been executed")
            if self.cursor.rowcount > 0:
                return self.cursor.fetchall()
        except Exception:
            SingleLogger().logger.exception("Error while running query from the zip file "+os.path.basename(path)+" to PostgreSQL", exc_info=True)
            sys.exit(1)

    def close(self):
        """This function closes the cursor and connection"""

        try:
            if hasattr(self, 'cursor'):
                self.cursor.close()
            if hasattr(self, 'conn'):
                self.conn.close()
            self.__connection_string = None
            SingleLogger().logger.info("Connection closed\n")
        except Exception:
            SingleLogger().logger.exception("Error while closing PostgreSQL cursor and connection", exc_info=True)
            sys.exit(1)

    @property
    def connection_string(self):
        return self.__connection_string

    @connection_string.setter
    def logger(self, connection_string) -> None:
        self.__connection_string = connection_string