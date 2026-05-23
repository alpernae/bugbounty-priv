from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/checkout")
def checkout():
    cart = load_cart(request.user.id)
    discount = float(request.json.get("discountPercent", 0))
    total = cart.subtotal - (cart.subtotal * discount / 100)
    order = create_order(request.user.id, total=total, discount=discount)
    return jsonify(order.to_dict())
