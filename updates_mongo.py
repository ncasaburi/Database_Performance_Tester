# import pymongo
# import json

# def execute_operation(document_str):
#     # Establecer conexión a la base de datos MongoDB
#     client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
#     db = client.hospital
#     collection = db.patient_documents
    
#     try:
#         # Parsear la cadena JSON a un diccionario Python
#         document_dict = json.loads(document_str)
        
#         # Extraer el filtro y la actualización del diccionario
#         filter_query = document_dict["$or"]
#         print(filter_query)
#         update_query = document_dict["$set"]
#         print(update_query)
#         # Ejecutar la operación de actualización
#         result = collection.update_many(filter_query, update_query)
#         print("Operación ejecutada correctamente. Documentos modificados:", result.modified_count)
#     except Exception as e:
#         print("Error al ejecutar la operación:", e)
#     finally:
#         # Cerrar la conexión con la base de datos
#         client.close()

# # Llamada a la función para ejecutar la operación
# document_str = '{ "$or": [ { "name": { "$regex": "^a" } }, { "name": { "$regex": "^f" } } ] },{ "$set": { "birthday": "2024-12-31" } }'
# execute_operation(document_str)


#Codigo que funciona
import pymongo
import json

def execute_operation(operation_str):
    # Establecer conexión a la base de datos MongoDB
    client = pymongo.MongoClient("mongodb://admin:secret@localhost:27017/")
    db = client.hospital
    collection = db.patient_documents
    
    # Ejecutar la operación de actualización
    try:
        collection.update_many({ "$or": [ { "name": { "$regex": "^a" } }, { "name": { "$regex": "^f" } } ] },{ "$set": { "birthday": "2024-12-31" } })
        print("Operación ejecutada correctamente.")
    except Exception as e:
        print("Error al ejecutar la operación:", e)
    finally:
        # Cerrar la conexión con la base de datos
        client.close()

# Llamada a la función para ejecutar la operación
execute_operation("db.patient_documents.updateMany({ $or: [ { name: /^A/ }, { name: /^F/ } ] },{ $set: { birthday: '2024-01-02' }})")


