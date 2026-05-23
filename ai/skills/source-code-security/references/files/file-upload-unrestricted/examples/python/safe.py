from flask import Flask, request, jsonify
from pathlib import Path
import secrets

app = Flask(__name__)
ALLOWED_MIME = {"image/png", "image/jpeg"}
UPLOAD_ROOT = Path("var/uploads").resolve()

@app.post("/avatar")
def avatar():
    uploaded = request.files["file"]
    if uploaded.mimetype not in ALLOWED_MIME:
        return jsonify({"error": "bad file type"}), 400
    name = secrets.token_hex(16) + ".bin"
    uploaded.save(UPLOAD_ROOT / name)
    return jsonify({"fileId": name})
