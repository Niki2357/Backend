from db import get_db
import flask


class LostAndFound:
    def __init__(self, uuid, name, lost_or_found, user_id, location, description, start_time, image, completed,
                 target_user_id, end_time):
        self.uuid = uuid
        self.name = name
        self.lost_or_found = lost_or_found  # Boolean, True = an item is lost, False = someone found an item
        self.user_id = user_id
        self.location = location
        self.description = description
        self.start_time = start_time
        self.image = image
        self.completed = completed
        self.target_user_id = target_user_id
        self.end_time = end_time

    @staticmethod
    def get_list(limit=50, offset=0):
        res = []
        db = get_db()
        entries = db.execute(
            f"SELECT * FROM lost_and_found LIMIT {limit} OFFSET {offset}"
        )
        # print(entries)
        for entry in entries:
            # entry = entry.fetchone()
            lost = LostAndFound(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7],
                                entry[8], entry[9], entry[10])
            res.append(dict(lost))
        # print(res)
        return res

    @staticmethod
    def get(uuid):
        db = get_db()
        entry = db.execute(
            "SELECT * FROM lost_and_found WHERE uuid = ?", (str(uuid),)
        ).fetchone()
        if not entry:
            return None

        entry = LostAndFound(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8],
                             entry[9], entry[10])
        return entry

    @staticmethod
    def create_or_update(item=None, uuid_=None, name=None, lost_or_found=None, user_id=None, location=None,
                         description=None, start_time=None, image=None, completed=None, target_user_id=None,
                         end_time=None):
        db = get_db()
        if item is not None:
            # We are given the item, so we are updating, start going through the parameter and replacing fields if we
            # are not given None
            item.name = name or item.name  # Replace only when empty
            # lost_and_found status shouldn't be changed
            # user_id shouldn't be changed
            item.location = location or item.location  # Replace only when empty
            item.description = description or item.description  # Replace only when empty
            item.start_time = start_time or item.start_time  # Replace only when empty
            item.image = image or item.image  # Replace only when empty
            item.target_user_id = target_user_id or item.target_user_id  # Replace only when empty
            item.end_time = end_time or item.end_time  # Replace only when empty
            if completed is not None:
                item.completed = completed
        else:  # Never seen the UUID, must be new

            completed = False
            # target_user_id = target_user_id
            # end_time = end_time
            item = LostAndFound(uuid_, name, lost_or_found, user_id, location, description, start_time, image,
                                completed, target_user_id, end_time)

        db.execute(
            "INSERT OR REPLACE INTO lost_and_found (uuid, name, lost_or_found, user_id, location, description,"
            "start_time, image, completed, target_user_id, end_time) "
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (uuid_, item.name, bool(item.lost_or_found), str(item.user_id), item.location, item.description,
             item.start_time, item.image, bool(item.completed), str(item.target_user_id), item.end_time),
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM lost_and_found WHERE uuid = ?", (self.uuid,))
        db.commit()

    def __iter__(self):  # to dict
        yield "uuid", str(self.uuid)
        yield "name", self.name
        yield "user_id", self.user_id
        yield "location", self.location
        yield "description", self.description
        yield "start_time", self.start_time
        yield "image", self.image
        yield "completed", bool(self.completed)
        yield "target_user_id", self.target_user_id
        yield "end_time", self.end_time

    def to_json(self):
        return flask.jsonify(dict(self))
