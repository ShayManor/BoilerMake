from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    # Listen on all interfaces (useful for EC2) on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
