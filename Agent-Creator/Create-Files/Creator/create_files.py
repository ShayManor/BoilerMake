import os
import time

from openai import OpenAI

from enums import *
from create_ask_ai import create_ask_ai
from create_requirements import create_requirements
from create_app import create_app
from create_run import create_run
from create_index import create_index

def decide_model(description: str) -> AI:
    client = OpenAI()
    assistant_id = "asst_OaEmnm4mjh7qAfIZXInJxTjf"
    assistant = client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )
    thread = client.beta.threads.create(
        messages=[{"role": "user", "content": description}]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = messages.data[0].content[0].text.value
        options = {
            '1': AI.CLAUDE,
            '2': AI.CHATGPT,
            '3': AI.DEEPSEEK,
        }
        return options[ai_response[0]]

def main(agent: AGENT):
    agent.model = decide_model(agent.description)
    print(agent.model)
    exit(0)
    before = os.getcwd()
    os.chdir(os.path.join(os.getcwd(), agent.path))
    os.system(f"cd {agent.path}")
    os.system(f"mkdir {agent.name}")
    os.system(f"cd {agent.name}")
    os.system(f"mkdir {agent.name}/templates")
    os.chdir(before)
    ask_ai = create_ask_ai(agent.model)
    with open(f"{agent.path}/{agent.name}/ask_ai.py", "w") as file:
        file.write(ask_ai)
    app = create_app(agent.description).replace('```python', '').replace('```', '')
    with open(f"{agent.path}/{agent.name}/app.py", "w") as file:
        file.write(app)

    run = create_run(app).replace('```bash', '').replace('```', '')
    with open(f"{agent.path}/{agent.name}/run.sh", "w") as file:
        file.write(run)
    index = create_index(app, agent.description).replace('```html', '').replace('```', '')
    with open(f"{agent.path}/{agent.name}/templates/index.html", "w") as file:
        file.write(index)

    create_requirements(agent.path, agent.name)

t = time.time()
a = AGENT()
a.name = "vocabulary-teacher"
a.description = "You are a teacher to teach users new words and improve their vocabulary. You will get a long list of hard words (from an api or otherwise generated with the ai) and you will give definitions and test the user with multiple choice questions, explaining when they get something wrong. Also you should have user statistics for the current session that can be shown. Ensure concise explanations."
a.path = "../../Sample-Agents"
main(a)
print(f"Time taken: {time.time() - t}")
