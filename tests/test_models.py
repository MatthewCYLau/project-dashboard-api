from datetime import datetime, timezone
from api.project.models import Project


def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check the name field is defined correctly
    """
    project = Project(name="foo", created=datetime.now(timezone.utc), last_modified=datetime.now(timezone.utc))
    assert project.name == "foo"
