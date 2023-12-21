import logging
from bson.objectid import ObjectId
from api.common.models import BaseModel
from api.db.setup import db
from api.exception.models import BadRequestException


class Like(BaseModel):
    def __init__(self, created_by, comment_id, created, last_modified):
        super().__init__(created, last_modified)
        self.created_by = created_by
        self.comment_id = comment_id

    def save_to_database(self):
        if db["likes"].find_one(
            {
                "$and": [
                    {"comment_id": self.comment_id},
                    {"created_by": self.created_by},
                ]
            }
        ):
            raise BadRequestException("Use has already liked comment", status_code=400)
        db.likes.insert_one(vars(self))
        logging.info("Saved like to database")

    @staticmethod
    def is_valid_comment_id(comment_id: str):
        if not (db["comments"].find_one({"_id": ObjectId(comment_id)})):
            raise BadRequestException("Invalid comment ID", status_code=400)
        return comment_id
