import os
from flask import Flask
from openai import OpenAI
from pymongo import MongoClient
from app.routes import bp as main_bp


app = Flask(__name__)

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

app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
