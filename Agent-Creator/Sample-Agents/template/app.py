from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Write code here

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
