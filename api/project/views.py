from flask import Blueprint, request, jsonify
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
def get_project_by_id(project_id):
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
def register_project(_):
    data = request.get_json()
    new_project = Project(name=data["name"])
    db.projects.insert_one(vars(new_project))
    return jsonify({"message": "Project created"}), 201


@bp.route("/projects/<project_id>", methods=["DELETE"])
@auth_required
def delete_project(project_id):
    try:
        res = db["projects"].delete_one({"_id": ObjectId(project_id)})
        if res.deleted_count:
            return "Project removed", 200
        else:
            return "Project not found", 404
    except Exception:
        return jsonify({"message": "Delete project by ID failed"}), 500
