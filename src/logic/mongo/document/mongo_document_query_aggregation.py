from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.config.Zipper import Zipper
from src.logger.SingleLogger import SingleLogger
from src.logic.mongo.collection.mongo_collection_list import mongo_collection_list_fn
import ast
import os
import re

def mongo_document_query_aggregation_fn(type:str):
    """This function allows the user to perform queries with aggregation on a MongoDB database"""

    try:
        mongo = MongoDB()
        if type == "default":
            print("The following query is going to be executed:\n")
            collection_name = 'doctors'
            query = '[ {"$match": {"name": "Michael"}}, {"$limit": 5} ]'
            print("  collection = "+collection_name)
            print("  pipeline = "+query)
            result = mongo.execute_aggregate(collection_name, ast.literal_eval(query))
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
        else:
            mongo_collection_list_fn(enable_interaction=False)
            print("Enter your query in pymongo:\n")
            print("  Example:\n")
            print("    collection = collecion_name")
            print("    pipeline =")
            print("    [")
            print('       {"$stage1": {...}} , {"$stageN": {...}}')
            print("    ]")
            print("  \n  Your query:\n")
            collection_name = input("    collection = ")
            print("    pipeline =")
            print("    [")
            stages = input("       {")
            if stages.endswith(","):
                stages = stages[:-1]
            if not stages.startswith("[{"):
                stages = "[{" + stages
            if not stages.endswith("]"):
                stages = stages + "]"
            result = mongo.execute_aggregate(collection_name, ast.literal_eval(stages))
            print("\nResult:\n")
            print("  "+'\n  '.join(map(str, result)))
            print("\n\nPress enter to continue...")
            input()
    except:
        SingleLogger().logger.exception("Error while quering the MongoDB with find", exc_info=True)