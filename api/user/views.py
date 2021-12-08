import json
from flask import Blueprint, request, jsonify
from bson import json_util
from api.db.setup import db
from .models import User

bp = Blueprint("user", __name__)


@bp.route("/users", methods=(["GET"]))
def get_users():
    users = list(db["users"].find({}))
    return jsonify(json.loads(json_util.dumps(users)))


@bp.route("/users", methods=(["POST"]))
def register_user():
    data = request.get_json()
    new_user = User(email=data["email"], password=data["password"])
    db.users.insert_one(new_user.to_dictionary())
    return "Register user"
