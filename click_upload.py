from datetime import datetime
from email.mime import image
import pytz
from flask import redirect, session, flash, Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from config import DATABASE_URL
from time import sleep
import string
import random

app = Flask(__name__)

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')


app.config['MONGO_URI'] = DATABASE_URL
mongo = PyMongo(app)
client = MongoClient(DATABASE_URL)
db = client.mindcraft
user_collection = db['users']
leaderboard = db['leaderboard']
questions = db['questions']
answer_log = db['answer-entry-log']
dq_collection = db['dq-participants']
checking_collection = db['checker']
image_collection = db['image-entry']


def accept_click(response, level):
    user_lb = leaderboard.find_one({'_id': session['user']})
    datetime_ist = datetime.now(IST)
    time = datetime_ist.strftime('%d/%m/%Y %H:%M:%S %Z %z')
    search_query = {'_id': session['user']}

    format = getFormat(response.filename)

    if format not in ['jpg', 'jpeg', 'tiff', 'raw', 'png']:
        return redirect('/play')

    fileName = imageNameGen(format)

    mongo.save_file(fileName, response)

    # live logs
    print(f"[{user_lb['username']}] uploaded click for Level-{level} @{time}")

    current_lvl_data = image_collection.find_one(search_query)[f'level{level}']
    updated_responses = current_lvl_data['responses']
    updated_responses.append(fileName)

    update_query = {
        '$set': {
            f'level{level}': {
                'number': current_lvl_data['number'] + 1,
                'responses': updated_responses
            }
        }
    }
    image_collection.update_one(search_query, update_query)
    flash("Upload successful", 'correct-ans')
    return redirect('/play')


    
def imageNameGen(format):
    return f"{''.join(random.choices(string.ascii_lowercase+string.ascii_lowercase+string.digits, k=random.randint(10,15)))}.{format}"

def getFormat(filename):
    out = ''
    for i in filename[::-1]:
        if i == '.':
            return out[::-1]
        out += i
    return False

def getImages(user_id, levels):
    tmp = image_collection.find_one({'_id': user_id})
    ret = []
    for i in range(levels):
        if tmp[f'level{i}']['number'] > 0:
            ret.append(tmp[f'level{i}']['responses'][-1])
        else:
            ret.append('none')
    return ret

def getAllImages(user_id, levels):
    tmp = image_collection.find_one({'_id': user_id})
    ret = []
    for i in range(levels):
        if tmp[f'level{i}']['number'] > 0:
            ret.append(tmp[f'level{i}']['responses'])
        else:
            ret.append('none')
    return ret