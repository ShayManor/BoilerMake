import os

from enums import *
from create_ask_ai import create_ask_ai
from create_requirements import create_requirements
from create_app import create_app
from create_run import create_run
from create_index import create_index


def main(agent: AGENT):
    before = os.getcwd()
    os.chdir(os.path.join(os.getcwd(), agent.path))
    os.system(f"cd {agent.path}")
    os.system(f"mkdir {agent.name}")
    os.system(f"cd {agent.name}")
    os.system(f"mkdir {agent.name}/templates")
    os.chdir(before)
    ask_ai = create_ask_ai(agent.model)
    with open(f"{agent.path}/bread-seller-predictor/ask_ai.py", "w") as file:
        file.write(ask_ai)
    app = create_app(agent.description).replace('```python', '').replace('```', '')
    with open(f"{agent.path}/bread-seller-predictor/app.py", "w") as file:
        file.write(app)

    run = create_run(app)
    with open(f"{agent.path}/bread-seller-predictor/run.sh", "w") as file:
        file.write(run)
    index = create_index(app, agent.description).replace('```html', '').replace('```', '')
    with open(f"{agent.path}/bread-seller-predictor/templates/index.html", "w") as file:
        file.write(index)

    create_requirements(agent.path)


a = AGENT()
a.name = "bread-seller-predictor"
a.description = "A bread seller has a csv of how much bread they sell every day. They need an agent that will take the csv file, let him upload it, and tell him how much bread to product the next day to keep up with demand. This should be simple for the end user and they only need to see the prediction."
a.path = "../../Sample-Agents"
main(a)
