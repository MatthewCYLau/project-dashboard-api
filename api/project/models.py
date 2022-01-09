import uuid
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.common.models import BaseModel
from api.db.setup import db
from api.auth.auth import auth_required


class Project(BaseModel):
    def __init__(self, name, created, created_by, last_modified, project_skills):
        super().__init__(created, last_modified)
        self.name = name
        self.created_by = created_by
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
            {
                "project_id": project_id,
                "skill_id": data["skill_id"],
                "name": data["name"],
            }
        )

    @staticmethod
    @auth_required
    def get_project_skills_by_project_id(_, project_id: uuid.UUID):
        return db["project_skills"].find({"project_id": project_id})

    @staticmethod
    @auth_required
    def remove_project_skills_by_project_id(_, project_id: uuid.UUID):
        return db["project_skills"].delete_many({"project_id": project_id})

    @staticmethod
    @auth_required
    def get_project_skills(_):
        return db["project_skills"].find({})

    @staticmethod
    @auth_required
    def get_project_skills_group_by_name_count(_):
        pipeline = [{"$group": {"_id": "$name", "count": {"$sum": 1}}}]
        return db["project_skills"].aggregate(pipeline)
