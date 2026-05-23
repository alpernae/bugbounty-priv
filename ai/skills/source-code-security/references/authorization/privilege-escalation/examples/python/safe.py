from flask import Flask, request, jsonify
from models import Invoice
from auth import require_user

app = Flask(__name__)

@app.get("/api/invoices/<invoice_id>")
@require_user
def invoice(invoice_id):
    invoice = Invoice.query.filter_by(
        id=invoice_id,
        organization_id=request.user.organization_id
    ).first()
    if not invoice:
        return jsonify({"error": "not found"}), 404
    return jsonify(invoice.to_dict())
