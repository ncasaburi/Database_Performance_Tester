from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.logger.SingleLogger import SingleLogger

def mongo_document_delete_fn(type:str) -> None:
    """This function allows the user to delete rows ina a table"""

    try:
        if type == "default":
            collection_default = 'doctor_medical_records'
            collection = MongoDB().db[collection_default]
            documents_left = collection.count_documents({})
            print("How many documents do you want to delete?: ("+str(documents_left)+" documents available)")
            documents_to_delete = input()
            if int(documents_to_delete) > documents_left:
                print("The number of documents requested exceed the number of documents available.\nAs a result, "+str(documents_left)+" documents will be inserted")
                input("Press enter to continue")
                documents_to_delete = documents_left

            id_minimo = int(1)
            id_maximo = int(documents_to_delete)
            query_delete = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('doctor_medical_records',query_delete)
            query_delete = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('doctors',query_delete)
            query_delete = {"id_patient": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('patients',query_delete)
            query_delete = {"id_medical_record": {"$gte": id_minimo, "$lte": id_maximo}}
            MongoDB().execute_query_delete('medical_records',query_delete)

            # print("How many rows do you want to delete?: ("+str(postgres.run_query("SELECT COUNT(*) FROM doctors","",expected_result=True)[0][0])+" rows left)")
            # rows_to_delete = input()
            # postgres.run_query("DELETE FROM doctor_medical_records WHERE id_doctor IN ( SELECT id_doctor FROM doctor_medical_records ORDER BY id_medical_record DESC, id_doctor DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" relationships between doctors and medical records...")
            # postgres.run_query("DELETE FROM medical_records WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_patient DESC, id_medical_record DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" medical records...")
            # postgres.run_query("DELETE FROM patients WHERE id_patient IN ( SELECT id_patient FROM patients ORDER BY id_patient DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" patients...")
            # postgres.run_query("DELETE FROM doctors WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor DESC LIMIT "+str(rows_to_delete)+" )","Deleting "+str(rows_to_delete)+" doctors...")
        else:
            # table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = '"+postgres.status()+"';", expected_result=True)
            # print("Tables:\n")
            # for table in table_list:
            #     print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
            #     print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
            # print("")
            # print("Enter your query to delete rows:\n")
            # print("  Example:")
            # print("    DELETE FROM tablename")
            # print("    WHERE condition")
            # tablename = input("\n\n  DELETE FROM ")
            # condition = input("  WHERE ")
            # query = ""
            # if not tablename == "":
            #     query = "DELETE FROM "+tablename
            # if not condition == "":
            #     query = query + " " + "WHERE "+ condition
            # postgres.run_query(query)
            print("Collection")
    except:
        SingleLogger().logger.exception("Error while deleting documents to MongoDB", exc_info=True)