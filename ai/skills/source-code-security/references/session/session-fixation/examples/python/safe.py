from flask import Flask, request, redirect, session

app = Flask(__name__)

@app.post("/login")
def login():
    user = authenticate(request.form["email"], request.form["password"])
    session.clear()
    session.regenerate()
    session["user_id"] = user.id
    session["role"] = user.role
    return redirect("/dashboard")
