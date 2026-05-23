from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.get("/profile")
def profile():
    html = f'<link rel="canonical" href="https://app.example.com/profile"><h1>{escape(request.user.email)}</h1>'
    return html, {"Cache-Control": "private, no-store"}
