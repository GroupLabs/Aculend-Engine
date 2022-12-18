from dotenv import load_dotenv
import os
import pymongo

def connectMongo():
    # Connection

    conn_str = f"mongodb://127.0.0.1:27017/"

    client = pymongo.MongoClient(conn_str)
    db = client["local"]

    return db