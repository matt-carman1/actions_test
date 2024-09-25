# Logging in as userB
test_username = 'userB'
test_password = 'userB'


def test_mpos_present_in_project(ld_api_client):
    """
    Test mpos present in a project using list_mpos ldclient method

    1. List MPOs present in any project which is accessible to the user using list_mpos method.
    2. Verify # of mpos >= 5
    3. List MPOs present in any project which is inaccessible to the user using list_mpos method.
    4. Verify # of mpos >= 0
    5. List MPOs present in any project which is invalid to the user using list_mpos method.
    6. Verify # of mpos = 0
    7. List MPOs present in multiple projects which is accessible to the user using list_mpos method
    8. Verify # of mpos >= 5

    :param ld_api_client: LDClient, ldclient object
    """

    # List MPOs present in project which is accessible to the user using list_mpos method
    # Project_name: 'JS Testing'
    # Verify # of mpos >= 5
    assert len(ld_api_client.list_mpos(project_ids=['4'])) >= 5

    # List MPOs present in project which is inaccessible to the user using list_mpos method
    # Project_name: 'Project A'
    # Verify # of mpos >= 0
    assert len(ld_api_client.list_mpos(project_ids=['2'])) >= 0

    # List MPOs present in project which is invalid to the user using list_mpos method
    # Project_name: 'empty'
    # Verify # of mpos = 0
    assert len(ld_api_client.list_mpos(project_ids=['empty'])) == 0

    # List MPOs present in multiple projects which is accessible to the user using list_mpos method
    # Project_name: 'JS Testing', 'Project A'
    # Verify # of mpos >= 5
    assert len(ld_api_client.list_mpos(project_ids=['4', '2'])) >= 5
