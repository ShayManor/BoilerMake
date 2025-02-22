import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file. Please check your configuration.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["test1"]  # Change this to your database name if needed

# Test connection
try:
    client.admin.command("ping")  # Simple ping to check connection
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
