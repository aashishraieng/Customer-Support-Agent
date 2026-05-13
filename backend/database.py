from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

client.admin.command("ping")

db = client["aaam_aadami_bank"]

users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]
cards_collection = db["cards"]
employees_collection = db["employees"]

print("MongoDB Connected Successfully")