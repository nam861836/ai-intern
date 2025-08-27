from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config.base_config import BaseConfiguration

def get_mongo_client():
    """
    Create a MongoDB client and test connection.
    Returns:
        MongoClient | None
    """
    config = BaseConfiguration()
    client = MongoClient(config.mongodb_config.uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("✅ Pinged your deployment. Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

