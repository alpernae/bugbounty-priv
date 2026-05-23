from flask import Flask, request, jsonify
from defusedxml import ElementTree

app = Flask(__name__)

@app.post("/saml/consume")
def consume_saml():
    if b"<!DOCTYPE" in request.data:
        return jsonify({"error": "doctype not allowed"}), 400
    doc = ElementTree.fromstring(request.data)
    name_id = doc.find(".//NameID")
    return jsonify({"user": name_id.text if name_id is not None else None})
