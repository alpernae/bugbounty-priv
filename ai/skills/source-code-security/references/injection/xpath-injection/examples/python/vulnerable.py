from flask import Flask, request, jsonify
import ldap3

app = Flask(__name__)

@app.get("/directory")
def directory():
    username = request.args.get("user", "")
    server = ldap3.Server("ldap://directory.example")
    conn = ldap3.Connection(server, auto_bind=True)
    search_filter = f"(&(objectClass=person)(uid={username}))"

    conn.search("ou=people,dc=example,dc=com", search_filter, attributes=["mail", "uid"])
    return jsonify([entry.entry_to_json() for entry in conn.entries])
