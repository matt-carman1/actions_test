import pytest

# Project name list for project ids: ['Default Restricted Project', 'JS Testing', 'NoMod Testing', 'RestrictedBC']
RESTRICTED_PROJECTS = ['107', '4', '5', '7']
# Non admin credentials for ldclient
test_username = 'userA'
test_password = 'userA'


@pytest.mark.smoke
def test_project_access_for_non_admin(ld_api_client):
    """
    Test whether non admins don't have access to global project and restricted projects
    """
    # Getting non admin project objects
    non_admin_projects = ld_api_client.projects()
    # Non admin ldclient projects with global project
    non_admin_projects_with_global_project = ld_api_client._projects_w_global()

    # Extracting global project objects from non admin project objects
    non_admin_global_projects = [p for p in non_admin_projects if p.id == '0']
    projects_w_global_match = [p for p in non_admin_projects_with_global_project if p.id == '0']
    # Verify whether non admin don't have access to global project
    assert len(non_admin_global_projects) == 0, "Global Project available for non admin users."
    assert len(projects_w_global_match) == 1, "Global project not available when used _project_w_global method."

    # Extracting restricted project objects from non admin project objects
    non_admin_restricted_projects = [p for p in non_admin_projects if (p.id in RESTRICTED_PROJECTS)]
    non_admin_with_global_project_restricted_projects = [
        p for p in projects_w_global_match if (p.id in RESTRICTED_PROJECTS)
    ]
    # Verify non admin don't have access to restricted projects
    assert len(non_admin_restricted_projects) == 0, "Restricted projects available to non-admin users."
    assert len(non_admin_with_global_project_restricted_projects) == 0, \
        "Restricted projects available to non-admins when used _project_w_global api method."
