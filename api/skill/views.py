from flask import Blueprint, request, jsonify
import logging
import pytz
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.auth.auth import auth_required
from .models import Skill

bp = Blueprint("skill", __name__)

GB = pytz.timezone("Europe/London")


@bp.route("/skills", methods=(["GET"]))
@auth_required
def get_skills(_):
    skills = list(db["skills"].find({}))
    return generate_response(skills)


@bp.route("/skills/<skill_id>", methods=(["GET"]))
def get_skill_by_id(skill_id):
    try:
        skill = Skill.get_skill_by_id(skill_id)
        if skill:
            return generate_response(skill)
        else:
            return "Skill not found", 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Get skill by ID failed"}), 500


@bp.route("/skills", methods=(["POST"]))
@auth_required
def create_skill(_):
    data = request.get_json()
    if not data or not data["name"]:
        return jsonify({"message": "Missing field"}), 400
    skill = Skill.get_skill_by_name(data["name"])
    if skill:
        return jsonify({"message": "Skill already exists"}), 400
    new_skill = Skill(
        name=data["name"],
        created=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        last_modified=datetime.now(timezone.utc).astimezone(GB).isoformat(),
    )
    new_skill.save_to_database()
    return jsonify({"message": "Skill created"}), 201


@bp.route("/skills/<skill_id>", methods=["DELETE"])
@auth_required
def delete_skill_by_id(_, skill_id):
    try:
        res = db["skills"].delete_one({"_id": ObjectId(skill_id)})
        if res.deleted_count:
            return jsonify({"message": "Skill deleted"}), 200
        else:
            return jsonify({"message": "Skill not found"}), 404
    except Exception:
        return jsonify({"message": "Delete skill by ID failed"}), 500


@bp.route("/skills/<skill_id>", methods=["PUT"])
@auth_required
def update_skill_by_id(_, skill_id):
    data = request.get_json()
    if not data or not data["name"]:
        return jsonify({"message": "Missing field"}), 400
    try:
        res = Skill.update_skill_by_id(skill_id=skill_id, data=data)
        if res.matched_count:
            return jsonify({"message": "Skill updated"}), 200
        else:
            return jsonify({"message": "Skill not found"}), 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update skill failed"}), 500
