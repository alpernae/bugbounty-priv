from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.get("/invoices")
def invoices():
    status = request.args.get("status", "open")

    with sqlite3.connect("app.db") as db:
        rows = db.execute(
            "SELECT id, total, status FROM invoices WHERE status = ?",
            (status,)
        ).fetchall()

    return jsonify({"invoices": rows})
