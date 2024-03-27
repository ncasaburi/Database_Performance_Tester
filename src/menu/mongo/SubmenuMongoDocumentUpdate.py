from consolemenu import *
from consolemenu.items import *
from src.drivers.MongoDBDriver import MongoDB
from src.menu.status import status
from src.logger.SingleLogger import SingleLogger
from datetime import datetime

class SubmenuMongoDocumentUpdate():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowUpdate class"""
        
        #submenu definition
        self.submenu_mongo_document_update = ConsoleMenu("MongoDB Document Updates", status)
        
        #submenu items
        mongo_document_update_default = FunctionItem("Update default rows", self.mongo_document_update_fn, args=["default"]) 
        mongo_document_update_custom = FunctionItem("Update custom rows", self.mongo_document_update_fn, args=["custom"])

        #submenu appends
        self.submenu_mongo_document_update.append_item(mongo_document_update_default)
        self.submenu_mongo_document_update.append_item(mongo_document_update_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_mongo_document_update

    def mongo_document_update_fn(self, type:str):
        """This function allows the user to update rows into a PostgreSQL database"""       
        
        try:
            if type == "default":
                collection_default = 'patients'
                collection = MongoDB().db[collection_default]
                documents_left = collection.count_documents({})
                print("How many documents do you want to update?: ("+str(documents_left)+" documents available)")
                documents_to_update = input()


                if int(documents_to_update) > documents_left:
                        print("The number of documents requested exceed the number of documents available.\nAs a result, "+str(documents_left)+" documents will be inserted")
                        input("Press enter to continue")
                        documents_to_update = documents_left

                id_minimo = str(1)
                id_maximo = str(documents_to_update)
                query_update = {"id_patient": {"$gte": id_minimo, "$lte": id_maximo}}
                update = {"$set": {"name": "Roberts"}}
                MongoDB().execute_query_update('patients',query_update,update)
                query_update = {"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}}
                update = {"$set": {"name": "Mark"}}
                MongoDB().execute_query_update('doctors',query_update,update)
                query_update = {"id_medical_record": {"$gte": id_minimo, "$lte": id_maximo}}
                update = {"$set": {"discharge_date": datetime.now().strftime('%Y-%m-%d')}}
                MongoDB().execute_query_update('medical_records',query_update,update)
                  
                # # Realizar la actualización
                # result = collection.update_many({"id_patient": {"$gte": id_minimo, "$lte": id_maximo}},
                #                      {"$set": {"name": "Roberts"}})
                #print("Total documents updated:", result.modified_count)

                # collection_default = 'doctors'
                # collection = MongoDB().db[collection_default]
                # result = collection.update_many({"id_doctor": {"$gte": id_minimo, "$lte": id_maximo}},
                #                      {"$set": {"name": "Mark"}})
                # print("Total documents updated:", result.modified_count)

                # postgres.run_query("UPDATE medical_records SET discharge_date = '"+datetime.now().strftime('%Y-%m-%d')+"' WHERE id_medical_record IN ( SELECT id_medical_record FROM medical_records ORDER BY id_medical_record DESC LIMIT "+str(rows_to_update)+")","Updating "+str(rows_to_update)+" medical records...")
                # postgres.run_query("UPDATE doctors SET name = 'Mark' WHERE id_doctor IN ( SELECT id_doctor FROM doctors ORDER BY id_doctor DESC LIMIT "+str(rows_to_update)+" )", "Updating "+str(rows_to_update)+" doctors...")

            else:
                # table_list = postgres.run_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = '"+postgres.status()+"';", expected_result=True)
                print("Tables:\n")
        #         for table in table_list:
        #             print(" - "+str(table[0])+" (rows: "+str(postgres.run_query("SELECT COUNT(*) FROM "+str(table[0]),"",expected_result=True)[0][0])+", columns: "+str(postgres.run_query("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '"+str(table[0])+"';","",expected_result=True)[0][0])+")")
        #             print("   ("+', '.join(item[0] for item in postgres.run_query("SELECT column_name FROM information_schema.columns WHERE table_name = '"+str(table[0])+"'","",expected_result=True))+")")
        #         print("")
        #         print("Enter your query to update rows: (if a field doesn't apply, press enter)\n")
        #         print("  Example:")
        #         print("    UPDATE tablename")
        #         print("    SET column1 = 'value1', column2 = 'value2'")
        #         print("    WHERE condition")
        #         tablename = input("\n\n  UPDATE ")
        #         set = input("  SET ")
        #         condition = input("  WHERE ")
        #         query = ""
        #         if not tablename == "":
        #             query = "UPDATE "+tablename
        #         if not set == "":
        #             query = query + " " + "SET "+set
        #         if not condition == "":
        #             query = query + " " + "WHERE "+ condition
        #         postgres.run_query(query,"Updating rows with custom query...")
        except:
            SingleLogger().logger.exception("Error while updating rows on PostgreSQL", exc_info=True)