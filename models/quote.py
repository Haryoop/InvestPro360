import pprint
from pymongo import MongoClient
from pydantic import BaseModel

connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
quote_collection=production.quote_collection
printer = pprint.PrettyPrinter()
test_db=client.test


def find_all_quote():
    quote = list(quote_collection.find())
    return quote

def insert_test_doc():
    collection=test_db.test
    test_document={
        "name":"Haroun",
        "type":"test"
    }
    inserted_id=collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")
    #print(inserted_id)

def add_quote(celebrety: str, quote: str, image: str):
    collection = production.quote_collection
    test_document = {
        "celebrety": celebrety,
        "quote": quote,
        "image": image
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")

def count_all_quote():
    count=quote_collection.count_documents(filter={})
    return count

def get_quote_by_id(quote_id):
    from bson.objectid import ObjectId
    _id = ObjectId(quote_id)
    quote = quote_collection.find_one({"_id":_id})
    printer.pprint(quote)
    return quote
#tochange
def project_columns():
    columns = {"_id":0, "first_name":1,"last_name":1}
    people = quote_collection.find({},columns)
    for person in people:
        printer.pprint(person)

def UpdateQuote(quote_id, newCelebrety: str, newQuote: str, newImage: str):
    from bson.objectid import ObjectId
    _id = ObjectId(quote_id)
    new_doc={
        "celebrety":newCelebrety,
        "quote":newQuote,
        "image":newImage
    }
    quote_collection.replace_one({"_id":_id},new_doc)

def deleteQuote(quote_id):
    from bson.objectid import ObjectId
    _id = ObjectId(quote_id)
    quote_collection.delete_one({"_id":_id})