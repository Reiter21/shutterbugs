from pymongo import MongoClient
from flask import session, redirect
from config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.mindcraft
user_collection = db['users']
leaderboard = db['leaderboard']


def user_data_upload(name, org, p1, p2, c1, c2, phone):
    search_query = {'_id': session['user']}
    update_query = {
        '$set': {
            'name': name,
            'organization': org,
            'participant1': p1,
            'participant2': p2,
            'class1': c1,
            'class2': c2,
            'phone': phone
        }
    }
    user_collection.update_one(search_query, update_query)
    current_level = leaderboard.find_one(search_query)['level']
    if current_level == '-':
        update_query = {
            '$set': {
                'level': 0
            }
        }
        leaderboard.update_one(search_query, update_query)
    return redirect('/play')
