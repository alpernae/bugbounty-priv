from flask import Flask, request, redirect

app = Flask(__name__)
ALLOWED_PATHS = {"/dashboard", "/settings", "/billing"}

@app.get("/login/callback")
def callback():
    next_url = request.args.get("next", "/dashboard")
    if next_url not in ALLOWED_PATHS:
        next_url = "/dashboard"
    return redirect(next_url)
