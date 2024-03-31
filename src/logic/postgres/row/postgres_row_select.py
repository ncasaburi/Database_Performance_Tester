from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn

def postgres_row_select_fn(type:str):
    """This function allows the user to select rows into a PostgreSQL database"""       
    
    try:
        postgres = PostgreSQL()
        if type == "default":
            print("The following query is going to be executed:\n")
            query = "SELECT * FROM doctors WHERE id_doctor BETWEEN 1 AND 5"
            print("  "+query)
            result = postgres.run_query(query,"Executing default select", True)
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
        else:
            postgres_table_list_fn(enable_interaction=False)
            print("Enter your query to select rows:\n")
            print("  Example:\n")
            print("    SELECT column1, column2 FROM tablename WHERE condition;")
            print("  \n  Your query:\n")
            query = input("    SELECT ")
            if not query.startswith("SELECT") or not query.startswith("select"):
                query = "SELECT " + query
            result = postgres.run_query(query,"Executing custom select", True)
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while selecting rows", exc_info=True)