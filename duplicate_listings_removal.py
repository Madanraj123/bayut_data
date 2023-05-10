import pymongo
import os

# Connect to MongoDB
uri = os.getenv("MONGO URI ")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# select database and collection
db = client['bayut']
collection = db['all_listings']

# Fetch all documents from collection
documents = collection.find()

# Create a dictionary to store unique room and area combinations
unique_combinations = {}

# Loop through all documents and group by unique room and area combinations
for document in documents:
    room = document["rooms"]
    area = document["area"]
    location= document['location'][1]['name']
    category = document['category'][1]['name']
    key = (room, area, location,category)
    if key in unique_combinations:
        unique_combinations[key].append(document)
    else:
        unique_combinations[key] = [document]

# Save the grouped documents to a new collection
new_collection = db["unique_listings"]
for key, documents in unique_combinations.items():
    new_document = {
        "room": key[0],
        "area": key[1],
        "location":key[2],
        "category":key[3],
        "documents": documents
    }
    new_collection.insert_one(new_document)
