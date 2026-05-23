from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/webhooks/payment")
def payment_webhook():
    event = request.get_json(force=True)
    mark_invoice_paid(event["invoiceId"], event["amount"])
    return jsonify({"received": True})
