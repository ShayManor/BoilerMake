from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


import random
from flask import jsonify
from ask_ai import ask_ai

problems = {
    'easy': [
        {'id': 1, 'question': 'What is 2 + 2?', 'answer': '4'},
        {'id': 2, 'question': 'What is 5 - 3?', 'answer': '2'},
        {'id': 3, 'question': 'What is 6 × 7?', 'answer': '42'}
    ],
    'medium': [
        {'id': 4, 'question': 'Solve for x: 2x + 3 = 7', 'answer': '2'},
        {'id': 5, 'question': 'What is the integral of x dx?', 'answer': '0.5x^2 + C'},
        {'id': 6, 'question': 'Simplify the expression: (3x^2)(2x)', 'answer': '6x^3'}
    ],
    'hard': [
        {'id': 7, 'question': 'Compute the derivative of x^3', 'answer': '3x^2'},
        {'id': 8, 'question': 'Solve the discrete mathematics problem: How many different binary strings of length 5 are there?', 'answer': '32'},
        {'id': 9, 'question': 'Evaluate the limit: lim as x approaches 0 of (sin x)/x', 'answer': '1'}
    ]
}

@app.route("/get_problem", methods=["GET"])
def get_problem():
    difficulty = request.args.get('difficulty', 'medium').lower()
    if difficulty not in problems:
        difficulty = 'medium'
    problem = random.choice(problems[difficulty])
    return jsonify({'id': problem['id'], 'question': problem['question']})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    problem_id = data.get('problem_id')
    user_answer = data.get('answer')
    
    # Find the problem by id
    problem = next((item for sublist in problems.values() for item in sublist if item["id"] == problem_id), None)
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    correct_answer = problem['answer'].strip().lower()
    user_answer_clean = str(user_answer).strip().lower()
    
    if user_answer_clean == correct_answer:
        return jsonify({'correct': True})
    else:
        prompt = f"The user answered '{user_answer}' to the problem: '{problem['question']}'. Explain why this answer is incorrect."
        explanation = ask_ai(prompt)
        return jsonify({'correct': False, 'explanation': explanation})


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
