import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing in .env file!")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["test1"]

# Test connection
try:
    client.admin.command("ping")  # Simple ping to check connection
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
