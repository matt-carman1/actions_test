import pytest

from helpers.api.actions.project import get_folders_in_project


@pytest.mark.serial
def test_list_folders(ld_api_client):
    """
    Test list folders.

    1. Validating folders for single project(JS Testing)
    2. Validating folders for multiple projects(JS Testing, ProjectB)
    3. Validating folders of list of projects for atleast one invalid project

    :param ld_api_client: LDClient object
    """
    js_testing_project_id = "4"
    project_b_project_id = "3"

    # ----- Validating folders for single project(JS Testing) ----- #
    single_project_folder_names = get_folders_in_project(ld_api_client, js_testing_project_id)
    expected_folder_names_js_testing = [
        'Adv Search', 'Lot Modes', 'MPO', 'Materials Science', 'Plots', 'Selenium Testing', 'Test Sorting'
    ]
    single_project_folder_names.sort()
    assert expected_folder_names_js_testing == single_project_folder_names, \
        "expected folder names for projectB is: {}, But got: {}".format(expected_folder_names_js_testing,
                                                                        single_project_folder_names)

    # ----- Validating folders for multiple projects(JS Testing, ProjectB) ----- #
    multiple_projects_folder_names = get_folders_in_project(ld_api_client, js_testing_project_id, project_b_project_id)
    expected_folder_names_projectb_and_js_testing = expected_folder_names_js_testing + ['General Live Reports']

    # sorting the folder names as the order changes for every run
    multiple_projects_folder_names.sort()
    expected_folder_names_projectb_and_js_testing.sort()

    assert expected_folder_names_projectb_and_js_testing == multiple_projects_folder_names, \
        "Expected folder names for projectB and JS Testing : {}, But got: {}".format(
            expected_folder_names_projectb_and_js_testing, multiple_projects_folder_names)

    # ----- Validating folders of list of projects for atleast one invalid project ----- #
    folder_names = get_folders_in_project(ld_api_client, '-1', js_testing_project_id)
    folder_names.sort()
    assert folder_names == expected_folder_names_js_testing, \
        "Folder names are not matching with expected when we give one of the project id as invalid. Expected folder " \
        "names: {}, but got : {}".format(folder_names, expected_folder_names_js_testing)
