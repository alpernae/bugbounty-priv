import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
log = logging.getLogger("api")
REDACTED_HEADERS = {"authorization", "cookie"}

@app.post("/oauth/token")
def token():
    safe_headers = {k: "[redacted]" for k in REDACTED_HEADERS if k in request.headers}
    log.info("token request code_present=%s headers=%s", "code" in request.json, safe_headers)
    return jsonify({"access_token": issue_token(request.json["code"])})
