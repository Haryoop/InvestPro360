import uuid
import pprint
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient


connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
reclamation_collection=production.reclamation_collection
printer = pprint.PrettyPrinter()




def find_all_reclamations():
    reclamations = list(reclamation_collection.find())
    return reclamations
def count_all_reclamation():
    count=reclamation_collection.count_documents(filter={})
    print('number of people', count)

def get_reclamation_by_id(reclamation_id):
    from bson.objectid import ObjectId
    _id = ObjectId(reclamation_id)
    reclamation = reclamation_collection.find_one({"_id":_id})
    printer.pprint(reclamation)
    return reclamation
def add_Reclamation(title: str, author: str, synopsis: str):
    test_document = {
        "title": title,
        "author": author,
        "synopsis": synopsis
    }
    inserted_id = reclamation_collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")
def UpdateReclamation(reclamation_id, newTitle: str, newAuthor: str, newSynopsis: str):
    from bson.objectid import ObjectId
    _id = ObjectId(reclamation_id)
    new_doc={
        "title":newTitle,
        "author":newAuthor,
        "synopsis":newSynopsis
    }
    reclamation_collection.replace_one({"_id":_id},new_doc)
def deleteReclamation(reclamation_id):
    from bson.objectid import ObjectId
    _id = ObjectId(reclamation_id)
    reclamation_collection.delete_one({"_id":_id})