from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/resume")
def resume():
    return render_template("index.htm")

@app.route("/projects")
def projects():
    return render_template("index.htm")

@app.route("/contact")
def contact():
    return render_template("index.htm")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
