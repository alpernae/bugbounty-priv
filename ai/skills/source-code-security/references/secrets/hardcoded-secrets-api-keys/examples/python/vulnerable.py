import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)
stripe.api_key = "sk_live_REDACTED_BUT_REAL_LOOKING_SECRET"

@app.post("/checkout")
def checkout():
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": request.json["priceId"], "quantity": 1}],
        success_url="https://app.example.com/success"
    )
    return jsonify({"url": session.url})
