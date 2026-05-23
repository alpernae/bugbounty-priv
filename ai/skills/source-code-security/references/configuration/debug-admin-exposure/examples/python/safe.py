from flask import Flask, jsonify, send_from_directory
from pathlib import Path

app = Flask(__name__)
PUBLIC_ROOT = Path("public").resolve()

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.get("/files/<path:name>")
def files(name):
    return send_from_directory(PUBLIC_ROOT, Path(name).name)
