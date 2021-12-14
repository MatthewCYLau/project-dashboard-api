from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from .models import User

bp = Blueprint("user", __name__)


@bp.route("/users", methods=(["GET"]))
def get_users():
    users = list(db["users"].find({}))
    return generate_response(users)


@bp.route("/users/<user_id>", methods=(["GET"]))
def get_user_by_id(user_id):
    try:
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            return generate_response(user)
        else:
            return "User not found", 404
    except Exception:
        return jsonify({"message": "Get user by ID failed"}), 500


@bp.route("/users", methods=(["POST"]))
def register_user():
    data = request.get_json()
    new_user = User(email=data["email"], password=data["password"])
    db.users.insert_one(vars(new_user))
    return jsonify({"message": "User created"}), 201


@bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        res = db["users"].delete_one({"_id": ObjectId(user_id)})
        if res.deleted_count:
            return "User removed", 200
        else:
            return "User not found", 404
    except Exception:
        return jsonify({"message": "Delete user by ID failed"}), 500
