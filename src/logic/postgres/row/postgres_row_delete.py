from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from src.logic.postgres.table.postgres_table_list import postgres_table_list_fn

def postgres_row_delete_fn(type:str) -> None:
    """This function allows the user to delete rows ina a table"""

    try:
        postgres = PostgreSQL()
        if type == "default":
            print("How many rows do you want to delete?: ("+str(postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0])+" rows left)")
            rows_to_delete = input()
            postgres.run_query("DELETE FROM doctor_medical_records WHERE id_doctor IN ( SELECT id_doctor FROM doctor_medical_records ORDER BY id_medical_record DESC, id_doctor DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" relationships between doctors and medical records...")
            postgres.run_query("DELETE FROM medical_records WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_patient DESC, id_medical_record DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" medical records...")
            postgres.run_query("DELETE FROM patients WHERE id_patient IN ( SELECT id_patient FROM patients ORDER BY id_patient DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" patients...")
            postgres.run_query("DELETE FROM doctors WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" doctors...")
        else:
            postgres_table_list_fn(enable_interaction=False)
            print("Enter your query to delete rows:\n")
            print("  Example:\n")
            print("    DELETE FROM tablename WHERE condition")
            print("  \n  Your query:\n")
            query = input("    DELETE FROM ")
            if not query.startswith("DELETE FROM") or not query.startswith("delete from"):
                query = "DELETE FROM " + query
            postgres.run_query(query,"Executing custom delete on PostgreSQL...")
            print("\nDone!\n")
            print("\nPress enter to continue...")
            input()
    except:
        SingleLogger().logger.exception("Error while deleting rows to PostgreSQL", exc_info=True)