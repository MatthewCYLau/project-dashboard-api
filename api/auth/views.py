from flask import Blueprint
from api.db.setup import client
from .models import User

bp = Blueprint("auth", __name__)


@bp.route("/auth", methods=(["GET"]))
def get_users():
    return "Login user"


@bp.route("/auth", methods=(["POST"]))
def register_user():
    db = client["pytho-gcp"]
    db.users.insert_one({"email": "foo", "password": "bar"})
    return "Register user"
