from flask import Flask, request, Response, jsonify
import ipaddress
import subprocess

app = Flask(__name__)

@app.get("/tools/ping")
def ping():
    host = request.args.get("host", "")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return jsonify({"error": "invalid host"}), 400

    completed = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        timeout=5
    )
    return Response(completed.stdout + completed.stderr, mimetype="text/plain")
