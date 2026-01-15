
import pymongo

uri = "mongodb+srv://kaxxynaero:Darakushita12@cluster0.55rhxrp.mongodb.net/?appName=Cluster0"
client = pymongo.MongoClient(uri)
db = client['campus_db']

if 'django_migrations' in db.list_collection_names():
    for doc in db['django_migrations'].find().sort([('app', 1), ('name', 1)]):
        print(f"{doc['app']} - {doc['name']}")
else:
    print("django_migrations collection not found")
