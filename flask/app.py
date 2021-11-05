import logging
import os

import flask

from scout_apm.flask import ScoutApm


app = flask.Flask("app")
app.secret_key = "super secret!"
app.config["PROPAGATE_EXCEPTIONS"] = True

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def home():
    return "Welcome home."


@app.route("/hello/", methods=["GET", "OPTIONS"], provide_automatic_options=False)
def hello():
    if flask.request.method == "OPTIONS":
        return "Hello Options!"
    return "Hello World!"


@app.route("/set-session/")
def set_session():
    session_var = flask.session.get("session_var") or 0
    flask.session["session_var"] = session_var + 1
    return "Set session"


@app.route("/crash/")
def crash():
    raise ValueError("BØØM!")  # non-ASCII


# https://docs.scoutapm.com/#flask
ScoutApm(app)
app.config["SCOUT_MONITOR"] = True
app.config["SCOUT_KEY"] = os.environ["SCOUT_KEY"]
app.config["SCOUT_NAME"] = "Test Flask App"
