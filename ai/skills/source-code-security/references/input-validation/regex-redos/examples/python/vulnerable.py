import re
from flask import Flask, request, jsonify

app = Flask(__name__)
EMAIL_PATTERN = re.compile(r"^([a-zA-Z0-9_.+-]+)+@(([a-zA-Z0-9-]+)+\.)+[a-zA-Z]{2,}$")

@app.get("/validate-email")
def validate_email():
    email = request.args.get("email", "")
    return jsonify({"valid": bool(EMAIL_PATTERN.match(email))})
