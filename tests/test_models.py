from api.project.models import Project


def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check the name field is defined correctly
    """
    project = Project(name="foo")
    assert project.name == "foo"
