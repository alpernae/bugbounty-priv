from flask import Flask, request, jsonify
from email_validator import validate_email as validate

app = Flask(__name__)

@app.get("/validate-email")
def validate_email():
    email = request.args.get("email", "")[:254]
    try:
        validate(email)
        return jsonify({"valid": True})
    except Exception:
        return jsonify({"valid": False})
