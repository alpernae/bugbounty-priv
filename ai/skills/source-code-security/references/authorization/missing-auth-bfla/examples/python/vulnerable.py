from flask import Flask, request, jsonify
from models import Invoice

app = Flask(__name__)

@app.get("/api/invoices/<invoice_id>")
def invoice(invoice_id):
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    if not invoice:
        return jsonify({"error": "not found"}), 404
    return jsonify(invoice.to_dict())
