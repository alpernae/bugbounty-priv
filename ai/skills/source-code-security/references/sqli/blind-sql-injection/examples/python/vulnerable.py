from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.get("/invoices")
def invoices():
    status = request.args.get("status", "open")
    sql = f"SELECT id, total, status FROM invoices WHERE status = '{status}'"

    with sqlite3.connect("app.db") as db:
        rows = db.execute(sql).fetchall()

    return jsonify({"invoices": rows})
