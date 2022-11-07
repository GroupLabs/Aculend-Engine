from dotenv import load_dotenv
import os
import pymongo

def connectMongo():
    # Connection

    conn_str = f"mongodb+srv://admin:{os.getenv('MONGO_PASS')}@cluster0.ngbgtru.mongodb.net/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(conn_str)
    db = client.test

    return db