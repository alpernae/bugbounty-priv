from flask import Flask, request

app = Flask(__name__)

@app.get("/profile")
def profile():
    host = request.headers.get("X-Forwarded-Host", request.host)
    html = f'<link rel="canonical" href="https://{host}/profile"><h1>{request.user.email}</h1>'
    return html, {"Cache-Control": "public, max-age=600"}
