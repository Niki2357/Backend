import sqlite3
import json
import array as arr

#Query the database and return everything

def post_user(user_id,name,email,profile_pic,teacher,admin,banned):
    user_id = str(user_id)
    name = name
    email = email
    profile_pic = profile_pic
    teacher = str(teacher)
    admin = str(admin)
    banned = str(banned)

    conn = sqlite3.connect('kentAPP.db')
    c = conn.cursor()
    c.execute("INSERT INTO user(user_id,name,email,profile_pic,teacher,admin,banned) VALUES(" + 
        "'" + user_id + "'," +
        "'" + name + "'," +
        "'" + email + "'," +
        "'" + profile_pic + "'," +
        "'" + teacher + "'," +
        "'" + admin + "'," +
        "'" + banned
         + "')" )
    conn.commit()
    conn.close()

    obj = dict(user_id=user_id,name=name,email=email,profile_pic=profile_pic,teacher=teacher,admin=admin,banned=banned)
    conn.close()
    return (json.dumps(obj))
  
def get_user():
    conn = sqlite3.connect('kentAPP.db')
    c = conn.cursor()
    conn.commit()
    c.execute("SELECT * FROM user")
    items = c.fetchall()
    row_count = 0
    # row_total = c.execute("SELECT COUNT(*) FROM user")
    row_total = 8
    all = []
    
    while row_count<row_total:
        obj = dict(user_id=items[row_count][0],
        name=items[row_count][1],
        email=items[row_count][2],
        profile_pic=items[row_count][3],
        teacher=items[row_count][4],
        admin=items[row_count][5],
        banned=items[row_count][6])
        all.append(obj)
        row_count+= 1



    conn.close()
    return (json.dumps(all))
 
