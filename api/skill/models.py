import uuid
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.common.models import BaseModel
from api.db.setup import db
from api.auth.auth import auth_required


class Skill(BaseModel):
    def __init__(self, name, created, last_modified):
        super().__init__(created, last_modified)
        self.name = name

    @staticmethod
    @auth_required
    def get_skill_by_id(_, skill_id: uuid.UUID):
        return db["skills"].find_one({"_id": ObjectId(skill_id)})

    @staticmethod
    @auth_required
    def get_skill_by_name(_, name: str):
        return db["skills"].find_one({"name": name})

    @staticmethod
    @auth_required
    def update_skill_by_id(_, skill_id: uuid.UUID, data: dict):
        updated_skill = {"$set": {"name": data["name"], "last_modified": datetime.now(timezone.utc)}}
        return db["skills"].update_one({"_id": ObjectId(skill_id)}, updated_skill, True)
