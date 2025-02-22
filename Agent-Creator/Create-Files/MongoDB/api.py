from flask import Flask, request, jsonify
from agent_crud import store_agent, retrieve_agent, update_agent, delete_agent

app = Flask(__name__)

@app.route("/agents", methods=["POST"])
def create_agent():
    data = request.json
    store_agent(
        data["name"],
        data["description"],
        data["model"],
        data["flags"],
        data["files"]
    )
    return jsonify({"message": "Agent created successfully"}), 201

@app.route("/agents/<name>", methods=["GET"])
def get_agent(name):
    retrieve_agent(name)
    return jsonify({"message": f"Agent '{name}' retrieved."})

@app.route("/agents/<name>", methods=["PUT"])
def update_agent_api(name):
    data = request.json
    update_agent(name, data["description"])
    return jsonify({"message": f"Agent '{name}' updated."})

@app.route("/agents/<name>", methods=["DELETE"])
def delete_agent_api(name):
    delete_agent(name)
    return jsonify({"message": f"Agent '{name}' deleted."})

if __name__ == "__main__":
    app.run(debug=True)
