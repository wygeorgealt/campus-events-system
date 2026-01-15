
import pymongo
from pymongo.errors import ConnectionFailure

uri = "mongodb+srv://kaxxynaero:Darakushita12@cluster0.55rhxrp.mongodb.net/?appName=Cluster0"
try:
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    print("Connection successful")
except ConnectionFailure as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
