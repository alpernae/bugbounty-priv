from flask import Flask, request, jsonify
from urllib.parse import urlparse
import ipaddress
import socket
import requests

app = Flask(__name__)
ALLOWED_HOSTS = {"api.partner.example", "images.example-cdn.com"}

def is_safe_url(raw):
    parsed = urlparse(raw)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        return False
    for result in socket.getaddrinfo(parsed.hostname, 443):
        ip = ipaddress.ip_address(result[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    return True

@app.get("/fetch-preview")
def fetch_preview():
    url = request.args.get("url", "")
    if not is_safe_url(url):
        return jsonify({"error": "blocked upstream"}), 400
    upstream = requests.get(url, timeout=5, allow_redirects=False)
    return jsonify({"status": upstream.status_code})
