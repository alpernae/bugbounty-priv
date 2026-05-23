from flask import Flask, request, redirect
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

@app.post("/billing/card")
def save_billing_card():
    save_card(request.user.id, request.form["token"])
    return redirect("/billing")
