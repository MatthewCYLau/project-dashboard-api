from flask import Blueprint, request, jsonify
import pytz
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.auth.auth import auth_required
from .models import Like

bp = Blueprint("like", __name__)

GB = pytz.timezone("Europe/London")


@bp.route("/likes", methods=(["GET"]))
@auth_required
def get_likes(_):
    likes = list(db["likes"].find({}))
    return generate_response(likes)


@bp.route("/likes", methods=(["POST"]))
@auth_required
def create_like(user):
    data = request.get_json()
    if not data or not data["comment_id"]:
        return jsonify({"message": "Missing field"}), 400
    new_like = Like(
        created=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        last_modified=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        created_by=user["_id"],
        comment_id=Like.is_valid_comment_id(data["comment_id"]),
    )
    new_like.save_to_database()
    return jsonify({"message": "Like created"}), 201


@bp.route("/likes/<like_id>", methods=["DELETE"])
@auth_required
def delete_like_by_id(_, like_id):
    try:
        res = db["likes"].delete_one({"_id": ObjectId(like_id)})
        if res.deleted_count:
            return jsonify({"message": "Like deleted"}), 200
        else:
            return jsonify({"message": "Like not found"}), 404
    except Exception:
        return jsonify({"message": "Delete like by ID failed"}), 500
