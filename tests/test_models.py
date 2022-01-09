from datetime import datetime, timezone
from api.project.models import Project
from api.skill.models import Skill
from api.user.models import User


def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check the name field is defined correctly
    """
    project = Project(
        name="foo",
        created=datetime.now(timezone.utc),
        created_by="bar",
        last_modified=datetime.now(timezone.utc),
        project_skills=[],
    )
    assert project.name == "foo"
    assert project.created_by == "bar"


def test_new_skill():
    skill = Skill(name="foo", created=datetime.now(timezone.utc), last_modified=datetime.now(timezone.utc))
    assert skill.name == "foo"


def test_new_user():
    user = User(
        "foo@bar.com", "password", False, created=datetime.now(timezone.utc), last_modified=datetime.now(timezone.utc)
    )
    assert user.email == "foo@bar.com"
