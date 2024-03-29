from src.drivers.PostgreSQLDriver import PostgreSQL
from src.logger.SingleLogger import SingleLogger
from datetime import datetime

def postgres_row_update_fn(type:str):
    """This function allows the user to update rows into a PostgreSQL database"""       
    
    try:
        postgres = PostgreSQL()
        if type == "default":
            rows_left = postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0]
            print("How many rows do you want to update?: ("+str(rows_left)+" rows available)")
            rows_to_update = input()

            if int(rows_to_update) > rows_left:
                    print("The number of rows requested exceed the number of rows available.\nAs a result, "+str(rows_left)+" rows will be inserted")
                    input("Press enter to continue")
                    rows_to_update = rows_left

            postgres.run_query("UPDATE medical_records SET discharge_date = '"+datetime.now().strftime('%Y-%m-%d')+"' WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_medical_record DESC LIMIT "+str(rows_to_update)+")","Updating "+str(rows_to_update)+" medical records...")
            postgres.run_query("UPDATE patients SET name = 'Robert' WHERE id_patient IN ( SELECT id_patient FROM patients ORDER BY id_patient DESC LIMIT "+str(rows_to_update)+" )", "Updating "+str(rows_to_update)+" patients...")
            postgres.run_query("UPDATE doctors SET name = 'Mark' WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor DESC LIMIT "+str(rows_to_update)+" )", "Updating "+str(rows_to_update)+" doctors...")

        else:
            table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = '"+postgres.status()+"';", expected_result=True)
            print("Tables:\n")
            for table in table_list:
                print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
                print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
            print("")
            print("Enter your query to update rows: (if a field doesn't apply, press enter)\n")
            print("  Example:")
            print("    UPDATE tablename")
            print("    SET column1 = 'value1', column2 = 'value2'")
            print("    WHERE condition")
            tablename = input("\n\n  UPDATE ")
            set = input("  SET ")
            condition = input("  WHERE ")
            query = ""
            if not tablename == "":
                query = "UPDATE "+tablename
            if not set == "":
                query = query + " " + "SET "+set
            if not condition == "":
                query = query + " " + "WHERE "+ condition
            postgres.run_query(query,"Updating rows with custom query...")
    except:
        SingleLogger().logger.exception("Error while updating rows on PostgreSQL", exc_info=True)