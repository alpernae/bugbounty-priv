from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/rules/preview")
def preview_rule():
    data = request.get_json(force=True)
    order = {"total": float(data.get("total", 0)), "country": "TR"}
    result = eval(data.get("expression", "False"))
    return jsonify({"order": order, "result": result})
