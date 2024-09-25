"""
Verifications in the project picker.

TODO: These verifications are very simple and could be inlined into the test.
"""


def verify_project_not_present(projects, project_name):
    """
    Verify that a particular project should not be in the list of project
    elements.

    :param projects: list of elements representing a project in the project
                     picker
    :param project_name: str, the name of the project of interest
    """
    assert project_name not in _get_project_names(projects), 'Project should not be present'


def verify_project_present(projects, project_name):
    """
    Verify that a particular project is present in the list of project elements.

    :param projects: list of elements representing a project in the project
                     picker
    :param project_name: str, the name of the project of interest
    """
    assert project_name in _get_project_names(projects)


def _get_project_names(projects):
    return [project.text for project in projects]
