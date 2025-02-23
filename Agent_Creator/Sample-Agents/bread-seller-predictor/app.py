from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


from ask_ai import ask_ai
import pandas as pd
from flask import jsonify

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed."}), 400
    try:
        df = pd.read_csv(file)
        if 'Sales' not in df.columns:
            return jsonify({"error": "CSV must contain 'sales' column."}), 400
        sales = df['Sales'].tolist()
        prompt = f"The following are daily bread sales: {sales}. Predict the number of breads to produce tomorrow to meet demand."
        prediction = ask_ai(prompt)
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "templates/index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
