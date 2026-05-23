from flask import Flask, request, Response
import subprocess

app = Flask(__name__)

@app.get("/tools/ping")
def ping():
    host = request.args.get("host", "")
    completed = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=5
    )
    return Response(completed.stdout + completed.stderr, mimetype="text/plain")
