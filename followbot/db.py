from pymongo import MongoClient
import os

client = MongoClient(os.environ["MONGO_URL"])

db = client["followbot"]

user_table = db["dnf"]
user_table.create_index("username", unique=True)
user_table.create_index("uid", unique=True)
