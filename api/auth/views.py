from flask import Blueprint, request
from api.db.setup import db
from .models import User

bp = Blueprint("auth", __name__)


@bp.route("/auth", methods=(["GET"]))
def get_users():
    users = list(db["users"].find({}))
    for user in users:
        print(str(user))
    return "Ok"


@bp.route("/auth", methods=(["POST"]))
def register_user():
    data = request.get_json()
    new_user = User(email=data["email"], password=data["password"])
    db.users.insert_one(new_user.to_dictionary())
    return "Register user"
