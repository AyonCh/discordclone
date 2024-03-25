from flask import Flask, Response, request, json
from time import sleep

app = Flask(__name__)


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


update = {}
users = {}


def data(id):
    last_len = {}
    for x in update:
        last_len[x] = len(update[x])

    while True:
        for x in last_len:
            if last_len[x] == len(update[x]):
                pass
            else:
                if id == users[x]:
                    yield f"data: {update[x][-1]}\n\n"
                    last_len[x] = len(update[x])
                else:
                    pass


@app.route("/")
def home():
    return "server started"


@app.route("/<id>")
def id(id):
    return make_response(data(id), mimetype="text/eventstream")


@app.route("/<id>", methods=["POST", "OPTIONS"])
def updt(id):
    global update
    try:
        message = request.json
    except:
        return make_response(False)

    if not message:
        return make_response(False)
    update[id].append(message["msg"])
    return make_response(json.dumps(message))


@app.route("/", methods=["POST", "OPTIONS"])
def post():
    global update
    global users
    try:
        message = request.json
    except:
        return make_response(False)

    if not message:
        return make_response(False)

    update[message["db"]] = []
    users[message["db"]] = message["on"]
    return make_response(json.dumps(message))


app.run(debug=True)
