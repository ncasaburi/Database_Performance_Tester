from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
from src.logic.mongo.collection.mongo_collection_list import mongo_collection_list_fn
import ast
import os
import re

def mongo_document_query_find_fn(type:str):
    """This function allows the user to perform queries with find on a MongoDB database"""

    try:
        mongo = MongoDB()
        if type == "default":
            print("The following query is going to be executed:\n")
            query = "doctors.find({'id_doctor': {'$gte': 1, '$lte': 5}})"
            print("  "+query)
            result = mongo.execute_query_find("doctors", {'id_doctor': {'$gte': 1, '$lte': 5}}, "Executing default find query1 in collection: doctors")
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
        else:
            mongo_collection_list_fn(enable_interaction=False)
            print("Enter your query in pymongo:\n")
            print("  Example:\n")
            print("    collection = collecion_name")
            print('    query = {"field": "value"}')
            print("  \n  Your query:\n")
            collection_name = input("    collection = ")
            query = input("    query = {")
            if not query.startswith("{"):
                query = "{" + query
            if not query.endswith("}"):
                query = query + "}"
            result = mongo.execute_query_find(collection_name, ast.literal_eval(query), f"Executing custom find in collection: {collection_name}")
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
    except:
        SingleLogger().logger.exception("MongoDB: Error while executing find", exc_info=True)