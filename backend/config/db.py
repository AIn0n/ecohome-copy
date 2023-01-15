import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

conn = pymongo.MongoClient(os.getenv("MONGO_URL"))

conn["database"]["rooms"].create_index([("name", pymongo.DESCENDING)], unique=True)

collection = conn["database"]["rooms"]
