from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.get("/fetch-preview")
def fetch_preview():
    url = request.args.get("url", "")
    upstream = requests.get(url, timeout=5)
    return jsonify({
        "status": upstream.status_code,
        "sample": upstream.text[:200]
    })
