from flask import Flask, jsonify
from models import Coupon, db

app = Flask(__name__)

@app.post("/coupons/<code>/redeem")
def redeem(code):
    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon or coupon.remaining <= 0:
        return jsonify({"error": "sold out"}), 409

    coupon.remaining -= 1
    db.session.commit()
    return jsonify({"redeemed": True})
