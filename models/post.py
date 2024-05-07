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
post_collection=production.post_collection
printer = pprint.PrettyPrinter()




def find_all_posts():
    posts = list(post_collection.find().sort("creation_date", pymongo.DESCENDING))
    return posts
def count_all_posts():
    count=post_collection.count_documents(filter={})
    print('number of posts: ', count)

def get_post_by_id(post_id):
    from bson.objectid import ObjectId
    _id = ObjectId(post_id)
    post = post_collection.find_one({"_id":_id})
    printer.pprint(post)
    return post
def add_Post(title: str, author: str, contenu: str):
    current_time = datetime.now()
    test_document = {
        "title": title,
        "author": author,
        "contenu": contenu,
        "creation_date": current_time
    }
    inserted_id = post_collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")

def UpdatePost(post_id, newTitle: str, newAuthor: str, newContenu: str):
    from bson.objectid import ObjectId
    _id = ObjectId(post_id)
    existing_post = get_post_by_id(post_id)
    new_doc={
        "title":newTitle,
        "author":newAuthor,
        "contenu":newContenu,
        "creation_date": existing_post["creation_date"]
    }
    post_collection.replace_one({"_id":_id},new_doc)