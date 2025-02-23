import os
import uuid
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from pymongo import MongoClient
from Agent_Creator.Create_Files.Creator.create_files import main
from Agent_Creator.Create_Files.Creator.enums import AGENT, AI

app = Flask(__name__)

# MongoDB connection (unchanged)
MONGO_URI = os.environ.get(
    'MONGO_URI',
    'mongodb+srv://trueflash42:dOKpvn6cqAyK7RHb@agent.ctwv3.mongodb.net/boilermake25?retryWrites=true&w=majority&appName=Agent'
)
AI_CHOOSER_ID = "asst_OaEmnm4mjh7qAfIZXInJxTjf"
QUESTION_ASKER_ID = "asst_TlqR8FmQyvlUwkosUpu9Alk5"

# Global dictionary to store conversation data.
conversation_data = {}


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
    return ""


try:
    client = MongoClient(MONGO_URI)
    print("Successfully connected to MongoDB Atlas!")
    db = client['boilermake25']
    agents_collection = db['agents']
except Exception as e:
    print("Error connecting to MongoDB:", e)
    agents_collection = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/discover')
def discover():
    return render_template('discover.html')


@app.route('/create')
def create_page():
    return render_template('create.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/support')
def support():
    return render_template('support.html')


# Endpoint to start the agent creation conversation.
@app.route('/create_agent', methods=['POST'])
def create_agent():
    try:
        data = request.get_json()
        agent_name = data.get('agentName')
        description = data.get('description')

        if not agent_name or not description:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the agent already exists.
        existing_agent = agents_collection.find_one({'agentName': agent_name})
        if existing_agent:
            message = f"Agent '{agent_name}' already exists."
            status = "exists"
            return jsonify({"status": status, "message": message})

        # Generate a new conversation ID.
        conversation_id = str(uuid.uuid4())
        # Store the initial agent info in our global conversation_data.
        conversation_data[conversation_id] = {
            "agentName": agent_name,
            "description": description
        }

        # Start the conversation by sending the initial prompt (agent name + description).
        initial_prompt = f"Agent Name: {agent_name}\nDescription: {description}\nPlease ask a question to refine the assistant."
        initial_question = gpt(initial_prompt, QUESTION_ASKER_ID)

        return jsonify({"conversationId": conversation_id, "question": initial_question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to continue the conversation.
@app.route('/create_agent/continue', methods=['POST'])
def continue_conversation():
    try:
        data = request.get_json()
        conversation_id = data.get('conversationId')
        chat_log = data.get('chatLog')  # The entire conversation log as a single string.
        if not conversation_id or not chat_log:
            return jsonify({"error": "Missing conversationId or chatLog"}), 400

        # Pass the entire chat log to GPT.
        ai_response = gpt(chat_log, QUESTION_ASKER_ID)
        if ai_response.strip().upper() == "DONE":
            # Retrieve the initial agent info.
            agent_info = conversation_data.get(conversation_id)
            if not agent_info:
                return jsonify({"error": "Conversation data not found"}), 400

            # Create the agent (simulate creation by calling main).
            agent = AGENT()
            agent.name = agent_info["agentName"]
            agent.description = agent_info["description"]
            # You can set additional parameters as needed.
            main(agent)

            # Insert the new agent into MongoDB.
            new_agent = {
                "agentName": agent.name,
                "description": agent.description,
                "modelType": "chatGPT",  # Or other value as needed.
                "flag": "default"
            }
            result = agents_collection.insert_one(new_agent)

            # Remove conversation data.
            del conversation_data[conversation_id]

            return jsonify({"message": "Agent creation complete.", "finished": True})
        else:
            return jsonify({"message": ai_response, "finished": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


@app.route('/api/agents', methods=['GET'])
def get_all_agents():
    try:
        agents = list(agents_collection.find())
        for agent in agents:
            agent['_id'] = str(agent['_id'])
        return jsonify({"agents": agents})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/agents', methods=['GET'])
def agents_page():
    return render_template('agents.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
