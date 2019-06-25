import os

import flask

from scout_apm.flask import ScoutApm

app = flask.Flask("app")
app.config["PROPAGATE_EXCEPTIONS"] = True


@app.route("/")
def home():
    return "Welcome home."


@app.route("/hello/", methods=["GET", "OPTIONS"], provide_automatic_options=False)
def hello():
    if flask.request.method == "OPTIONS":
        return "Hello Options!"
    return "Hello World!"


@app.route("/crash/")
def crash():
    raise ValueError("BØØM!")  # non-ASCII


# https://docs.scoutapm.com/#flask
ScoutApm(app)
app.config["SCOUT_MONITOR"] = True
app.config["SCOUT_KEY"] = os.environ["SCOUT_KEY"]
app.config["SCOUT_NAME"] = "Test Flask App"
