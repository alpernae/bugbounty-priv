from flask import Flask, request, jsonify

app = Flask(__name__)
ALLOWED_FIELDS = {"total"}

@app.post("/rules/preview")
def preview_rule():
    data = request.get_json(force=True)
    field = data.get("field")
    minimum = float(data.get("min", 0))
    order = {"total": float(data.get("total", 0)), "country": "TR"}

    if field not in ALLOWED_FIELDS:
        return jsonify({"error": "bad field"}), 400
    return jsonify({"result": order[field] > minimum})
