import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "whatsapp_bot")

client = AsyncMongoClient(MONGODB_URL)
db = client[DB_NAME]

products_collection = db["products"]