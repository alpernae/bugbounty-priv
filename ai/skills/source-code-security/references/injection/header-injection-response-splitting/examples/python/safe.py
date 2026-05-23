from flask import Flask, request, Response
import re

app = Flask(__name__)

@app.get("/download")
def download():
    raw = request.args.get("name", "report.csv")
    filename = re.sub(r"[^a-zA-Z0-9._-]", "_", raw)[:80] or "report.csv"
    response = Response("id,total\n1,42\n", mimetype="text/csv")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
