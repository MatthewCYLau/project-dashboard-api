import uuid
from bson.objectid import ObjectId
from api.db.setup import db
from api.user.views import auth_required


class Project:
    def __init__(self, name):
        self.name = name

    @staticmethod
    @auth_required
    def get_project_by_id(_, project_id: uuid.UUID):
        return db["projects"].find_one({"_id": ObjectId(project_id)})
