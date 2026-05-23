from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

@app.get("/admin")
def admin():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    claims = jwt.decode(
        token,
        key=open("jwt-public.pem").read(),
        algorithms=["RS256"],
        issuer="https://auth.example.com",
        audience="example-api"
    )

    if claims.get("role") != "admin":
        return jsonify({"error": "forbidden"}), 403
    return jsonify({"admin": True})
