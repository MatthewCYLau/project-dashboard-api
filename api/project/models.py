import uuid
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.common.models import BaseModel
from api.db.setup import db
from api.auth.auth import auth_required


class Project(BaseModel):
    def __init__(self, name, created, last_modified, project_skills):
        super().__init__(created, last_modified)
        self.name = name
        self.project_skills = project_skills

    @staticmethod
    @auth_required
    def get_project_by_id(_, project_id: uuid.UUID):
        return db["projects"].find_one({"_id": ObjectId(project_id)})

    @staticmethod
    @auth_required
    def update_project_by_id(_, project_id: uuid.UUID, data: dict):
        updated_project = {"$set": {"name": data["name"], "last_modified": datetime.now(timezone.utc)}}
        return db["projects"].update_one({"_id": ObjectId(project_id)}, updated_project, True)

    @staticmethod
    @auth_required
    def add_project_skill(_, project_id: uuid.UUID, data: dict):
        return db["project_skills"].insert_one(
            {"skill_id": data["skill_id"], "project_id": project_id, "name": data["name"]}
        )
