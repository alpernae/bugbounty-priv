# Python analogue: unsafe recursive merge of user JSON into defaults.
from flask import Flask, request, jsonify

app = Flask(__name__)

def merge(dst, src):
    for key, value in src.items():
        if isinstance(value, dict):
            dst[key] = merge(dst.get(key, {}), value)
        else:
            dst[key] = value
    return dst

@app.post("/settings")
def settings():
    defaults = {"theme": "light", "alerts": {"email": True}}
    return jsonify(merge(defaults, request.get_json(force=True)))
