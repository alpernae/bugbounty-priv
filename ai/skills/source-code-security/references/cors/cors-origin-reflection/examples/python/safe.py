from flask import Flask, request, jsonify

app = Flask(__name__)
ALLOWED_ORIGINS = {"https://app.example.com", "https://admin.example.com"}

@app.after_request
def add_cors(response):
    origin = request.headers.get("Origin", "")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
    return response

@app.get("/api/me")
def me():
    return jsonify({"email": request.user.email, "plan": request.user.plan})
