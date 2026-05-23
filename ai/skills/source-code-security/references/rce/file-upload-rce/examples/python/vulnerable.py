from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.post("/avatar")
def avatar():
    uploaded = request.files["file"]
    destination = os.path.join("public", "uploads", uploaded.filename)
    uploaded.save(destination)
    return jsonify({"publicUrl": f"/uploads/{uploaded.filename}"})
