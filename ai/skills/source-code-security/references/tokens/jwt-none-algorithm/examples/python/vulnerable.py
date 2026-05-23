from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

@app.get("/admin")
def admin():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    claims = jwt.decode(token, options={"verify_signature": False})

    if claims.get("role") != "admin":
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"admin": True})
