from os import walk
from flask import Flask, Response, json, request
import time
from sqlite3 import connect

app = Flask(__name__)

connection = connect("db/database.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS messages(message, author, time)")
messages = list(
    map(
        lambda x: f"""{{"message": "{x[0]}", "author": "{x[1]}", "time": "{x[2]}"}}""",
        list(cursor.execute("SELECT * FROM messages")),
    )
)


def make_response(data, mimetype=None):
    resp = Response(data, mimetype=mimetype)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    resp.headers["Access-Control-Allow-Headers"] = (
        "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    )
    return resp


def data():
    lastLen = len(messages)
    for msg in messages:
        yield f"data: {msg}\n\n"
    while True:
        while lastLen == len(messages):
            time.sleep(0.01)
        yield f"data: {messages[-1]}\n\n"
        lastLen = len(messages)


@app.route("/msg", methods=["GET"])
def msg():
    return make_response(data(), mimetype="text/event-stream")


@app.route("/post", methods=["POST", "OPTIONS"])
def post():
    global messages
    try:
        message = request.json
    except:
        return make_response(False)
    cursor = connection.cursor()
    values = ",".join(['"' + x + '"' for x in list(message.values())])
    cursor.execute(f"INSERT INTO messages VALUES ({values})")
    connection.commit()
    messages.append(json.dumps(message))
    return make_response(message)


app.run(debug=True)
