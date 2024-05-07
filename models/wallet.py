import uuid
import pprint
from typing import Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient

connection_string="mongodb+srv://"
client=MongoClient(connection_string)
production=client.production
wallet_collection=production.wallet_collection
printer = pprint.PrettyPrinter()



def find_all_wallets():
    wallets = list(wallet_collection.find())
    return wallets
def find_somme():
    somme=wallet_collection.find_one({"quantite":"somme"})
    printer.pprint(somme)

def count_all_wallet():
    count=wallet_collection.count_documents(filter={})
    print('number of wallets', count)

def get_wallet_by_id(wallet_id):
    from bson.objectid import ObjectId
    _id = ObjectId(wallet_id)
    wallet = wallet_collection.find_one({"_id":_id})
    printer.pprint(wallet)
    return wallet
def add_Wallet(  quantite: float):
    test_document = {
        "quantite": quantite
    }
    inserted_id = wallet_collection.insert_one(test_document).inserted_id
    print(f"Inserted document with ID: {inserted_id}")
def UpdateWallet(wallet_id,   newQuantite: float):
    from bson.objectid import ObjectId
    _id = ObjectId(wallet_id)
    new_doc={
        "quantite":newQuantite
    }
    
    wallet_collection.replace_one({"_id":_id},new_doc)
    
def deleteWallet(wallet_id):
    from bson.objectid import ObjectId
    _id = ObjectId(wallet_id)
    wallet_collection.delete_one({"_id":_id})
    


