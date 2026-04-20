from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB bağlantısı
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://sekom_admin:Sekom123!@mongodb:27017/techlog_db?authSource=techlog_db")
client = MongoClient(MONGO_URI)
db = client["techlog_db"]

@app.route("/")
def index():
    return jsonify({"mesaj": "Sekom Tech-Log API ayakta!"})

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = list(db.logs.find({}, {"_id": 0}))
    return jsonify(logs)

@app.route("/logs", methods=["POST"])
def add_log():
    data = request.json
    db.logs.insert_one(data)
    return jsonify({"mesaj": "Log eklendi!"}), 201

@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "")
    results = list(db.logs.find(
        {"$or": [
            {"muhendis": {"$regex": keyword, "$options": "i"}},
            {"not": {"$regex": keyword, "$options": "i"}}
        ]},
        {"_id": 0}
    ))
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
