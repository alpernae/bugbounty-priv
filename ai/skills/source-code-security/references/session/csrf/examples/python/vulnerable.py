from flask import Flask, request, redirect

app = Flask(__name__)

@app.post("/billing/card")
def save_billing_card():
    save_card(request.user.id, request.form["token"])
    return redirect("/billing")
