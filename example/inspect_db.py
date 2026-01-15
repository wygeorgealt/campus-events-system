
import pymongo

uri = "mongodb+srv://kaxxynaero:Darakushita12@cluster0.55rhxrp.mongodb.net/?appName=Cluster0"
client = pymongo.MongoClient(uri)
db = client['campus_db']

collections = db.list_collection_names()
print(f"Collections: {collections}")

if 'events_event' in collections:
    doc = db['events_event'].find_one()
    if doc:
        print(f"Event keys: {list(doc.keys())}")

if 'events_ticket' in collections:
    count = db['events_ticket'].count_documents({})
    print(f"Ticket count: {count}")
    doc = db['events_ticket'].find_one()
    if doc:
        print(f"Ticket keys: {list(doc.keys())}")
