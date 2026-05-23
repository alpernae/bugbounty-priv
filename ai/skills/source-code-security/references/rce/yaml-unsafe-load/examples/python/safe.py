from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

@app.get("/session/restore")
def restore_session():
    blob = request.args.get("state", "")
    session = json.loads(base64.b64decode(blob))
    if not isinstance(session.get("userId"), str):
        return jsonify({"error": "invalid session"}), 400
    return jsonify({"userId": session["userId"], "theme": session.get("theme", "light")})
