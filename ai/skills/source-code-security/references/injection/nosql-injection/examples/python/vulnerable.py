from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
users = MongoClient()["app"]["users"]

@app.post("/login")
def login():
    body = request.get_json(force=True)
    user = users.find_one({
        "email": body.get("email"),
        "password": body.get("password")
    })

    if not user:
        return jsonify({"error": "invalid login"}), 401
    return jsonify({"id": str(user["_id"]), "email": user["email"]})
