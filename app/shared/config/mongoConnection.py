from pymongo.mongo_client import MongoClient
from sqlalchemy.ext.declarative import declarative_base
uri = "mongodb+srv://regibermontoya2005:baguvix123@medicproject.pr7vw.mongodb.net/?retryWrites=true&w=majority&appName=medicProject"

# Create a new client and connect to the server
client = MongoClient(uri)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
