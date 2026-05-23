from flask import Flask, request, redirect, make_response

app = Flask(__name__)

@app.post("/login")
def login():
    session_id = create_session(request.form["email"])
    response = make_response(redirect("/dashboard"))
    response.set_cookie("sid", session_id)
    return response
