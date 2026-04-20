from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://sekom_admin:Sekom123!@mongodb:27017/techlog_db?authSource=techlog_db")
client = MongoClient(MONGO_URI)
db = client["techlog_db"]

@app.route("/")
def index():
    return jsonify({"mesaj": "Sekom Tech-Log Hub API v2 Ayakta!"})

@app.route("/logs", methods=["GET"])
def get_logs():
    # Sadece listeleme için resimsiz verileri çekelim (hız için)
    logs = list(db.logs.find({}, {"resim": 0}))
    for log in logs:
        log["_id"] = str(log["_id"])
    return jsonify(logs)

@app.route("/logs/<log_id>", methods=["GET"])
def get_log_detail(log_id):
    from bson.objectid import ObjectId
    log = db.logs.find_one({"_id": ObjectId(log_id)})
    if log:
        log["_id"] = str(log["_id"])
        return jsonify(log)
    return jsonify({"hata": "Kayıt bulunamadı"}), 404

@app.route("/logs", methods=["POST"])
def add_log():
    data = request.json
    # calisan, durum, aciklama ve resim (base64) bekliyoruz
    result = db.logs.insert_one(data)
    return jsonify({"mesaj": "Kayıt eklendi!", "id": str(result.inserted_id)}), 201

@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "")
    results = list(db.logs.find(
        {"$or": [
            {"calisan": {"$regex": keyword, "$options": "i"}},
            {"aciklama": {"$regex": keyword, "$options": "i"}}
        ]},
        {"resim": 0}
    ))
    for r in results:
        r["_id"] = str(r["_id"])
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
