from db import get_db
import flask


class Event:

    def __init__(self, uuid, uploader_id, title, image, content, time_posted, deadline, activity_time, location,
                 organizers,
                 activity_type, space_used, space_available):
        self.uuid = uuid
        self.uploader_id = uploader_id
        self.title = title
        self.image = image
        self.content = content
        self.time_posted = time_posted
        self.deadline = deadline
        self.activity_time = activity_time
        self.location = location
        self.organizers = organizers
        self.activity_type = activity_type
        self.space_used = space_used
        self.space_available = space_available

    @staticmethod
    def get_list(limit=50, offset=0):
        res = []
        db = get_db()
        entries = db.execute(
            f"SELECT * FROM events LIMIT {limit} OFFSET {offset}"
        )
        # print(entries)
        for entry in entries:
            # entry = entry.fetchone()
            event = Event(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7],
                          entry[8], entry[9], entry[10], entry[11], entry[12])
            res.append(dict(event))
        # print(res)
        return res

    @staticmethod
    def get(uuid):
        db = get_db()
        entry = db.execute(
            "SELECT * FROM events WHERE uuid = ?", (str(uuid),)
        ).fetchone()
        if not entry:
            return None

        entry = Event(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8],
                      entry[9], entry[10], entry[11], entry[12])
        return entry

    @staticmethod
    def create_or_update(event=None, uuid_=None, uploader_id=None, title=None, image=None, content=None,
                         time_posted=None, deadline=None,
                         activity_time=None, location=None, organizers=None,
                         activity_type=None, space_used=None, space_available=None):
        db = get_db()
        if event is not None:
            # We are given the event, so we are updating, start going through the parameter and replacing fields if we
            # are not given None
            # uploader shouldn't need update
            event.title = title if title or title != 'None' else event.title  # Replace only when empty
            event.image = image if title or title != 'None' else event.image
            event.content = content if title or title != 'None' else event.content
            # time posted shouldn't need update
            event.deadline = deadline if title or title != 'None' else event.deadline
            event.activity_time = activity_time if title or title != 'None' else event.activity_time
            event.location = location if title or title != 'None' else event.location
            event.organizers = organizers if title or title != 'None' else event.organizers
            event.activity_type = activity_type if title or title != 'None' else event.activity_type
            event.space_used = space_used if title or title != 'None' else event.space_used
            event.space_available = space_available if title or title != 'None' else event.space_available
        else:  # Never seen the UUID, must be new

            # target_user_id = target_user_id
            # end_time = end_time
            event = Event(uuid_, uploader_id, title, image, content, time_posted, deadline, activity_time, location,
                          organizers, activity_type, space_used, space_available)

        db.execute(
            "INSERT OR REPLACE INTO events (uuid, uploader_id, title, image, content, time_posted, deadline, "
            "activity_time, location, organizers,activity_type, space_used, space_available) "
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (str(uuid_), event.uploader_id, event.title, event.image, event.content, event.time_posted, event.deadline,
             event.activity_time, event.location, event.organizers, event.activity_type, event.space_used,
             event.space_available),
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM events WHERE uuid = ?", (self.uuid,))
        db.commit()

    def signup(self):
        # yet to be implemented
        pass

    def __iter__(self):
        yield "uuid", self.uuid
        yield "uploader_id", self.uploader_id
        yield "title", self.title
        yield "image", self.image
        yield "content", self.content
        yield "time_posted", self.time_posted
        yield "deadline", self.deadline
        yield "activity_time", self.activity_time
        yield "location", self.location
        yield "organizers", self.organizers
        yield "activity_type", self.activity_type
        yield "space_used", self.space_used
        yield "space_available", self.space_available
