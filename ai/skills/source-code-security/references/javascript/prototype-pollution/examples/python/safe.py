from flask import Flask, request, jsonify

app = Flask(__name__)
ALLOWED_KEYS = {"theme", "alerts"}

@app.post("/settings")
def settings():
    body = request.get_json(force=True)
    clean = {k: v for k, v in body.items() if k in ALLOWED_KEYS}
    return jsonify({
        "theme": clean.get("theme", "light"),
        "alerts": clean.get("alerts", {"email": True})
    })
