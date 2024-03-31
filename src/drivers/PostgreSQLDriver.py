from src.logger.SingleLogger import SingleLogger
from psycopg2 import extensions
import psycopg2
import time
import sys
import re
import tempfile

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
            SingleLogger().logger.exception("PostgreSQL: Error while getting connection status", exc_info=True)
            sys.exit(1)

    def exist(self, db_connection_string, db_name):
        """This function checks whether the database exists or not"""

        try:
            if not db_name == "":
                SingleLogger().logger.info("PostgreSQL: Checking database "+db_name+" existence")
                conn_temp = psycopg2.connect(db_connection_string+db_name)
                cursor_temp = conn_temp.cursor()
                cursor_temp.execute("SELECT datname FROM pg_database")
                databases = cursor_temp.fetchall()
                if (db_name,) in databases:
                    SingleLogger().logger.info("PostgreSQL: Database "+db_name+" already exists")
                    cursor_temp.close()
                    del cursor_temp
                    conn_temp.close()
                    del conn_temp
                    return True
                else:
                    SingleLogger().logger.info("PostgreSQL: Database "+db_name+" doesn't exists")
                    return False
            else:
                try:
                    conn_temp = psycopg2.connect(db_connection_string)
                    conn_temp.close()
                    del conn_temp
                    return True
                except Exception:
                    SingleLogger().logger.info("PostgreSQL: The connection with "+db_connection_string+" couldn't be established")
                    return False                  
        except Exception:
            SingleLogger().logger.info("PostgreSQL: Database "+db_name+" doesn't exists")
            return False          

    def create(self, db_connection_string, db_name):
        """This function creates a database on PostgreSQL"""

        try:
            SingleLogger().logger.info(f"PostgreSQL: Creating database {db_name}")
            self.close()
            if not self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.connect(db_connection_string, "")
                self.cursor.execute('CREATE DATABASE '+db_name)
                stop_counter = time.time()
                SingleLogger().logger.info(f"PostgreSQL: Database {db_name} created")
                SingleLogger().logger.info(f"PostgreSQL: Done! Elapsed time: {round(stop_counter - start_counter,3)} seconds")
                self.connect(db_connection_string,db_name)
        except Exception:
            SingleLogger().logger.exception("PostgreSQL: Error while creating database", exc_info=True)
            sys.exit(1)

    def connect(self, db_connection_string, db_name):
        """This function establishes a connection with a postgreSQL database"""
        
        try:
            self.close()
            if self.exist(db_connection_string, db_name):
                SingleLogger().logger.info(f"PostgreSQL: Connecting to {db_connection_string}{db_name}")
                start_counter = time.time()
                self.conn = psycopg2.connect(db_connection_string+db_name)
                stop_counter = time.time()
                self.conn.set_session(autocommit=True)
                self.cursor = self.conn.cursor()
                SingleLogger().logger.info(f"PostgreSQL: Connection with {db_connection_string}{db_name} has been established")
                SingleLogger().logger.info(f"PostgreSQL: Done! Elapsed time: {round(stop_counter - start_counter,3)} seconds")
                self.__connection_string = db_connection_string
        except Exception:
            SingleLogger().logger.exception(f"PostgreSQL: Error while connecting to {db_connection_string}{db_name}", exc_info=True)
            sys.exit(1)
    
    def drop(self, db_connection_string, db_name):
        """This function drops a postgreSQL database"""
        
        try:
            SingleLogger().logger.info(f"PostgreSQL: Dropping the database {db_name}")
            self.connect(db_connection_string, "postgres") #This connection is needed to drop another database
            if self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.cursor.execute('DROP DATABASE IF EXISTS '+db_name)
                stop_counter = time.time()
                SingleLogger().logger.info(f"PostgreSQL: The database {db_name} has been dropped")
                SingleLogger().logger.info(f"PostgreSQL: Done! Elapsed time: {round(stop_counter - start_counter,3)} seconds")
            self.close()
        except Exception:
            SingleLogger().logger.exception("PostgreSQL: Error while dropping database", exc_info=True)
            sys.exit(1)

    def run_query(self, query:str, description:str="", expected_result:bool=False):
        """This function executes a query and prints the description and returns a list with the results"""

        try:
            result = ""
            if not description == "":
                SingleLogger().logger.info(f"PostgreSQL: {description}")
            start_counter = time.time()
            self.cursor.execute(query)
            stop_counter = time.time()
            if expected_result == True and self.cursor.rowcount > 0:
                result = self.cursor.fetchall()
            pattern = r'(?:FROM|INTO|UPDATE|DELETE\s+FROM|CREATE\s+TABLE)\s+(\w+)'
            tablename = re.search(pattern, query, re.IGNORECASE)
            if tablename and not (tablename.group(1) == "information_schema"):
                SingleLogger().logger.info(f"PostgreSQL: Done! Elapsed time: {round(stop_counter - start_counter,3)} seconds, Table: {tablename.group(1)}, Space occupied: {self.table_space_occupied(tablename.group(1))} MB")
            else:
                SingleLogger().logger.info(f"PostgreSQL: Done! Elapsed time: {round(stop_counter - start_counter,3)} seconds")
            return result
        except Exception:
            SingleLogger().logger.exception("PostgreSQL: Error while running query", exc_info=True)
            sys.exit(1)
            
    def close(self):
        """This function closes the cursor and connection"""

        try:
            if hasattr(self, 'cursor'):
                self.cursor.close()
                del self.cursor
            if hasattr(self, 'conn'):
                self.conn.close()
                del self.conn
            self.__connection_string = None
            SingleLogger().logger.info("PostgreSQL: Connection closed")
        except Exception:
            SingleLogger().logger.exception("PostgreSQL: Error while closing cursor and connection", exc_info=True)
            sys.exit(1)

    def table_space_occupied(self, tablename:str):
        """This function returns the space occupied by a table in MB"""

        try:
            self.cursor.execute("SELECT pg_total_relation_size('"+str(tablename)+"') AS total_size;")
            return round(self.cursor.fetchone()[0] / (1024 * 1024), 3)
        except Exception:
            SingleLogger().logger.exception(f"PostgreSQL: Error while getting space occupied by the table: {tablename}", exc_info=True)
            sys.exit(1)

    @property
    def connection_string(self):
        return self.__connection_string

    @connection_string.setter
    def logger(self, connection_string) -> None:
        self.__connection_string = connection_string