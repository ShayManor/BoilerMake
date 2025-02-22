import os

from flask import Flask, render_template
from flask_cors import *

app = Flask(__name__)
CORS(app)


# Methods go here

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
