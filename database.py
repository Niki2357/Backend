import sqlite3
import json

#Query the database and return everything

def show_all():
    
    conn = sqlite3.connect('test.db')

    c = conn.cursor()


    c.execute("INSERT INTO lost_and_found VALUES ('book', 'library', true)")
    conn.commit()
    
    c.execute("SELECT * FROM lost_and_found")
    items = c.fetchall()

    return (json.dumps(items))
 

    conn.close()

#=====================================================
