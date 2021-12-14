from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
import os
import jwt
import datetime
import logging
from functools import wraps
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
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(email=data["email"], password=hashed_password)
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


@bp.route("/login", methods=["POST"])
def login_user():

    data = request.get_json()

    if not data or not data["email"] or not data["password"]:
        return jsonify({"message": "User not authorized"}), 401

    user = db["users"].find_one({"email": data["email"]})

    if check_password_hash(user["password"], data["password"]):
        token = jwt.encode(
            {"email": user["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            os.environ.get("JWT_SECRET"),
            algorithm="HS256",
        )
        return jsonify({"token": token})

    return jsonify({"message": "User not authorized"}), 401


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "x-auth-token" in request.headers:
            token = request.headers["x-auth-token"]

        if not token:
            return jsonify({"message": "User not authorized"}), 401

        try:
            data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms="HS256")
            user = db["users"].find_one({"email": data["email"]}, {"password": False})
        except Exception as e:
            logging.error(e)
            return jsonify({"message": "Invalid token"}), 401

        return f(user, *args, **kwargs)

    return decorator
