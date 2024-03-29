from src.logger.SingleLogger import SingleLogger
import psycopg2
import time
import sys

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
            if not db_name == "":
                SingleLogger().logger.info("Checking whether Postgres database "+db_name+" exist or not...")
                conn_temp = psycopg2.connect(db_connection_string+db_name)
                cursor_temp = conn_temp.cursor()
                cursor_temp.execute("SELECT datname FROM pg_database")
                databases = cursor_temp.fetchall()
                if (db_name,) in databases:
                    SingleLogger().logger.info("Postgres database "+db_name+" already exists")
                    cursor_temp.close()
                    del cursor_temp
                    conn_temp.close()
                    del conn_temp
                    return True
                else:
                    SingleLogger().logger.info("Postgres database "+db_name+" doesn't exists")
                    return False
            else:
                try:
                    conn_temp = psycopg2.connect(db_connection_string)
                    conn_temp.close()
                    del conn_temp
                    return True
                except Exception:
                    SingleLogger().logger.info("The connection with "+db_connection_string+" couldn't be established")
                    return False                  
        except Exception:
            SingleLogger().logger.info("Postgres database "+db_name+" doesn't exists")
            return False          

    def create(self, db_connection_string, db_name):
        """This function creates a database on PostgreSQL"""

        try:
            SingleLogger().logger.info("Creating database "+db_name+" on postgreSQL...")
            self.close()
            if not self.exist(db_connection_string, db_name):
                start_counter = time.time()
                self.connect(db_connection_string, "")
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
            self.close()
            if self.exist(db_connection_string, db_name):
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
            self.connect(db_connection_string, "postgres") #This connection is needed to drop another database
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
            if not description == "":
                SingleLogger().logger.info(description)
            start_counter = time.time()
            self.cursor.execute(query)
            stop_counter = time.time()
            SingleLogger().logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            SingleLogger().logger.info("The sql query has been executed")
            SingleLogger().logger.info(f"current timeout: {self.conn.get_parameter_status('connect_timeout')}")
            if expected_result == True and self.cursor.rowcount > 0:
                return self.cursor.fetchall()
        except Exception:
            SingleLogger().logger.exception("Error while running query to PostgreSQL", exc_info=True)
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