import psycopg2

def postgres_connection(db_connection_string, db_name=""):
    """This function establishes the connection with PostgreSQL"""

    conn = None
    try:
        conn = psycopg2.connect(db_connection_string+db_name)
        conn.set_session(autocommit=True)
        cursor = conn.cursor()
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
    return cursor