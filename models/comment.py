import uuid
import pprint
import pymongo
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient
from datetime import datetime

connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
comment_collection=production.comment_collection
printer = pprint.PrettyPrinter()




def find_all_comments():
    comments = list(comment_collection.find().sort("creation_date", pymongo.DESCENDING))
    return comments
def count_all_comments():
    count=comment_collection.count_documents(filter={})
    print('number of comments: ', count)

def get_comment_by_id(comment_id):
    from bson.objectid import ObjectId
    _id = ObjectId(comment_id)
    comment = comment_collection.find_one({"_id":_id})
    printer.pprint(comment)
    return comment
def add_Comment(post_id: str, author: str, contenu: str):
    current_time = datetime.now()
    test_document = {
        "source": post_id,
        "author": author,
        "contenu": contenu,
        "creation_date": current_time
    }
    inserted_id = comment_collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")

def UpdateComment(comment_id, newAuthor: str, newContenu: str):
    from bson.objectid import ObjectId
    _id = ObjectId(comment_id)
    existing_comment = get_comment_by_id(comment_id)
    new_doc={
        "author":newAuthor,
        "contenu":newContenu,
        "creation_date": existing_comment["creation_date"]
    }
    comment_collection.replace_one({"_id":_id},new_doc)