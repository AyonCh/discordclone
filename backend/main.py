import time
from flask import Flask, Response, json, request

app = Flask(__name__)


messages = []


def data():
    lastLen = len(messages)
    for msg in messages:
        yield f"{msg}\n\n"
    while True:
        while lastLen == len(messages):
            time.sleep(0.01)
        yield f"{messages[-1]}\n\n"
        lastLen = len(messages)


@app.route("/msg", methods=["GET"])
def msg():
    return Response(data(), mimetype="text/event-stream")


@app.route("/post", methods=["POST"])
def post():
    print(request.json)
    message = request.json
    messages.append(message)
    return Response(json.dumps(message))


app.run()
