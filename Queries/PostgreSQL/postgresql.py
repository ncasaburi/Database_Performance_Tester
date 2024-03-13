import psycopg2
from psycopg2 import errors
import time
import sys
import zipfile
import os

class PostgreSQL():

    def __init__(self, db_connection_string, logger, db_name):
        """This function establishes the connection with PostgreSQL"""

        try:
            conn = psycopg2.connect(db_connection_string)
            conn.set_session(autocommit=True)
            cursor = conn.cursor()
            cursor.execute('DROP DATABASE IF EXISTS '+db_name)
            cursor.execute('CREATE DATABASE '+db_name)
            cursor.close()
            conn.close()
            logger.info("Connecting to PostgreSQL database...")
            start_counter = time.time()
            self.conn = psycopg2.connect(db_connection_string+db_name)
            self.conn.set_session(autocommit=True)
            stop_counter = time.time()
            logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
            self.cursor = self.conn.cursor()    
        except Exception:
            logger.exception("Error while connecting to PostgreSQL", exc_info=True)
            sys.exit(1)

    def run_query(self, query, logger, description=""):
        """This function executes a query and prints the description"""

        try:
            if not description == "":
                logger.info(description)
            start_counter = time.time()
            self.cursor.execute(query)
            stop_counter = time.time()
            logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
        except Exception:
            logger.exception("Error while running query to PostgreSQL", exc_info=True)
            sys.exit(1)

    def run_query_from_file(self, path, logger, description=""):
        """This function executes a query from a file and prints the description"""

        try:
            if not description == "":
                logger.info(description)
            with zipfile.ZipFile(path+'.zip', 'r') as zip_ref:
                file_path = os.path.basename(path+'.sql')
                with zip_ref.open(file_path, 'r') as file:
                    query = file.read()
                    start_counter = time.time()
                    self.cursor.execute(query)
                    stop_counter = time.time()
                    logger.info("Done! Elapsed time: "+str(stop_counter - start_counter)+" seconds")
        except Exception:
            logger.exception("Error while running query from a file to PostgreSQL", exc_info=True)
            sys.exit(1)

    def close(self, logger):
        """This function close the cursor and connection"""

        try:
            self.cursor.close()
            self.conn.close()
            logger.info("Connection closed\n")
        except Exception:
            logger.exception("Error while closing PostgreSQL cursor and connection", exc_info=True)
            sys.exit(1)
