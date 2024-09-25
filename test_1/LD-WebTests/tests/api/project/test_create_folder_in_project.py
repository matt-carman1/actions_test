import pytest
from ldclient.models import Folder
from requests import RequestException

from helpers.api.actions.project import get_folders_in_project, create_folder
from helpers.api.verification.general import verify_error_response
from library import utils


def test_create_folder_in_project(ld_api_client):
    """
    Test Create folder in project

    1. Create folder with proper project, folder name and verify folder created properly.
    2. Create folder with existed folder name in same project and verify the error message.
    3. Create folder with existed folder name in different project and verify folder created.
    4. Create folder with invalid project and verify the error message.

    :param ld_api_client: LDClient object
    """
    # ----- Create folder with proper project and folder name and verify folder created properly ----- #
    folder_name = utils.make_unique_name('API Test folder')
    project_a_project_id = '2'

    # Creating folder in Project A project
    folder = create_folder(ld_api_client, folder_name, project_id=project_a_project_id)
    # verify folder created properly
    verify_created_folder(ld_api_client, folder, folder_name, project_a_project_id)

    # ----- Create folder with existed folder name in same project and verify the error message ----- #
    with pytest.raises(RequestException) as error_response:
        create_folder(ld_api_client, folder_name, project_a_project_id)

    verify_error_response(error_response.value, '400', 'A tag with the same name already exists in this project.')

    # ----- Create folder with existed folder name in different project and verify folder created ----- #
    global_project_id = '0'
    folder = create_folder(ld_api_client, folder_name, project_id=global_project_id)
    verify_created_folder(ld_api_client, folder, folder_name, global_project_id)

    # ----- Create folder with invalid project and verify the error message ----- #
    with pytest.raises(RequestException) as error_response:
        create_folder(ld_api_client, folder_name, project_id="-1")

    verify_error_response(error_response.value, '400', 'Invalid ID value: -1')


def verify_created_folder(ld_client, response, actual_folder_name, actual_project_id):
    """
    Verify folder created properly:
    1. Verify whether folder created with the given name
    2. Verify whether folder created in the given project
    3. check whether created folder present in given project folder list

    :param ld_client: LDClient, ldclient object
    :param response: Folder, response from create_folder method
    :param actual_folder_name: str, name of the folder
    :param actual_project_id: str, id of the project
    """
    assert isinstance(response, Folder), \
        "folder is not created in project_id : {} with folder name:{}, got the error: {}".format(actual_project_id,
                                                                                                 actual_folder_name,
                                                                                                 response)
    assert actual_folder_name == response.name, \
        "Folder name from response is not matched with given folder name. Expected folder name:{}, But got:{}".format(
            actual_folder_name, response.name)
    assert actual_project_id == response.project_id, \
        "Project id from response is not matched with the given project id. Expected project id:{}, But got:{}".format(
            actual_project_id, response.project_id)

    # validating whether created folder present in Project A project
    assert actual_folder_name in get_folders_in_project(ld_client, actual_project_id), \
        "Created folder: {} not present in project:{}".format(actual_folder_name, actual_project_id)
