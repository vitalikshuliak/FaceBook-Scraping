from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from dotenv import load_dotenv
from facebook_scraper import FacebookScraper
from datetime import timedelta
import datetime
import os
from pathlib import Path
import json
from utils import get_env_value, facebook_login, get_city
from automate import fb_join_request, get_group_posts
from bson import ObjectId


ENV_PATH = Path(__file__).resolve().parent/ ".env"
load_dotenv(dotenv_path=ENV_PATH)

app = Flask(__name__)
db_username = get_env_value("DB_USERNAME")
db_password = get_env_value("DB_PASSWORD")
dbname = get_env_value("DATABASE_NAME")
collection_name = get_env_value("COLLECTION_NAME")
client = MongoClient(f"mongodb+srv://{db_username}:{db_password}@grouptracker.qmpwcd4.mongodb.net/{dbname}?retryWrites=true&w=majority")

fb = FacebookScraper()
fb_email = get_env_value("FB_EMAIL")
fb_password = get_env_value("FB_PASSWORD")
fb_url = get_env_value("FB_URL")

# Access a database and collection
db = client[dbname]
collection = db[collection_name]


@app.route('/posts', methods=['POST'])
def get_post():
    try:
        data = request.get_json(force=True)
        group_url = data.get('url') if data.get("url") is not None else ""
        keywords = data.get("keywords") if data.get("keywords") is not None else ""
        print('keywords  ', keywords)
        post_data = get_group_posts(group_url, keywords, fb_email,fb_password)
        if bool(post_data):
            if collection.find_one({'post_id': post_data['post_id']}) is None:
                # Post is not already in the database, insert it
                collection.insert_one(post_data)
                del post_data['_id']
                return jsonify({'posts': post_data})
            return jsonify({'posts': post_data})
        else:
            # Retrieve all posts from the database and return as JSON response
            result = collection.find_one({}, sort=[('_id', -1)])
            del result['_id']
            return jsonify({'posts': result})
    except Exception as exp:
        print("Error:",repr(exp))
        return jsonify({'Message': f"There were some problem at the server...Please try again after sometime."})
        

@app.route('/join_request', methods=['POST'])
def join_request():
    url = request.get_json(force=True).get("url")
    message = fb_join_request(url,fb_email,fb_password)
    json_message = json.dumps(message)  # Serialize the message to JSON
    return Response(json_message, mimetype='application/json')

@app.route('/', methods=['GET'])
def home():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True,port=5000)
