import os
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import json

app = Flask(__name__)

PORT = 5001
DB_ENVIRONMENT = environ.get('DB_ENVIRONMENT') or "localhost"
client = MongoClient(host=DB_ENVIRONMENT,
                        port=27018
                    )

CORS(app) 

db = client['user_db']
sample_data = [
    {
    "_id": "112532673980137782859",
    "given_name": "Keith Loh",
    "email" : "keith.loh.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2"
    ],
    "recommended_classes": [],
    },
    {
    "_id": "113532673980137782859",
    "given_name": "Joseph Hee",
    "email" : "joseph.hee.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [],
    "recommended_classes": [],
    },
    {
    "_id": "114532673980137782859",
    "given_name": "Tyler Lian",
    "email" : "tyler.lian.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2",
        "Review 3"
    ],
    "recommended_classes": [],
    },
    {
    "_id": "115542673980137782859",
    "given_name": "Teo Sean",
    "email" : "teosean@outlook.com",
    "picture": "https://lh3.googleusercontent.com/a/AGNmyxZr5-3b5UcQFgka72_O7-Hci1I664JFT-ZJHVsV0eM=s96-c",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
    ],
    "recommended_classes": [],
    },
    {
    "_id": "116532673980137782859",
    "given_name": "Elton Tay",
    "email" : "elton.tay.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [],
    "recommended_classes": [],
    },
] 


# <------Routes for userDB------>
@app.route('/health', methods=('GET', 'POST'))
def index():
    return "User Service is up and running"

# Initalise the user database with the sample data above
@app.route('/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'user_db' in db_exists:
        client.drop_database('user_db')
    db = client['user_db']
    for data in sample_data:
        db["users"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# Get all users in the userDB
@app.route('/')
def get_all_users():
    users = db.users.find()
    if (users == None):
        return "no users in DB"
    else:
        return json.loads(json_util.dumps(users))

# Get a particular user by their userId else return string saying no such user
@app.route('/<userId>')
def get_user(userId):
    myquery = { "_id": userId }
    user = db.users.find_one(myquery)
    if user == None:
        return f"User with _id:{userId} does not exist in the database ", 400
    return json.loads(json_util.dumps(user))

# Add user to the userDB if user does not exist in DB, else update user details
@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.get_json()
    if (data == None):
        return "Invalid user details", 400
    else:
        userId = data["id"]
        myquery = { "_id": userId }
        user = db.users.find_one(myquery)
        if (user != None):
            return json.loads(json_util.dumps(user))
        else:
            addObject = {            
                "_id": data["id"],
                "given_name": data["given_name"],
                "email": data["email"],
                "picture": data["picture"],
                "preferences": [],
                "attended_classes": [],
                "recommended_classes": [],
            }
            db.users.insert_one(addObject)
            return addObject

# add class attended to userID
@app.route('/addClass/<userId>', methods=['PUT'])
def add_class(userId):
    data = request.get_json()
    myquery = { "_id": userId }
    user_doc = db.users.find_one(myquery)
    if not user_doc:
            return f"User with _id: {userId} does not exist", 404
    newvalues = { "$push": { "attended_classes": data["classId"] } }
    if data["classId"] not in user_doc["attended_classes"]:
        updated_user = db.users.find_one_and_update(myquery, newvalues, return_document=ReturnDocument.AFTER)
        return json.loads(json_util.dumps(updated_user))
    else:
        updated_user = user_doc
        return f"User with _id: {userId} already attended class",404

# Add preferences
@app.route('/pref/<userId>', methods=['PUT'])
def add_preferences(userId):
    data = request.get_json()
    myquery = { "_id": userId }
    newvalues = { "$push": { "preferences": data['preference'] } }
    updated_user = db.users.find_one_and_update(myquery, newvalues, return_document=ReturnDocument.AFTER)
    if not updated_user:
        return f"User with _id: {userId} does not exist", 404
    return json.loads(json_util.dumps(updated_user))

# Add recommended classes
@app.route('/recc/<userId>', methods=['PUT'])
def add_recommendations(userId):
    data = request.get_json()
    myquery = { "_id": userId }
    newvalues = { "$set": { "recommended_classes": data['recommended_classes'] } }
    updated_user = db.users.find_one_and_update(myquery, newvalues,return_document=ReturnDocument.AFTER)
    if not updated_user:
        return f"User with _id: {userId} does not exist", 404
    return json.loads(json_util.dumps(updated_user))

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    create_db()
    app.run(host='0.0.0.0', port=PORT, debug=True)
print(f"User Service is initialized on port {PORT}")