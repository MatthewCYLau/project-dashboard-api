import uuid
import logging
from datetime import datetime, timezone
from bson.objectid import ObjectId
from api.common.models import BaseModel
from api.db.setup import db
from api.auth.auth import auth_required
from api.exception.models import BadRequestException


class Comment(BaseModel):
    def __init__(self, body, created_by, project_id, created, last_modified, likes):
        super().__init__(created, last_modified)
        self.body = body
        self.project_id = project_id
        self.created_by = created_by
        self.likes = likes

    @staticmethod
    def is_valid_project_id(project_id: str):
        if not (db["projects"].find_one({"_id": ObjectId(project_id)})):
            raise BadRequestException("Invalid project ID", status_code=400)
        return project_id

    @staticmethod
    @auth_required
    def get_comment_by_id(_, comment_id: uuid.UUID):
        return db["comments"].find_one({"_id": ObjectId(comment_id)})

    @staticmethod
    @auth_required
    def update_comment_by_id(_, comment_id: uuid.UUID, data: dict):
        updated_comment = {
            "$set": {"body": data["body"], "last_modified": datetime.now(timezone.utc)}
        }
        return db["comments"].update_one(
            {"_id": ObjectId(comment_id)}, updated_comment, True
        )

    def save_to_database(self):
        db.comments.insert_one(vars(self))
        logging.info(f"Saved comment to database - {self.body}")
