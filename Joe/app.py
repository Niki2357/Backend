# Python standard libraries
import json
import os
import sqlite3
import uuid
import datetime

# Third party libraries

from flask import Flask, redirect, request, url_for, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User
from lostandfound import LostAndFound
from event import Event

# Configuration
# IMPORTANT: THIS IS MY PERSONAL CLIENT ID AND SECRET, DO NOT PUBLISH
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID",
                                  None) or "90594130632-isla2hkb7n2lh4mgtrl376mm94ntpd3h.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None) or "BIYQ69Y1FRCZZkKG604Bks0M"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            # "<p>Hello, {}! You're logged in! Email: {}</p>"
            # "<div><p>Google Profile Picture:</p>"
            # '<img src="{}" alt="Google profile pic"></img></div>'
            # '<a class="button" href="/logout">Logout</a>'.format(
            #     current_user.name, current_user.email, current_user.profile_pic
            # )
            "Success"
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/content")
@login_required
def content():
    return "You are logged in: This Is The Secret Content"


@app.route("/lost_and_found", methods=['GET', 'POST'])
@login_required  # @TODO IMPORTANT: Remember to uncomment this when deploying (if this whole line is commented)
def lost():
    if current_user.ban:
        return 'You are banned, please contact the administrator.', 403
    if request.method == 'GET':
        entries = LostAndFound.get_list()
        return jsonify(entries)
    elif request.method == 'POST':
        try:
            data_json = json.loads(request.data)
            if data_json["operation"] == "create":
                try:
                    uuid_ = str(uuid.uuid4())
                    LostAndFound.create_or_update(uuid_=uuid_,
                                                  name=data_json["name"],
                                                  lost_or_found=data_json["lost_or_found"],
                                                  user_id=current_user.id,
                                                  location=data_json["location"],
                                                  description=data_json["description"],
                                                  start_time=int(datetime.datetime.now().timestamp()),
                                                  image=data_json["image"],
                                                  )
                    return uuid_
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "update":
                try:
                    item = LostAndFound.get(data_json["uuid"])
                    if item is None:
                        return "Item not found", 404
                    if current_user.admin or item.user_id == current_user.id:  # only admin and same user can modify
                        LostAndFound.create_or_update(item=item,
                                                      uuid_=data_json["uuid"],
                                                      name=data_json["name"],
                                                      # lost_or_found=data_json["lost_or_found"], Shouldn't need update
                                                      # user id shouldn't need update
                                                      location=data_json["location"],
                                                      description=data_json["description"],
                                                      start_time=data_json["start_time"],
                                                      image=data_json["image"],
                                                      completed=data_json["completed"],
                                                      target_user_id=data_json["target_user_id"],
                                                      end_time=data_json["end_time"]
                                                      )
                        return "OK"
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "delete":
                try:
                    item = LostAndFound.get(data_json["uuid"])
                    if item is None:
                        return "Item not found", 404
                    if current_user.admin or current_user.id == item.user_id:
                        item.delete()
                        return "OK"
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            else:
                return "Bad Operation", 400
        except KeyError:
            return "Missing Info", 400
        except json.decoder.JSONDecodeError:
            return "Bad json", 400


@app.route("/user", methods=['GET', 'POST'])
@login_required  # @TODO IMPORTANT: Remember to uncomment this when deploying (if this whole line is commented)
def user_info():
    if current_user.ban:
        return 'You are banned, please contact the administrator.', 403
    if request.method == 'GET':
        entries = User.get_list()
        return jsonify(entries)
    elif request.method == 'POST':
        try:
            data_json = json.loads(request.data)
            if data_json["operation"] == "request_info":
                try:
                    user = User.get(
                        str(data_json["user_id"]))  # Remember user uuid is a string, cuz it's too long as int
                    if user is None:
                        return "User Not Found", 404
                    return jsonify(user.to_dict())
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "promote":
                try:
                    if current_user.admin:  # only admin can promote
                        user = User.get(str(data_json["user_id"]))
                        if user is None:
                            return "User Not Found", 404
                        user.promoted()
                        return 'Success'
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "ban":
                try:
                    if current_user.admin:  # only admin can promote
                        user = User.get(str(data_json["user_id"]))
                        if user is None:
                            return "User Not Found", 404
                        user.banned()
                        return 'Success'
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "unban":
                try:
                    if current_user.admin:  # only admin can promote
                        user = User.get(str(data_json["user_id"]))
                        if user is None:
                            return "User Not Found", 404
                        user.unbanned()
                        return 'Success'
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            else:
                return "Bad Operation", 400
        except KeyError:
            return "Missing Info", 400
        except json.decoder.JSONDecodeError:
            return "Bad json", 400


@app.route("/explore", methods=['GET', 'POST'])
@login_required
def explore():
    if current_user.ban:
        return 'You are banned, please contact the administrator.', 403
    if request.method == 'GET':
        entries = Event.get_list()
        return jsonify(entries)
    elif request.method == 'POST':
        try:
            data_json = json.loads(request.data)
            if data_json["operation"] == "create":
                try:
                    uuid_ = str(uuid.uuid4())
                    Event.create_or_update(uuid_=uuid_,
                                           uploader_id=current_user.id,
                                           title=data_json['title'],
                                           image=data_json['image'],
                                           content=data_json['content'],
                                           time_posted=int(datetime.datetime.now().timestamp()),
                                           deadline=data_json['deadline'],
                                           activity_time=data_json['activity_time'],
                                           location=data_json['location'],
                                           organizers=data_json['organizers'],
                                           activity_type=data_json['activity_type'],
                                           space_used=data_json['space_used'],
                                           space_available=data_json['space_available']
                                           )
                    return uuid_
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "update":
                try:
                    event = Event.get(data_json["uuid"])
                    if event is None:
                        return "Item not found", 404
                    if current_user.admin or event.uploader_id == current_user.id:  # only admin and same user can modify
                        Event.create_or_update(event=event,
                                               uuid_=data_json['uuid'],
                                               # uploader_id doesnt need to be changed
                                               title=data_json['title'],
                                               image=data_json['image'],
                                               content=data_json['content'],
                                               deadline=data_json['deadline'],
                                               activity_time=data_json['activity_time'],
                                               location=data_json['location'],
                                               organizers=data_json['organizers'],
                                               activity_type=data_json['activity_type'],
                                               space_used=data_json['space_used'],
                                               space_available=data_json['space_available']
                                               )
                        return "OK"
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            elif data_json["operation"] == "delete":
                try:
                    event = Event.get(data_json["uuid"])
                    if event is None:
                        return "Item not found", 404
                    if current_user.admin or current_user.id == event.uploader_id:
                        event.delete()
                        return "OK"
                    else:
                        return "Permission Denied", 403
                except KeyError:
                    return "Missing Info", 400
                except Exception as e:
                    print(e)
                    return "Failed", 500
            else:
                return "Bad Operation", 400
        except KeyError:
            return "Missing Info", 400
        except json.decoder.JSONDecodeError:
            return "Bad json", 400


@app.route("/signups", methods=['GET', 'POST'])
def signups():
    if current_user.ban:
        return 'You are banned, please contact the administrator.', 403
    if request.method == 'GET':
        return 'Pass'
    elif request.method == 'POST':
        return 'POST yet to be implemented'


if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context="adhoc")
