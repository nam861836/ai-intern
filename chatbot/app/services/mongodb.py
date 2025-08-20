from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config.base_config import BaseConfiguration
from datetime import datetime

config = BaseConfiguration()
# Create a new client and connect to the server
client = MongoClient(config.mongodb_config.uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def save_message(thread_id: str, message_type: str, content: str):
    messages_collection = client["chat_history"]["messages"]
    doc = {
        "thread_id": thread_id,
        "message_type": message_type,
        "content": content,
        "timestamp": datetime
    }
    messages_collection.insert_one(doc)
    

