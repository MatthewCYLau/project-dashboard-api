from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/", methods=(["GET"]))
def get_users():
    return "Login user"
