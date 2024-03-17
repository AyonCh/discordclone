from flask import Flask, Response, json, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

messages = []


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
    return Response(data(), mimetype="text/event-stream")


@app.route("/post", methods=["POST"])
def post():
    message = request.json
    messages.append(json.dumps(message))
    res = Response(json.dumps(message))
    return res


app.run(debug=True)
