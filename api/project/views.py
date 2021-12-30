from flask import Blueprint, request, jsonify
import logging
import pytz
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.db.setup import db
from api.util.util import generate_response
from api.auth.auth import auth_required
from .models import Project
from api.skill.models import Skill


bp = Blueprint("project", __name__)

GB = pytz.timezone("Europe/London")


@bp.route("/projects", methods=(["GET"]))
@auth_required
def get_projects(_):
    count = int(request.args["count"]) if "count" in request.args else 0
    projects = list(db["projects"].find({}).limit(count))
    for project in projects:
        project_skills = Project.get_project_skills_by_project_id(str(project["_id"]))
        for i in project_skills:
            project["project_skills"].append(i)
    return generate_response(projects)


@bp.route("/projects/<project_id>", methods=(["GET"]))
@auth_required
def get_project_by_id(_, project_id):
    try:
        project = Project.get_project_by_id(project_id)
        if project:
            project_skill = Project.get_project_skills_by_project_id(project_id)
            for i in project_skill:
                project["project_skills"].append(i)
            return generate_response(project)
        else:
            return "Project not found", 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Get project by ID failed"}), 500


@bp.route("/projects", methods=(["POST"]))
@auth_required
def create_project(_):
    data = request.get_json()
    new_project = Project(
        name=data["name"],
        created=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        last_modified=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        project_skills=[],
    )
    res = db.projects.insert_one(vars(new_project))
    if res.inserted_id:
        return jsonify({"project_id": str(res.inserted_id)}), 201
    else:
        return jsonify({"message": "Create project failed"}), 500


@bp.route("/projects/<project_id>", methods=["DELETE"])
@auth_required
def delete_project_by_id(_, project_id):
    try:
        res = db["projects"].delete_one({"_id": ObjectId(project_id)})
        if res.deleted_count:
            return jsonify({"message": "Project deleted"}), 200

        else:
            return jsonify({"message": "Project not found"}), 404
    except Exception:
        return jsonify({"message": "Delete project by ID failed"}), 500


@bp.route("/projects/<project_id>", methods=["PUT"])
@auth_required
def update_project_by_id(_, project_id):
    data = request.get_json()
    if not data or not data["name"]:
        return jsonify({"message": "Missing field"}), 400
    try:
        res = Project.update_project_by_id(project_id=project_id, data=data)
        if res.matched_count:
            return jsonify({"message": "Project updated"}), 200
        else:
            return jsonify({"message": "Project not found"}), 404
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update project failed"}), 500


@bp.route("/projects/<project_id>/project-skills", methods=["PUT"])
@auth_required
def update_project_skill(_, project_id):
    data = request.get_json()
    if not data:
        res = Project.remove_project_skills_by_project_id(project_id=project_id)
        if res.deleted_count:
            return jsonify({"message": "Project skills deleted"}), 200
        else:
            return jsonify({"message": "Delete project skills failed"}), 500
    try:
        res = Project.remove_project_skills_by_project_id(project_id=project_id)
        for i in data:
            if not "skill_id" in i or not "name" in i:
                return jsonify({"message": "Missing field"}), 400
            skill = Skill.get_skill_by_id(i["skill_id"])
            if not skill:
                return jsonify({"message": "Skill has not been created"}), 400
            if skill["name"] != i["name"]:
                return jsonify({"message": "Please enter valid skill name"}), 400
            Project.add_project_skill(project_id=project_id, data=i)
        return jsonify({"message": "Project skills updated"}), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Update project skills failed"}), 500


@bp.route("/project-skills", methods=(["GET"]))
@auth_required
def get_project_skills(_):
    project_skills = list(Project.get_project_skills())
    return generate_response(project_skills)


@bp.route("/project-skills-count", methods=(["GET"]))
@auth_required
def get_project_skills_count(_):
    return jsonify(list(Project.get_project_skills_group_by_name_count()))
