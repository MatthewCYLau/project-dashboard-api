from flask import Blueprint, request, make_response, jsonify
from api.db.setup import db
from api.util.util import generate_response
from .models import User

bp = Blueprint("user", __name__)


@bp.route("/users", methods=(["GET"]))
def get_users():
    users = list(db["users"].find({}))
    return generate_response(users)


@bp.route("/users", methods=(["POST"]))
def register_user():
    data = request.get_json()
    new_user = User(email=data["email"], password=data["password"])
    db.users.insert_one(new_user.to_dictionary())
    return jsonify({"message": "User created"}), 201
