import mongo_cfg
import pymongo
import praw

DB_URL = mongo_cfg.URL
DB_URL = "mongodb://localhost:27017/"

client = pymongo.MongoClient(DB_URL)
db = client.test


myclient = pymongo.MongoClient(DB_URL)

mydb = myclient["mydatabase"]

