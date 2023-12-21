from flask import Blueprint, request, jsonify
import logging
import pytz
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.auth.auth import auth_required
from .models import Comment

bp = Blueprint("comment", __name__)

GB = pytz.timezone("Europe/London")


@bp.route("/comments", methods=(["GET"]))
@auth_required
def get_comments(_):
    project_id = request.args.get("project_id")
    query = (
        {"project_id": Comment.is_valid_project_id(project_id)}
        if request.args.get("project_id")
        else {}
    )
    comments = list(db["comments"].find(query))
    for comment in comments:
        likes = list(db["likes"].find({"comment_id": str(comment["_id"])}))
        for i in likes:
            comment["likes"].append(i)
    return generate_response(comments)


@bp.route("/comments/<comment_id>", methods=(["GET"]))
def get_comment_by_id(comment_id):
    try:
        comment = Comment.get_comment_by_id(comment_id)
        if comment:
            return generate_response(comment)
        else:
            return jsonify({"message": "Comment not found"}), 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Get comment by ID failed"}), 500


@bp.route("/comments", methods=(["POST"]))
@auth_required
def create_comment(user):
    data = request.get_json()
    if not data or not data["body"]:
        return jsonify({"message": "Missing field"}), 400
    new_comment = Comment(
        body=data["body"],
        created=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        created_by=user["_id"],
        last_modified=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        project_id=Comment.is_valid_project_id(data["project_id"]),
        likes=[],
    )
    new_comment.save_to_database()
    return jsonify({"message": "Comment created"}), 201


@bp.route("/comments/<comment_id>", methods=["DELETE"])
@auth_required
def delete_comment_by_id(_, comment_id):
    try:
        res = db["comments"].delete_one({"_id": ObjectId(comment_id)})
        if res.deleted_count:
            return jsonify({"message": "Comment deleted"}), 200
        else:
            return jsonify({"message": "Comment not found"}), 404
    except Exception:
        return jsonify({"message": "Delete comment by ID failed"}), 500


@bp.route("/comments/<comment_id>", methods=["PUT"])
@auth_required
def update_comment_by_id(_, comment_id):
    data = request.get_json()
    if not data or not data["body"]:
        return jsonify({"message": "Missing field"}), 400
    try:
        res = Comment.update_comment_by_id(comment_id=comment_id, data=data)
        if res.matched_count:
            return jsonify({"message": "Comment updated"}), 200
        else:
            return jsonify({"message": "Comment not found"}), 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update skill failed"}), 500
