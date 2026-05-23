from flask import Flask, request, jsonify
import zipfile

app = Flask(__name__)

@app.post("/import")
def import_zip():
    archive = zipfile.ZipFile(request.files["file"].stream)
    archive.extractall("var/imports")
    return jsonify({"imported": True})
