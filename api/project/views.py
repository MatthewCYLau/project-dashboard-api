from flask import Blueprint, request, jsonify
import logging
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.user.views import auth_required
from .models import Project

bp = Blueprint("project", __name__)


@bp.route("/projects", methods=(["GET"]))
@auth_required
def get_projects(_):
    projects = list(db["projects"].find({}))
    return generate_response(projects)


@bp.route("/projects/<project_id>", methods=(["GET"]))
@auth_required
def get_project_by_id(_, project_id):
    try:
        project = db["projects"].find_one({"_id": ObjectId(project_id)})
        if project:
            return generate_response(project)
        else:
            return "Project not found", 404
    except Exception:
        return jsonify({"message": "Get project by ID failed"}), 500


@bp.route("/projects", methods=(["POST"]))
@auth_required
def create_project(_):
    data = request.get_json()
    new_project = Project(name=data["name"])
    db.projects.insert_one(vars(new_project))
    return jsonify({"message": "Project created"}), 201


@bp.route("/projects/<project_id>", methods=["DELETE"])
@auth_required
def delete_project_by_id(_, project_id):
    try:
        res = db["projects"].delete_one({"_id": ObjectId(project_id)})
        if res.deleted_count:
            return "Project removed", 200
        else:
            return "Project not found", 404
    except Exception:
        return jsonify({"message": "Delete project by ID failed"}), 500


@bp.route("/projects/<project_id>", methods=["PUT"])
@auth_required
def update_project_by_id(_, project_id):
    data = request.get_json()
    if not data or not data["name"]:
        return jsonify({"message": "Missing field"}), 400
    try:
        res = db["projects"].replace_one({"_id": ObjectId(project_id)}, data, True)
        if res.matched_count:
            return "Project updated", 200
        else:
            return "Project not found", 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update project failed"}), 500
