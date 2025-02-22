import datetime
from config import db
from gridfs_manager import store_file, retrieve_file


def store_agent(agent_name, description, model, flags, file_paths):
    """Stores an AI agent and its files in MongoDB."""
    file_entries = [{"filename": fp, "file_id": store_file(fp)} for fp in file_paths]

    agent_data = {
        "name": agent_name,
        "description": description,
        "model": model,
        "flags": flags,
        "files": file_entries,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }

    db.agents.insert_one(agent_data)
    print(f"✅ Stored agent '{agent_name}'.")


def retrieve_agent(agent_name):
    """Retrieves agent files and downloads them."""
    agent = db.agents.find_one({"name": agent_name})
    if not agent:
        print(f"❌ Agent '{agent_name}' not found.")
        return

    for file in agent["files"]:
        retrieve_file(file["file_id"])

    print(f"✅ Retrieved all files for '{agent_name}'.")


def update_agent(agent_name, new_description):
    """Updates an agent's description."""
    result = db.agents.update_one(
        {"name": agent_name},
        {"$set": {"description": new_description, "updated_at": datetime.datetime.utcnow()}}
    )

    if result.matched_count:
        print(f"✅ Updated '{agent_name}'.")
    else:
        print(f"❌ Agent '{agent_name}' not found.")


def delete_agent(agent_name):
    """Deletes an agent and its files."""
    agent = db.agents.find_one({"name": agent_name})
    if not agent:
        print(f"❌ Agent '{agent_name}' not found.")
        return

    for file in agent["files"]:
        db.fs.chunks.delete_many({"files_id": file["file_id"]})
        db.fs.files.delete_one({"_id": file["file_id"]})

    db.agents.delete_one({"name": agent_name})
    print(f"🗑️ Deleted '{agent_name}'.")
