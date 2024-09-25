import pytest

# Project name list for project ids: ['Default Restricted Project', 'JS Testing', 'NoMod Testing', 'RestrictedBC']
RESTRICTED_PROJECTS = ['107', '4', '5', '7']


@pytest.mark.smoke
def test_project_access_for_admin(ld_api_client):
    """
    Test whether admin users have access to global project and restricted projects

    :param ld_api_client: API Client
    """
    # Getting project objects for admin user ldclient
    admin_projects = ld_api_client.projects()

    # Extracting global project object from Admin project objects
    admin_global_projects = [p for p in admin_projects if p.id == '0']
    # Verify admin have access to global project
    assert len(admin_global_projects) == 1, "Global project not available for admin users."

    # Extracting restricted project objects from Admin project objects
    admin_restricted_projects = [p for p in admin_projects if p.id in RESTRICTED_PROJECTS]
    # verify admin have access to restricted projects
    assert len(admin_restricted_projects) == len(RESTRICTED_PROJECTS), "Admin don't have access to restricted projects"
