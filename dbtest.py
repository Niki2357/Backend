import sqlite3
from flask import jsonify
import json

#Query the database and return everything

conn = sqlite3.connect('test.db')

c = conn.cursor()
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


c.execute("INSERT INTO lost_and_found VALUES ('book', 'library', true)")
conn.commit()
    
c.execute("SELECT * FROM lost_and_found")
items = c.fetchall()


print (json.dumps(items))


 

conn.close()
