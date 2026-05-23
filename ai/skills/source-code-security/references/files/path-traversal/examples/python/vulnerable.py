from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.get("/download")
def download():
    name = request.args.get("file", "")
    path = os.path.join(os.getcwd(), "uploads", name)
    return send_file(path, as_attachment=True)
