from pymongo import MongoClient, collection
from config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.mindcraft
collection = db['checker']


def runhunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'running'
    }
    }
    collection.update_one(search, update)


def endhunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'ended'
    }
    }
    collection.update_one(search, update)


def pausehunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'paused'
    }
    }
    collection.update_one(search, update)
