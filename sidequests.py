from flask import redirect, session, flash
from pymongo import MongoClient
from config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.mindcraft
user_collection = db['users']
sidequest_collection = db['sidequests']


def new_quest(content):
    sidequest_collection.update_one(
        {'_id': 'sidequest'},
        {'$set': {'content': content}}
    )


def fetch_quest():
    return sidequest_collection.find_one({'_id': 'sidequest'})['content']
