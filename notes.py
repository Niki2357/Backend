item_name text not null,
	    lost_or_found boolean not null,
	    user_id text not null,
	    location text not null,
	    description text,
	    lf_time datetime not null,
	    post_time datetime not null,
	    image text,
	    completed boolean not null,
	    item_type text not null

 c.execute("""
    CREATE TABLE lost_and_found(
        item_name text not null,
	    lost_or_found boolean not null,
	    user_id text not null,
	    location text not null,
	    description text,
	    lf_time datetime not null,
	    post_time datetime not null,
	    image text,
	    completed boolean not null,
	    item_type text not null
    )

    """)


    c.execute("""
    CREATE TABLE activity(
    name text
    )
    """)



#============================
#可以用的activity.py

import sqlite3
import json

#Query the database and return everything

def post_activity():
    
    conn = sqlite3.connect('activity.db')

    c = conn.cursor()
    c.execute("INSERT INTO activity VALUES ('activity1')")
    conn.commit()
    
    c.execute("SELECT * FROM activity")
    items = c.fetchall()

    return (json.dumps(items))
 

    conn.close()

    print ("item_name")
    item_name = request.get()
    print ("lost or found")
    lost_or_found = request.get()
    print ("user id")
    user_id = request.get()
    print ("location")
    location = request.get()
    print ("description")
    description = request.get()
    print ("lf_time")
    lf_time = request.get()
    print ("post_time")
    post_time = request.get()
    print ("image")
    image = request.get()
    print ("completed?")
    completed = request.get()
    print ("item type")
    item_type = request.get()


    
