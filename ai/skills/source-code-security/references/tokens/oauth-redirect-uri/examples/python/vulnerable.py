from flask import Flask, request, redirect

app = Flask(__name__)

@app.get("/login/callback")
def callback():
    next_url = request.args.get("next", "/dashboard")
    return redirect(next_url)
