from flask import Flask, request, send_file, jsonify
from pathlib import Path

app = Flask(__name__)
ROOT = Path("uploads").resolve()

@app.get("/download")
def download():
    name = Path(request.args.get("file", "")).name
    path = (ROOT / name).resolve()
    if ROOT not in path.parents:
        return jsonify({"error": "invalid file"}), 400
    return send_file(path, as_attachment=True)
