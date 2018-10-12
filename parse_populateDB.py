import os
import pymongo
from glob import glob
from bs4 import BeautifulSoup
from pymongo import MongoClient

global bulk_insert
bulk_insert = list()

# create dictionary for each document
def createDocument(pmid, pmcid, title, abstract):
    global bulk_insert
    current_document = {
        "pmid"     : pmid,
        "pmcid"    : pmcid,
        "title"    : title,
        "abstract" : abstract,
        "code"     : "CSE-593"
    }
    bulk_insert.append(current_document)

# populate the database
def populateDatabase():
    client = MongoClient('localhost', 27017) # connect on the default host and port
    print("Insert the name of the database")
    database_name = raw_input()
    db = client[database_name] # Fetch the required database
    # dbs = MongoClient().database_names() # get list of all databases
    print("Insert the name of the collection")
    collection_name = raw_input()
    collection = db[collection_name] # Fetch the required collection
    # db.collection_names(include_system_collections=False) # get list of all collections
    print("Status Update: Inserting into Collection")
    insert = collection.insert_many(bulk_insert) # insert all the dictionaries in the array
    print("Status Update: Insertion Done")

'''
    1. Get all files with .nxml extension including their directory name
    2. All folders will be searched recursively
'''

def getFiles():
    file_names = list()
    pattern   = "*.nxml"
    folder_count, file_count = 0, 0
    for dir,_,_ in os.walk(os.getcwd()):
        folder_count += 1
        current_folder = glob(os.path.join(dir,pattern))
        for file in current_folder:
            file_count += 1
            file_names.append("/".join(file.split("/")[-3:]))
    return file_names

# get abstract of a document
def getAbstract(soup, filename):
    abstract = soup.find("abstract")
    abstract_text = ""
    # if there is no abstract tag, add the filename to a file to keep track of documents that does not have a abstract
    if not abstract:
        no_abstract_file = open("no_abstract.txt", "w")
        no_abstract_file.write(filename)
        no_abstract_file.write("\n")
        no_abstract_file.close()
    else:
        # get texts of only paragraph tags.
        abstract = abstract.find_all("p")
        for para in abstract:
            parts = para.get_text().split()
            abstract_text += " ".join(parts)
    return abstract_text

# get title of a document
def getTitle(soup, filename):
    title_tag = soup.find("article-title")
    title = ""
    # if there is no title tag, add the filename to a file to keep track of documents that does not have a title
    if not title_tag:
        no_title_file = open("no_title.txt", "w")
        no_title_file.write(filename)
        no_title_file.close()
    else:
        title = title_tag.get_text()
    return title

# get required ID's of a document
def getIDs(soup):
    pmid, pmcid = "", ""
    article_ids = soup.find_all("article-id") # get the list of all article id tags
    for id in article_ids:
        id_type = id["pub-id-type"]
        # get only pmid, and pmcid. id.get_text() gets the full text of the id tag
        if id_type == "pmid": pmid = id.get_text()
        elif id_type == "pmc": pmcid = id.get_text()
        else: pass # other types of id's are also there like 'doi', 'manuscript', 'publisher-id', 'art-access-id', 'publisher-manuscript'
    return pmid, pmcid

def parseFiles(file_names):
    try:
        article_type_file = open("article_type.txt", "w")
        no_article_type_file = open("no_article_type.txt", "w")
        article_types_set = set()
        dirname = os.path.dirname(__file__)
        current_count, research_article_count = 0, 0
        for file in file_names:
            current_count += 1
            # print ("Total Files Parsed: {}".format(current_count))
            filename = os.path.join(dirname, file)
            input_file = open(file, "r")
            soup = BeautifulSoup(input_file,"lxml")
            if len(soup):
                article_tag = soup.find_all("article")
                if not len(article_tag): no_article_type_file.write("file"); no_article_type_file.write("\n")
                article_type = soup.article["article-type"]
                # we proceed with populating the database only if the article type is "research-article"
                if not(current_count % 500):
                    print "Status Update: {} Files Done. Number of Research Articles are {}".format(current_count, research_article_count)
                if article_type == "research-article":
                    research_article_count += 1
                    pmid, pmcid = getIDs(soup)
                    title, abstract = getTitle(soup, filename), getAbstract(soup, filename)
                    createDocument(pmid, pmcid, title, abstract)
    except Exception as e:
        print e

    # now populate the database with the documents in global bulk_insert list
    populateDatabase()
    print ("Total Articles Parsed: {}, Total Research Articles: {}").format(current_count, research_article_count)
    article_type_file.close()
    no_article_type_file.close()

def main():
    print "Status Update: Getting File Names"
    file_names = getFiles()
    print "Status Update: Parsing Files"
    parseFiles(file_names)
    print "Status Update: Execution Done"

if __name__ == '__main__':
    main()
