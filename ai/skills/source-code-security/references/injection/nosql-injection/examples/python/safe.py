from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash

app = Flask(__name__)
users = MongoClient()["app"]["users"]

@app.post("/login")
def login():
    body = request.get_json(force=True)
    email = str(body.get("email", ""))
    password = str(body.get("password", ""))
    user = users.find_one({"email": email})

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "invalid login"}), 401
    return jsonify({"id": str(user["_id"]), "email": user["email"]})
