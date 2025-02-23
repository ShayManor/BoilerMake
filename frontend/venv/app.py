import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from pymongo import MongoClient
from Agent_Creator.Create_Files.Creator.create_files import main
from Agent_Creator.Create_Files.Creator.enums import AGENT, AI

app = Flask(__name__)

# Get the Atlas connection string from an environment variable.
MONGO_URI = os.environ.get(
    'MONGO_URI',
    'mongodb+srv://trueflash42:dOKpvn6cqAyK7RHb@agent.ctwv3.mongodb.net/boilermake25?retryWrites=true&w=majority&appName=Agent'
)
AI_CHOOSER_ID = "asst_OaEmnm4mjh7qAfIZXInJxTjf"
QUESTION_ASKER_ID = "asst_TlqR8FmQyvlUwkosUpu9Alk5"


def gpt(prompt: str, assistant_id):
    client = OpenAI()
    assistant = client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )
    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": prompt}]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = messages.data[0].content[0].text.value
        return ai_response


try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    print("Successfully connected to MongoDB Atlas!")
    db = client['boilermake25']
    agents_collection = db['agents']
except Exception as e:
    print("Error connecting to MongoDB:", e)
    agents_collection = None


# Main index page (hero)
@app.route('/')
def index():
    return render_template('index.html')


# New navigation pages (placeholders to be built out further)
@app.route('/discover')
def discover():
    return render_template('discover.html')  # Create a discover.html template

@app.route('/create_agent/continue')
def ask_question():
    gpt("asdf", QUESTION_ASKER_ID)
@app.route('/create')
def create_page():
    return render_template('create.html')  # Create a create.html template


@app.route('/about')
def about():
    return render_template('about.html')  # Create an about.html template


@app.route('/support')
def support():
    return render_template('support.html')  # Create a support.html template


# Endpoint to create an agent (POST from your Create page)
@app.route('/create_agent', methods=['POST'])
def create_agent():
    try:
        data = request.get_json()
        agent_name = data.get('agentName')
        description = data.get('description')
        model_type = data.get('modelType')

        # Validate required fields
        if not agent_name or not description or not model_type:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the agent already exists
        existing_agent = agents_collection.find_one({'agentName': agent_name})
        if existing_agent:
            message = f"Agent '{agent_name}' already exists."
            status = "exists"
        else:
            options = {
                '1': ("CLAUDE", AI.CLAUDE),
                '2': ("GPT", AI.CHATGPT),
                '3': ("DEEPSEEK", AI.DEEPSEEK),
            }
            # model = gpt(options[description], AI_CHOOSER_ID)
            agent = AGENT()
            agent.name = agent_name
            # agent.model = model[1]
            agent.description = description
            # main(agent)

            new_agent = {
                "agentName": agent_name,
                "description": description,
                # "modelType": model[0],
                "modelType": "chatGPT",
                "flag": "default"  # Customize as needed
            }
            result = agents_collection.insert_one(new_agent)
            message = f"Agent '{agent_name}' created successfully with id {result.inserted_id}!"
            status = "success"

        return jsonify({"status": status, "message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to get a single agent by name
@app.route('/agent/<agent_name>', methods=['GET'])
def get_agent(agent_name):
    try:
        agent = agents_collection.find_one({'agentName': agent_name})
        if agent:
            agent['_id'] = str(agent['_id'])
            return jsonify(agent)
        else:
            return jsonify({"error": "Agent not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API endpoint returning all agents (for your agents page)
@app.route('/api/agents', methods=['GET'])
def get_all_agents():
    try:
        agents = list(agents_collection.find())
        for agent in agents:
            agent['_id'] = str(agent['_id'])
        return jsonify({"agents": agents})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Page to display agents (if you have a dedicated template)
@app.route('/agents', methods=['GET'])
def agents_page():
    return render_template('agents.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
