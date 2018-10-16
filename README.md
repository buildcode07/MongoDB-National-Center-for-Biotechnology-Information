MongoBD - PyMongo

Some basic working of pymongo
=============================

<!-- import two inportant modules of pymongo -->
import pymongo 
from pymongo import MongoClient

<!-- connect to mongoDB client -->
client = MongoClient('localhost', 27017) 

<!-- list all current databases -->
current_dbs = client.database_names()

<!-- select a database with name 'database_name' -->
DATABASE = client[database_name]

<!-- list all current colelctions under the selected database 'database_name' -->
current_collections = DATABASE.collection_names(include_system_collections=False)

<!-- select a database with name 'collection_name' -->
COLLECTION = DATABASE[collection_name]

<!-- querying using regex, finds multiple documents -->
query_documents = COLLECTION.find({attribute: {"$regex": search_text}})

<!-- querying using regex, finds only one document -->
query_documents = COLLECTION.find_one({attribute: {"$regex": search_text}})
