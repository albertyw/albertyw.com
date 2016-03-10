import os

from flask import Flask, render_template, got_request_exception

import rollbar
import rollbar.contrib.flask

import dotenv
root_path = os.path.dirname(os.path.realpath(__file__))+'/../'
dotenv.read_dotenv(os.path.join(root_path, '.env'))
from getenv import env

app = Flask(__name__)


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        'f40c35cdc38a4dba906088d9b327a264',
        # environment name
        env('ENV'),
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/resume")
def resume():
    return render_template("resume.htm")

@app.route("/projects")
def projects():
    return render_template("projects.htm")

@app.route("/contact")
def contact():
    return render_template("contact.htm")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
