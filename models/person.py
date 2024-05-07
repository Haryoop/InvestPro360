import pprint
from pymongo import MongoClient
from pydantic import BaseModel

connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
person_collection=production.person_collection
printer = pprint.PrettyPrinter()
test_db=client.test


def find_all_people():
    people = list(person_collection.find())
    return people

def insert_test_doc():
    collection=test_db.test
    test_document={
        "name":"Haroun",
        "type":"test"
    }
    inserted_id=collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")
    #print(inserted_id)

def add_person(first_name: str, last_name: str, age: int):
    collection = production.person_collection
    test_document = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")


def create_documents():
    first_names=["Tim","Sarah","Haroun","Ahmed"]
    last_names=["Ber","Trad","Jemaa","Mahjoub"]
    ages=[20,21,24,24]

    docs=[]


    for first_name, last_name, age in zip(first_names,last_names,ages):
        doc={"first_name": first_name, "last_name": last_name, "age": age}
        docs.append(doc)
        #person_collection.insert_one(doc)
    person_collection.insert_many(docs)





def find_haroun():
    haroun=person_collection.find_one({"first_name":"Haroun"})
    printer.pprint(haroun)

def count_all_people():
    count=person_collection.count_documents(filter={})
    print('number of people', count)

def get_person_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id":_id})
    printer.pprint(person)
    return person

def get_age_range(min_age, max_age):
    query = {
        "$and": [
            {"age": {"$gte": min_age}},
            {"age": {"$lte": max_age}}
        ]
    }
    people = person_collection.find(query).sort("age")
    for person in people:
        printer.pprint(person)

def project_columns():
    columns = {"_id":0, "first_name":1,"last_name":1}
    people = person_collection.find({},columns)
    for person in people:
        printer.pprint(person)

def update_person_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    #all_updates={
    #    "$set":{"new_field":True},
    #    "$inc":{"age":1},
    #    "$rename":{"first_name":"first","last_name":"last"}
    #}
    #person_collection.update_one({"_id":_id}, all_updates)

    person_collection.update_one({"_id":_id},{"$unset":{"new_field":""}})

def UpdatePerson(person_id, newFirst_name: str, newLast_name: str, newAge: int):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    new_doc={
        "first_name":newFirst_name,
        "last_name":newLast_name,
        "age":newAge
    }
    person_collection.replace_one({"_id":_id},new_doc)

def deletePerson(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    person_collection.delete_one({"_id":_id})