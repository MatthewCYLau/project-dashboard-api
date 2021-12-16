import uuid
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from api.db.setup import db
from api.auth.auth import auth_required


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save_user_to_db(self):
        self.password = generate_password_hash(self.password, method="sha256")
        res = db.users.insert_one(vars(self))
        return res.inserted_id

    @staticmethod
    @auth_required
    def update_user_by_id(_, user_id: uuid.UUID, data: dict):
        updated_user = {"email": data["email"], "password": generate_password_hash(data["password"], method="sha256")}
        return db["users"].replace_one({"_id": ObjectId(user_id)}, updated_user, True)
