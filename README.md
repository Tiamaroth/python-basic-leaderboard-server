# python-basic-leaderboard-server
Basic http server that handles a Leaderboard.

Requirements: python 3.5+.

## How to start the server

```
python main.py
```

(depending on your distribution, you might need to use `python3` instead)

Runs by default on 0.0.0.0:8080. You can change it on `main.py` if needed.

## API documentation

### Create a user or set a user's score to a new value

```
POST /update/user/absolute
{ "user": X, "score": Y}
```

Creates user X with score Y if it doesn't exist, or sets user's X score to Y in an absolute way.
This is in constrast with relative score update. X and Y must be two integers.

Example:
```
POST /update/user/absolute
{ "user": 1, "score": 100}

Response:
{"status": "OK"}
```

### Increase or decrease a user's score

```
POST /update/user/relative
{ "user": X, "score": "+/-Y"}
```

Increases user X's score by Y points. X must be an integer, and Y must be a string containing a signed integer.
If Y is negative, user X's score will be decreased by abs(Y) points.

Returns a 404 error if user X does not exist.

Example:
```
POST /update/user/relative
{ "user": 1, "score": "-10"}

Response:
{"status": "OK"}
```

### Get top list

```
GET /top/X
```

Returns a JSON list of the top X users, sorted by score (decreasing) and then id (decreasing). X must be an integer.

Example:

```
GET /top/3

Response:
[{'score': 999, 'user': 158}, {'score': 999, 'user': 84}, {'score': 997, 'user': 590}]
```

### Get partial top range

```
GET /partial/X/Y
```

Retrieves a JSON list of the relative ranking of the users in the following range:
 * Xth user
 * Y users before the Xth user
 * Y users after Xth user

X and Y must be integers.

Note: if the range exceeds the actual number of users, you'll receive less items.
For example, if you have 5 users but asks for `/partial/5/2`, you'll only get the 3rd, 4th and 5th user ;
if you ask for `/partial/20/1` you'll get an empty list.

Example:
```
GET /partial/5/2

Response:
[{'user': 2, 'score': 936}, {'user': 8, 'score': 788}, {'user': 6, 'score': 685}, {'user': 5, 'score': 651}, {'user': 1, 'score': 409}]
```
