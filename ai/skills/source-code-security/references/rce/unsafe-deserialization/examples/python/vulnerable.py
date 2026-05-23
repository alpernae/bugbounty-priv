from flask import Flask, request, jsonify
import base64
import pickle

app = Flask(__name__)

@app.get("/session/restore")
def restore_session():
    blob = request.args.get("state", "")
    session = pickle.loads(base64.b64decode(blob))
    return jsonify({"userId": session["userId"], "theme": session.get("theme")})
