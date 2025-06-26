from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

app = Flask(__name__)

# Mongo config
MONGO_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME", "odisha_rera_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "projects")

# Connect
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/")
def index():
    projects = list(collection.find({}, {"_id": 0}))
    return render_template("index.html", projects=projects)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env var
    app.run(host="0.0.0.0", port=port, debug=True)

