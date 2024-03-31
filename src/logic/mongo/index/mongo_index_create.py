from src.drivers.MongoDBDriver import MongoDB
from src.config.Config import Config
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper
import re
import ast

def mongo_index_create_fn(type:str):
    """This function allows the user to create a index"""
    
    try:
        pattern = r"db\.(\w+)\.createIndex\((.*?)\);"
        if type == "default":
            print("Creating default indexes...")
            content_nosql = Zipper().unzip_content(Config().default_data["default_mongo_indexes"]+"Indexes.zip","js")
            matches = re.findall(pattern, content_nosql)
        else:
            print("Enter the table creation query: \nExample: db.collectionname.createIndex([('fieldname', 1)]);")
            content_nosql = input()
            matches = re.findall(pattern, content_nosql)
        for match in matches:
            collection_name = match[0]
            parameters = match[1]
            parameters = ast.literal_eval(parameters)
            print("Executing -> db.", collection_name,".createIndex.",parameters)
            MongoDB().create_index(collection_name,parameters, f"Creating index on collection: {collection_name}")
    except:
        SingleLogger().logger.exception("MongoDB: Error while creating an index", exc_info=True)