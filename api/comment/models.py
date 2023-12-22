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
    def get_comments(query: dict):
        comments = list(db["comments"].find(query))
        for comment in comments:
            likes = list(db["likes"].find({"comment_id": str(comment["_id"])}))
            for i in likes:
                comment["likes"].append(i)
            if comment["created_by"]:
                comment["created_by"] = db["users"].find_one(
                    {"_id": ObjectId(comment["created_by"])},
                    {"password": False, "isEmailVerified": False},
                )
        return comments

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
