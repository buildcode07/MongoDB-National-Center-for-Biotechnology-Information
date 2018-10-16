import os
import pymongo
from pymongo import MongoClient

global DATABASE
global COLLECTION

# get appropriate results by querying the database
def get_results(attribute, search_text):
    try:
        query_title = COLLECTION.find({attribute: {"$regex": search_text}}) # query is matched using regular expression
        os.system("clear")
        print("{} articles found").format(query_title.count())
        if query_title.count() > 0:
            print("What do you want to output?")
            print("1. title 2. abstract 3. PMID 4. PMCID")
            input = int(raw_input())
            if input == 1: search_type = "title"
            elif input == 2: search_type = "abstract"
            elif input == 3: search_type = "pmid"
            else: search_type = "pmc"
            os.system("clear")
            print("Enter the number of results to display:"),
            num_display = int(raw_input())
            num_display = num_display if num_display <= query_title.count() else query_title.count()
            os.system("clear")
            for i in range(num_display):
                print str(i + 1) + ". " + query_title[i][search_type]
                print "\n"
        else:
            pass
    except Exception as e:
        print (e)

# allow users to query title, abstract, PMID, or PMCID
def queryMongoDB():
    try:
        print("What do you want to search?")
        print("===========================")
        print("1. Title 2. Abstract 3. PMID 4. PMCID") # options for selecting the search type
        option = int(raw_input())
        os.system("clear")
        if option == 1:
            print("Enter the word/phrase to search")
            search_text = raw_input().strip()
            get_results("title", search_text)
        elif option == 2:
            print("Enter the word/phrase to search")
            search_text = raw_input().strip()
            get_results("abstract", search_text)
        elif option == 3:
            print("Enter the PMID")
            search_text = raw_input().strip()
            get_results("pmid", search_text)
        elif option == 4:
            print("Enter the PMCID")
            search_text = raw_input().strip()
            query_title = COLLECTION.find({"pmcid": {"$regex": search_text}})
            get_results("pmcid", search_text)

        print("Do you want to query again?. Enter 'yes' or 'no'.")
        input = raw_input()
        if input in ["yes", "YES","y", "Y"]: os.system("clear"); queryMongoDB()
        else: return
    except Exception as e:
        print e

# pre configure the database and collection by taking user inputs
def selectDB():
    global DATABASE
    global COLLECTION
    try:
        client = MongoClient('localhost', 27017)
        current_dbs = client.database_names()
        count = 1
        print("Total List of Databases")
        print("=======================")
        for db in current_dbs:
            print str(count) + ". " + db
            count += 1
        print "Enter the number of the database to select:",
        database_name = current_dbs[int(raw_input().strip()) - 1]
        DATABASE = client[database_name] # database selected
        print "\n"
        current_collections = DATABASE.collection_names(include_system_collections=False)
        count = 1
        print("Total List of Collections")
        print("=========================")
        for collection in current_collections:
            print str(count) + ". " + collection
            count += 1
        print("Enter the number of the collection to select:"),
        collection_name = current_collections[int(raw_input().strip()) - 1]
        COLLECTION = DATABASE[collection_name] # collection selected
        os.system("clear")
        print("Database: {}, Collection: {}").format(database_name, collection_name)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    selectDB()
    queryMongoDB()
    print ("Done querying!")
