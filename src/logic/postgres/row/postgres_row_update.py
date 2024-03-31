from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from datetime import datetime
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn

def postgres_row_update_fn(type:str):
    """This function allows the user to update rows into a PostgreSQL database"""       
    
    try:
        postgres = PostgreSQL()
        if type == "default":
            rows_left = postgres.run_query("SELECT COUNT(*) FROM doctors","Calculating the number of rows in the doctors' table",expected_result=True)[0][0]
            print("How many rows do you want to update?: ("+str(rows_left)+" rows available)")
            rows_to_update = input()

            if int(rows_to_update) > rows_left:
                    print("The number of rows requested exceed the number of rows available.\nAs a result, "+str(rows_left)+" rows will be inserted")
                    input("Press enter to continue")
                    rows_to_update = rows_left

            postgres.run_query("UPDATE medical_records SET discharge_date = '"+datetime.now().strftime('%Y-%m-%d')+"' WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_medical_record DESC LIMIT "+str(rows_to_update)+")","Updating "+str(rows_to_update)+" medical records")
            postgres.run_query("UPDATE patients SET name = 'Robert' WHERE id_patient IN ( SELECT id_patient FROM patients ORDER BY id_patient DESC LIMIT "+str(rows_to_update)+" )", "Updating "+str(rows_to_update)+" patients")
            postgres.run_query("UPDATE doctors SET name = 'Mark' WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor DESC LIMIT "+str(rows_to_update)+" )", "Updating "+str(rows_to_update)+" doctors")

        else:
            postgres_table_list_fn(enable_interaction=False)
            print("Enter your query to update rows:\n")
            print("  Example:\n")
            print("    UPDATE tablename SET column1 = 'value1', column2 = 'value2' WHERE condition;")
            print("  \n  Your query:\n")
            query = input("    UPDATE ")
            if not query.startswith("UPDATE") or not query.startswith("update"):
                query = "UPDATE " + query
            postgres.run_query(query,"Executing custom update")
            print("\nDone!\n")
            print("\nPress enter to continue")
            input()
    except:
        SingleLogger().logger.exception("PostgreSQL: Error while updating rows", exc_info=True)