from flask import Flask, jsonify
from models import Coupon, db

app = Flask(__name__)

@app.post("/coupons/<code>/redeem")
def redeem(code):
    updated = Coupon.query.filter(
        Coupon.code == code,
        Coupon.remaining > 0
    ).update({Coupon.remaining: Coupon.remaining - 1})

    if updated != 1:
        return jsonify({"error": "sold out"}), 409
    db.session.commit()
    return jsonify({"redeemed": True})
