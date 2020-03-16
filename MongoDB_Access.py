import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://bigdom1023:**********@dom-cluster-1numt.mongodb.net/test?retryWrites=true&w=majority")

def get_dictionary_words():
    db = client.get_database("EnglishWords")
    collection = db.get_collection("Words")
    document = collection.find_one()
    words = document.get("wordList")
    return words
