from flask import Flask, render_template, request, jsonify
from ask_ai import ask_ai

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/meal_options', methods=['POST'])
def meal_options():
    # Retrieve user dietary preferences and macro goals from the form.
    dietary_pref = request.form.get('dietary_preferences', '')
    macro_goals = request.form.get('macro_goals', '')

    # Build a prompt for the AI to generate meal options.
    prompt = (
        f"Generate 3 simple and easy meal options for someone with these dietary preferences: {dietary_pref} "
        f"and these macro goals: {macro_goals}. Format the answer as a numbered list."
    )

    options = ask_ai(prompt)
    return jsonify({'options': options})


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Retrieve the selected meal option from the form.
    meal_option = request.form.get('meal_option', '')
    prompt = (
        f"Generate a detailed recipe for the meal: {meal_option}. "
        "Include a list of ingredients and step-by-step instructions that are easy to follow."
    )
    recipe = ask_ai(prompt)
    return jsonify({'recipe': recipe})


if __name__ == '__main__':
    app.run(debug=True)
