from flask import Flask, request, jsonify
from models import User, db

app = Flask(__name__)

@app.patch("/profile")
def update_profile():
    user = User.query.get(request.user.id)
    for key, value in request.get_json(force=True).items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())
