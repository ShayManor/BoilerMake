from flask import Flask, render_template, request
from predict import predict_next_sales

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    if request.method == "POST":
        if "file" not in request.files:
            error = "No file part in the request."
        else:
            file = request.files["file"]
            if file.filename == "":
                error = "No file selected."
            elif not file.filename.lower().endswith(".csv"):
                error = "Invalid file type. Please upload a CSV file."
            else:
                prediction = predict_next_sales(file)
    return render_template("index.html", prediction=prediction, error=error)

if __name__ == "__main__":
    # Listen on all interfaces (useful for EC2) on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
