import os
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

@app.post("/checkout")
def checkout():
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": request.json["priceId"], "quantity": 1}],
        success_url="https://app.example.com/success"
    )
    return jsonify({"url": session.url})
