from flask import Flask, request, jsonify
from models import User, db

app = Flask(__name__)
ALLOWED_FIELDS = {"display_name", "avatar_url"}

@app.patch("/profile")
def update_profile():
    user = User.query.get(request.user.id)
    body = request.get_json(force=True)
    for key in ALLOWED_FIELDS:
        if key in body:
            setattr(user, key, body[key])
    db.session.commit()
    return jsonify(user.to_dict())
