from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

@app.post("/webhooks/payment")
def payment_webhook():
    signature = request.headers.get("X-Provider-Signature", "")
    expected = hmac.new(
        os.environ["WEBHOOK_SECRET"].encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        return jsonify({"error": "bad signature"}), 401

    event = request.get_json(force=True)
    mark_invoice_paid(event["invoiceId"], event["amount"])
    return jsonify({"received": True})
