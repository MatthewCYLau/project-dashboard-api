from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.auth.auth import auth_required
import os
import jwt
import logging
from datetime import datetime, timezone, timedelta
from .models import User

bp = Blueprint("user", __name__)


@bp.route("/users", methods=(["GET"]))
def get_users():
    users = list(db["users"].find({}, {"password": False}))
    return generate_response(users)


@bp.route("/users/<user_id>", methods=(["GET"]))
def get_user_by_id(user_id):
    try:
        user = db["users"].find_one({"_id": ObjectId(user_id)}, {"password": False})
        if user:
            return generate_response(user)
        else:
            return "User not found", 404
    except Exception:
        return jsonify({"message": "Get user by ID failed"}), 500


@bp.route("/users", methods=(["POST"]))
def register_user():
    data = request.get_json()
    user = db["users"].find_one({"email": data["email"]})
    if user:
        return jsonify({"message": "Email already registered"}), 400
    new_user = User(
        email=data["email"],
        password=data["password"],
        created=datetime.now(timezone.utc),
        last_modified=datetime.now(timezone.utc),
    )
    if new_user.save_user_to_db():
        return jsonify({"message": "User created"}), 201
    else:
        return jsonify({"message": "Failed to create user"}), 500


@bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        res = db["users"].delete_one({"_id": ObjectId(user_id)})
        if res.deleted_count:
            return jsonify({"message": "User deleted"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception:
        return jsonify({"message": "Delete user by ID failed"}), 500


@bp.route("/auth", methods=["GET"])
@auth_required
def get_auth_user(user):
    return generate_response(user)


@bp.route("/auth", methods=["POST"])
def login_user():

    data = request.get_json()

    if not data or not data["email"] or not data["password"]:
        return jsonify({"errors": [{"message": "User not authorized"}]}), 401

    user = db["users"].find_one({"email": data["email"]})

    if user and check_password_hash(user["password"], data["password"]):
        token = jwt.encode(
            {"email": user["email"], "exp": datetime.utcnow() + timedelta(minutes=30)},
            os.environ.get("JWT_SECRET"),
            algorithm="HS256",
        )
        return jsonify({"token": token})

    return jsonify({"errors": [{"message": "User not authorized"}]}), 401


@bp.route("/users/<user_id>", methods=["PUT"])
@auth_required
def update_user_by_id(current_user, user_id):
    data = request.get_json()
    if not data or not data["email"] or not data["password"]:
        return jsonify({"message": "Missing field"}), 400
    if current_user["email"] != data["email"]:
        user = db["users"].find_one({"email": data["email"]})
        if user:
            return jsonify({"message": "Email already registered"}), 400
    try:
        res = User.update_user_by_id(user_id=user_id, data=data)
        if res.matched_count:
            return jsonify({"message": "User updated"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update project failed"}), 500
