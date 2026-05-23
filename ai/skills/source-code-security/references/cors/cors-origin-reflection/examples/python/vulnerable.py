from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/api/me")
def me():
    return jsonify({"email": request.user.email, "plan": request.user.plan})
