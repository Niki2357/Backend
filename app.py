from flask import Flask
from flask import request, jsonify
import database
import lost_and_found
import activity
import user

import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return"Hello, world"
    

@app.route("/database")
def detabase():
    return database.show_all()

@app.route("/test")
def test():
    return"test page!"

@app.route("/lost_and_found/lost", methods=['GET'])
def get_lost():
    return lost_and_found.get_lost()

@app.route("/lost_and_found/lost/post", methods=['POST'])
def post_lost():
    json_data = request.json
    print(json_data)
    item_id = json_data['item_id']
    user_id = json_data['user_id']
    item_name = json_data['item_name']
    location = json_data['location']
    description = json_data['description']
    lf_time = json_data['lf_time']
    post_time = json_data['post_time']
    image = json_data['image']
    completed = json_data['completed']
    item_type = json_data['item_type']

    return lost_and_found.post_found(item_id, user_id, item_name,location, description, lf_time, post_time, image, completed, item_type)

@app.route("/lost_and_found/found", methods=['GET'])
def get_found():
    return lost_and_found.get_found()

@app.route("/lost_and_found/found/post", methods=['POST'])
def post_found():
    json_data = request.json
    print(json_data)
    item_id = json_data['item_id']
    user_id = json_data['user_id']
    item_name = json_data['item_name']
    location = json_data['location']
    description = json_data['description']
    lf_time = json_data['lf_time']
    image = json_data['image']
    completed = json_data['completed']
    item_type = json_data['item_type']

    return lost_and_found.post_found(item_id, user_id, item_name,location, description, lf_time, image, completed, item_type)

@app.route("/activity", methods=['GET'])
def get_activity():
    return activity.get_activity()

@app.route("/activity/post", methods=['POST'])
def post_activity():

    json_data = request.json
    print(json_data)
    act_id = json_data['act_id']
    user_id = json_data['user_id']
    title = json_data['title']
    image = json_data['image']
    description = json_data['description']
    deadline = json_data['deadline']
    activity_time = json_data['activity_time']
    location = json_data['location']
    activity_type = json_data['activity_type']
    space_used = json_data['space_used']
    space_limit = json_data['space_limit']

    return activity.post_activity(act_id, user_id, title, image, description, deadline, activity_time, location, activity_type,space_used, space_limit)

@app.route("/user", methods=['GET'])
def get_user():
    return user.get_user()

@app.route("/user/post", methods=['POST'])
def post_user():
    json_data = request.json
    print(json_data)
    user_id = json_data['user_id']
    name = json_data['name']
    email = json_data['email']
    profile_pic = json_data['profile_pic']
    teacher = json_data['teacher']
    admin = json_data['admin']
    banned = json_data['banned']
    return user.post_user(user_id,name,email,profile_pic,teacher,admin,banned)

if __name__ == "__main__":
    app.run()


#=======================================================================

#dummy lost and found item list
lost_list = [
    {'id':1, 'name':'Bible','location':'Chapel','lost_or_found':True},
    {'id':2, 'name':'Wallet','location':'dining hall','lost_or_found':True},
    {'id':3, 'name':'Bag','location':"",'lost_or_found':True}
]
found_list = [
    {'id':1, 'name':'book','location':'library','lost_or_found':False},
    {'id':2, 'name':'pencil','location':'dickenson','lost_or_found':False},
    {'id':3, 'name':'phone','location':'town','lost_or_found':False}
]

#fake activity list
act_list = [
    {'id':1, 'name':'Math club','location':'S519'},
    {'id':2, 'name':'squash game','location':'squash court'},
    {'id':3, 'name':'Weekend Mall trip','location':'behind HC'}
]

#fake user list
user_list = [
    {'id':1, 'name':'Niki','gender':'F','email':'huj23'},
    {'id':2, 'name':'Jiayi','gender':'F','email':'jiayi24'},
    {'id':3, 'name':'NH','gender':'hidden','email':'niki.hu04'}
]