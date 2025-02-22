from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


from flask import jsonify, session
from flask import Flask, render_template, request, send_from_directory, jsonify, session
from flask_cors import CORS
import random
from ask_ai import ask_ai

app.secret_key = 'your_secret_key_here'

def get_words():
    prompt = "Generate a list of 100 advanced English words with their definitions in JSON format."
    response = ask_ai(prompt)
    try:
        words = response.json()  # Assuming ask_ai returns a response with a .json() method
    except:
        # Fallback parsing if response is plain text
        words = []
        for line in response.split('\n'):
            if line.strip():
                parts = line.split(':', 1)
                if len(parts) == 2:
                    word, definition = parts
                    words.append({'word': word.strip(), 'definition': definition.strip()})
    return words

WORDS = get_words()

def init_stats():
    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'incorrect': 0}

@app.route("/api/get_question", methods=["GET"])
def get_question():
    init_stats()
    word = random.choice(WORDS)
    correct_definition = word['definition']
    choices = [correct_definition]
    wrong_defs = random.sample(
        [w['definition'] for w in WORDS if w['word'] != word['word']],
        3
    )
    choices.extend(wrong_defs)
    random.shuffle(choices)
    session['current_question'] = {'word': word['word'], 'definition': correct_definition}
    return jsonify({'word': word['word'], 'choices': choices})

@app.route("/api/submit_answer", methods=["POST"])
def submit_answer():
    init_stats()
    data = request.get_json()
    answer = data.get('answer')
    current = session.get('current_question')
    if not current:
        return jsonify({'success': False, 'message': 'No active question.'}), 400
    correct_def = current['definition']
    if answer == correct_def:
        session['stats']['correct'] += 1
        message = "Correct!"
    else:
        session['stats']['incorrect'] += 1
        message = f"Incorrect. The correct definition is: {correct_def}"
    session.pop('current_question', None)
    return jsonify({'success': True, 'correct': answer == correct_def, 'message': message})

@app.route("/api/get_stats", methods=["GET"])
def get_stats():
    init_stats()
    return jsonify(session['stats'])


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
