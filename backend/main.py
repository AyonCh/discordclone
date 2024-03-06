from flask import Flask, Response, request

app = Flask(__name__)


def data(msg):
    i = 0
    while True:
        if msg:
            yield f"data: {msg}\n\n"
        else:
            yield f"data: {i}\n\n"
        i += 1
        print(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        message = request.get_json()
        msg = message["message"]
    if request.method == "GET":
        return Response(data(msg), mimetype="text/event-stream")
    return "Helo World"


app.run(debug=True)
