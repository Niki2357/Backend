
#9+1+1=11 variables
import sqlite3
import json
from flask import request

#Query the database and return everything

def post_lost(item_id, user_id, item_name,location, description, lf_time, image, completed, item_type):
    item_id = item_id
    user_id = user_id
    item_name = item_name
    lost_or_found = 1
    location = location
    description = description
    lf_time = lf_time
    image = image
    completed = completed
    item_type = item_type

    conn = sqlite3.connect('kentAPP.db')

    c = conn.cursor()

    c.execute("INSERT INTO lost_and_found(item_id, user_id, item_name,lost_or_found, location, description, lf_time, post_time, image, completed, item_type) VALUES(" + 
        "'" + item_id + "'," +
        "'" + user_id + "'," +
        "'" + item_name + "'," +
        "'" + lost_or_found + "'," +
        "'" + location + "'," +
        "'" + description + "'," +
        "'" + lf_time + "'," +
        "current_timestamp" + "," +
        "'" + image + "'," +
        "'" + completed + "'," +
        "'" + item_type
         + "')" )
    conn.commit()
    
    c.execute("SELECT * FROM lost_and_found")

    return ("thank you")
 

def post_found(item_id, user_id, item_name,location, description, lf_time, image, completed, item_type):
    item_id = item_id
    user_id = user_id
    item_name = item_name
    lost_or_found = 0
    location = location
    description = description
    lf_time = lf_time
    image = image
    completed = completed
    item_type = item_type

    conn = sqlite3.connect('KentAPP.db')

    c = conn.cursor()

    c.execute("INSERT INTO lost_and_found(item_id, user_id, item_name,lost_or_found, location, description, lf_time, post_time, image, completed, item_type) VALUES(" + 
        "'" + item_id + "'," +
        "'" + user_id + "'," +
        "'" + item_name + "'," +
        "'" + lost_or_found + "'," +
        "'" + location + "'," +
        "'" + description + "'," +
        "'" + lf_time + "'," +
        "current_timestamp" + "," +
        "'" + image + "'," +
        "'" + completed + "'," +
        "'" + item_type
         + "')" )
    conn.commit()
    
    c.execute("SELECT * FROM lost_and_found")

    return ("thank you")


def get_lost():
    conn = sqlite3.connect('kentAPP.db')
    c = conn.cursor()
    conn.commit()
    c.execute("SELECT * FROM lost_and_found where lost_or_found = 'true'")
    items = c.fetchall()

    return (json.dumps(items))
 

def get_found():
    conn = sqlite3.connect('kentAPP.db')
    c = conn.cursor()
    conn.commit()
    c.execute("SELECT * FROM lost_and_found where lost_or_found = 'false' ")
    items = c.fetchall()

    return (json.dumps(items))
 


