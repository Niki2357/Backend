from flask_login import UserMixin

from db import get_db


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, admin=False, ban=False):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.admin = admin
        self.ban = ban
        self.teacher = User.is_teacher(email)

    @staticmethod
    def get_list():
        res = []
        db = get_db()
        entries = db.execute(
            "SELECT * FROM user"
        )
        if not entries:
            return None

        for entry in entries:
            user = User(entry[0], entry[1], entry[2], entry[3], admin=bool(entry[5]), ban=bool(entry[6]))
            res.append(dict(user))

        return res

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], admin=bool(user[5]), ban=bool(user[6])
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        admin = False
        if str(id_) == "116843363697558615402":  # Joe Yu is always the admin
            admin = True
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic, teacher, admin, banned)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic, User.is_teacher(email), admin, False),
        )
        db.commit()

    @staticmethod
    def is_teacher(email):
        return not any(char.isdigit() for char in email)  # Return True if the email does not contain graduation years

    def promoted(self):
        self.admin = True
        db = get_db()
        db.execute(
            "UPDATE user SET admin = 1 WHERE id =?",
            (self.id,)
        )
        db.commit()

    def banned(self):
        self.ban = True
        db = get_db()
        db.execute(
            "UPDATE user SET banned = 1 WHERE id =?",
            (self.id,)
        )
        db.commit()

    def unbanned(self):
        self.ban = True
        db = get_db()
        db.execute(
            "UPDATE user SET banned = 0 WHERE id =?",
            (self.id,)
        )
        db.commit()

    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        yield "email", self.email
        yield "profile_pic", self.profile_pic
        yield "is_teacher", bool(self.teacher)
        yield "admin", bool(self.admin)
        yield "banned", bool(self.ban)
