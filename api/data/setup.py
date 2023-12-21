import logging
import pytz
from api.skill.models import Skill
from api.user.models import User
from api.db.setup import mongo_client
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

GB = pytz.timezone("Europe/London")

placeholder_skills = ["React", "Python"]


def add_skill(skill_name):
    client = mongo_client()
    db = client["project-dashboard-api"]
    new_skill = Skill(
        name=skill_name,
        created=datetime.now(timezone.utc).astimezone(GB).isoformat(),
        last_modified=datetime.now(timezone.utc).astimezone(GB).isoformat(),
    )
    skill = db["skills"].find_one({"name": skill_name})
    if skill:
        logging.info(f"Skip creating placeholder skill {skill_name} - already exists")
    else:
        db.skills.insert_one(vars(new_skill))
        logging.info(f"Saved skill to database - {skill_name}")


def add_test_user():
    data = {"email": "test@test.com", "password": "Password!23", "name": "test user"}
    client = mongo_client()
    db = client["project-dashboard-api"]
    user = db["users"].find_one({"email": data["email"]})

    if user:
        logging.info(f"Skip creating test user - already exists")

    else:
        test_user = User(
            email=data["email"],
            password=generate_password_hash(data["password"], method="pbkdf2"),
            name=data["name"],
            isEmailVerified=True,  # Test users automatically have email verified
            created=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )
        db["users"].insert_one(vars(test_user))
        logging.info(f"Saved test user to database")


def generate_placeholder_data():
    [add_skill(skill) for skill in placeholder_skills]
    add_test_user()
