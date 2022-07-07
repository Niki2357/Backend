# kent-backend
Kent App Backend

# Usage
- Please read the entire file
- Run app.py
- Running app.py for the first time will create a empty sqlite3 database file
 called lost_and_found
- Access it at port 5000
- ~~If you have trouble logging in, comment out @login_required~~ This is required for the admin features
- Login only work when you access at https://127.0.0.1:5000/ or https://us.joeworld.xyz:5000/ (Google require this)
- Login with Kent email only

# API 
**SHOULD BE UPDATED, IF YOU HAVE API ERRORS PLEASE LET ME KNOW**

Requests and responses are formatted in JSON unless otherwise specified.

Every user is identified by a unique user id from google login services.

Every item entry is identified by a UUID4 generated when creating.

# /user

GET Request: Return a list of user with full info.

POST Request operations:
 - request_info
    - Return a users information, given "user_id"
 - promote
    - admin only, promote another user to be an admin, given "user_id"

Example request and respond:

Request:

```
{
  "operation": "request_info",
  "user_id": 116843363697558615402
}
```

Respond:

```
{
    "email": "yuh22@kent-school.edu",
    "id": "116843363697558615402",
    "name": "Hanjiang (Joe)",
    "profile_pic": "https://lh5.googleusercontent.com/-e9EUFx_aBYs/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuck-1SZbi_jd8wuURigk4L5h7NhNhg/s96-c/photo.jpg",
    "teacher": false
    "admin": true
    "banned": false
}
```

# /lost_and_found
GET Request: Return the full list of lost_and_found entries with full info. (In the future I will implement it to return only the latest n entry)

POST Request operations:
 - create
    - Create a new lost_and_found entries and store into database, responded with the UUID assigned to the new entry 
    or errors in plain text.
 - update
    - Only admin and the original poster can update post details
    - Update info that are given in "uuid", **Must use this full list:**
    ```
   {
        "operation": "update",
        "name": "Wallet",
        "uuid": "ec6e6e7f-5275-4202-8796-68a42cefd716",
        "location": "North Common Room",
        "description": "$400 in it",
        "image": null,
        "completed": false,
        "target_user_id": null,
        "end_time": null
    }
   ```
   - If you get "Missing Info" error here I probably changed the above list, please contact me
 - delete
    - delete a entry given its "uuid", admin permissions or original poster only, returns OK or errors
    
Example request and respond:

Request:

```
{
  "operation": "create",
  "name": "Wallet",
  "lost_or_found": 1,
  "location": "Dining Hall",
  "description": "$100 in it",
  "start_time": 16028148140000,
  "image": null
}
```

Respond:

```
c416055a-357c-4bc3-bea5-edf9b58ab06d
```

# Errors

Mostly standard HTTP error codes

- 500 Failed: Server side error of unknown problem, contact me
- 400 Bad json: the request JSON cannot be decoded due to bad formatting
- 400 Bad operation: The "operation" field of the JSON is not valid
- 400 Missing Info: The request JSON is missing fields necessary to complete the requested operation
- 403 Permission Denied: The current user does not have enough permission to complete the operation
- 403 You are banned
- 404 Item not found: Item not found given the uuid
- 404 User not found: Same story

# Important
- **Remember** to check if **@login_required** is commented anywhere in app.py before deploying
- **Do not leak my API key**

# Deployment
**Actually I never actually deployed it (apparently, it is not finished). In fact, I am not sure how to deploy.**

# Security
Admin permission system is implemented. However, I have no confidence with this application when it's under attack. 
Currently I am unsure if there are any bugs in the admin permission system.

Right now the most urgent need is to limit the amount of request per user in case of a DDoS attack. The code currently 
is completely vulnerable to such attacks.

