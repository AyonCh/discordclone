from flask import Flask, Response, json, request
import time
from sqlite3 import connect
from utils.generateToken import generate

app = Flask(__name__)

connection = connect("db/database.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS messages(message, author, time)")
# cursor.execute("CREATE TABLE IF NOT EXISTS messages(message, author, time, server)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(username, email, password, PRIMARY KEY(username, email))"
)
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS servers(id INTEGER PRIMARY KEY, name, members)"
# )

# When searching for the list of members, fetch the server from the sql database, parse the members column into a list and start fetching the data of the all the members using a for loop
# for member in members:
#   cursor.execute(f"SELECT * FROM users WHERE username={member}")

messages = list(
    map(
        lambda x: f"""{{"message": "{x[0]}", "author": "{x[1]}", "time": "{x[2]}"}}""",
        list(cursor.execute("SELECT * FROM messages")),
    )
)

# messages = {}
# msgs = list(cursor.execute("SELECT * FROM messages")),
# for msg in range msgs:
#   messages[msg[3]] = [*messages[msg[3]], msg]


def make_response(data, mimetype=None, status=None):
    resp = Response(data, mimetype=mimetype, status=status)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    resp.headers["Access-Control-Allow-Headers"] = (
        "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    )
    return resp


def error(data):
    return json.dumps({"error": data})


# for x in messages:
#   lastlen[x] = len(messages[x])


def data():
    lastLen = len(messages)
    # for msg in messages[id]
    for msg in messages:
        yield f"data: {msg}\n\n"
    while True:
        ## maybe use threading here
        # for x in laslen:
        #   while laslen[x] == len(mesasges[x]):
        #       time.sleep(0.01)
        #   yield f"data: {messages[x][-1]}\n\n"
        #   lastlen[x] = len(messages[x])
        while lastLen == len(messages):
            time.sleep(0.01)
        yield f"data: {messages[-1]}\n\n"
        lastLen = len(messages)


@app.route("/msg", methods=["GET"])
# /msg/id
def msg():
    # data(id)
    return make_response(data(), mimetype="text/event-stream", status=200)


@app.route("/post", methods=["POST", "OPTIONS"])
def post():
    global messages
    try:
        message = request.json
    except:
        return make_response(False)

    if not message:
        return make_response(error("Body empty."), status=204)

    cursor = connection.cursor()
    values = ",".join(['"' + x + '"' for x in list(message.values())])
    cursor.execute(f"INSERT INTO messages VALUES ({values})")
    connection.commit()
    messages.append(json.dumps(message))
    return make_response(message, status=200)


@app.route("/user", methods=["POST", "OPTIONS"])
def user():
    try:
        data = request.json
    except:
        return make_response(False)

    if not data:
        return make_response(error("Body empty."), status=204)

    username, email, password = data.values()

    usernameExists = not not list(
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
    )

    emailExists = not not list(
        cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
    )

    err = []
    if usernameExists:
        err.append("Username already exists")

    if emailExists:
        err.append("Email already exists")

    if err:
        return make_response(error(err), status=409)

    list(
        cursor.execute("INSERT INTO users VALUES (?,?,?)", (username, email, password))
    )
    connection.commit()

    res = make_response(json.dumps({"message": "Registered user."}), status=201)

    res.set_cookie(
        "jwt",
        generate({"username": username, "email": email}),
        httponly=True,
        samesite="strict",
        max_age=30 * 24 * 60 * 60,
    )

    return res


@app.route("/user/auth", methods=["POST", "OPTIONS"])
def auth():
    try:
        data = request.json
    except:
        return make_response(False)

    if not data:
        return make_response(error("Body empty."), status=204)

    email, password = data.values()
    return make_response("hlo")


app.run(debug=True)
