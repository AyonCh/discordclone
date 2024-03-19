from flask import Flask, Response, json, request
import time

app = Flask(__name__)

messages = []


def make_response(data, mimetype=None):
    if type(data) != str and type(data) in [int, dict, set, bool]:
        data = json.dumps(data)
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
    messages.append(json.dumps(message))
    messages = list(set(messages))
    return make_response(message)


app.run(debug=True)
