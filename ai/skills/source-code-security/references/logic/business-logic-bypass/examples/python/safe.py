from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/checkout")
def checkout():
    cart = load_cart(request.user.id)
    coupon = validate_coupon(request.user.id, request.json.get("coupon", ""))
    total = calculate_server_side_total(cart, coupon)
    order = create_order(request.user.id, total=total, coupon_id=getattr(coupon, "id", None))
    return jsonify(order.to_dict())
