#11+1=12 variables
import sqlite3
import json
from flask import request

#Query the database and return everything

def post_activity(act_id, user_id, title, image, description, deadline, activity_time, location, activity_type,space_used, space_limit):
    act_id = act_id
    user_id = user_id
    title = title
    image = image
    description = description
    deadline = deadline
    activity_time = activity_time
    location = location
    activity_type = activity_type
    space_used = space_used
    space_limit = space_limit

    conn = sqlite3.connect('kentAPP.db')

    c = conn.cursor()
    c.execute(
        "INSERT INTO activity(act_id, user_id, title, image, description, post_time, deadline, activity_time, location, activity_type,space_used, space_limit) VALUES(" + 
        "'" + act_id + "'," +
        "'" + user_id + "'," +
        "'" + title + "'," +
        "'" + image + "'," +
        "'" + description + "'," +
        "current_timestamp" + "," +
        "'" + deadline + "'," +
        "'" + activity_time + "'," +
        "'" + location + "'," +
        "'" + activity_type + "'," +
        "'" + space_used + "'," +
        "'" + space_limit
         + "')" )
    conn.commit()
    
    c.execute("SELECT * FROM activity")

    return ("finished")
 

    conn.close()

def get_activity():
    conn = sqlite3.connect('kentAPP.db')
    c = conn.cursor()
    conn.commit()
    c.execute("SELECT * FROM activity")
    items = c.fetchall()

    return (json.dumps(items))
 

    conn.close()

