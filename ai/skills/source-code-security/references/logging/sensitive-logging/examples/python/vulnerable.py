import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
log = logging.getLogger("api")

@app.post("/oauth/token")
def token():
    log.info("token request body=%s headers=%s", request.json, dict(request.headers))
    return jsonify({"access_token": issue_token(request.json["code"])})
