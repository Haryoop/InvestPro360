import uuid
import pprint
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient
from datetime import datetime



connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
transaction_collection=production.transaction_collection
printer = pprint.PrettyPrinter()




def find_all_transactions():
    transactions = list(transaction_collection.find())
    return transactions
def count_all_transaction():
    count=transaction_collection.count_documents(filter={})
    print('number of transactions', count)

def get_transaction_by_id(transaction_id):
    from bson.objectid import ObjectId
    _id = ObjectId(transaction_id)
    transaction = transaction_collection.find_one({"_id":_id})
    printer.pprint(transaction)
    return transaction
def add_Transaction(amount:float, type:str, date:float):
    """Add transaction details."""
    assert type in ['withdraw', 'deposit'], 'Type must be either "withdraw" or "deposit"'
    test_document = {
         "amount": amount,
         "type": type,
         "date" : date
    }
    inserted_id = transaction_collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")
    
    
def UpdateTransaction(transaction_id,   newAmount: float,newType:str,newDate:float):
    from bson.objectid import ObjectId
    _id = ObjectId(transaction_id)
    assert newType in ['withdraw', 'deposit'], 'Type must be either "withdraw" or "deposit"'
    new_doc={
        "amount":newAmount,
        "type":newType,
        "date":newDate }
    transaction_collection.replace_one({"_id":_id},new_doc)
    
def deleteTransaction(transaction_id):
    from bson.objectid import ObjectId
    _id = ObjectId(transaction_id)
    transaction_collection.delete_one({"_id":_id})
    
    
    


