from flask import Flask, request, jsonify
import ldap3
import re

app = Flask(__name__)
SAFE_USER = re.compile(r"^[a-zA-Z0-9._-]{1,40}$")

@app.get("/directory")
def directory():
    username = request.args.get("user", "")
    if not SAFE_USER.fullmatch(username):
        return jsonify({"error": "invalid user"}), 400

    server = ldap3.Server("ldap://directory.example")
    conn = ldap3.Connection(server, auto_bind=True)
    search_filter = "(&(objectClass=person)(uid={}))".format(ldap3.utils.conv.escape_filter_chars(username))

    conn.search("ou=people,dc=example,dc=com", search_filter, attributes=["mail", "uid"])
    return jsonify([entry.entry_to_json() for entry in conn.entries])
