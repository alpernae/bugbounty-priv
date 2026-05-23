from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.get("/debug/env")
def debug_env():
    return jsonify(dict(os.environ))

@app.get("/files/<path:name>")
def files(name):
    return send_from_directory(".", name)
