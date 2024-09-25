import pytest
from requests import HTTPError

from library.api.ldclient import get_api_client
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.project import verify_lr_in_project, verify_lr_not_in_project

test_type = "api"


@pytest.mark.parametrize('lr_type, username, password, is_deletion_allowed', [('ReadOnly', 'userA', 'userA', False),
                                                                              ('ReadOnly', 'seurat', 'seurat', True),
                                                                              ('Private', 'userA', 'userA', False),
                                                                              ('Private', 'seurat', 'seurat', True),
                                                                              ('Normal', 'userA', 'userA', False),
                                                                              ('Normal', 'seurat', 'seurat', True)])
def test_delete_lrs_created_by_admin(ld_api_client, new_live_report, lr_type, username, password, is_deletion_allowed):
    """
    Test to check if LR created by Admin user could be deleted by users with different roles

    :param ld_api_client: Fixture which creates API Client
    :param new_live_report: Fixture which creates new LR using API client
    :param lr_type: str, Different LR types - ReadOnly, Private, Normal
    :param username: str, Username for creating a new API Client
    :param password: str, Password for creating a new API Client
    :param is_deletion_allowed: bool, True if user has permission to delete the LR, False otherwise
    """
    lr_id = new_live_report.id
    project_id = new_live_report.project_id
    if lr_type == 'ReadOnly':
        new_live_report.shared_editable = False
    elif lr_type == 'Private':
        new_live_report.is_private = True

    # Creates a API Client with provided username:password
    client = get_api_client(username=username, password=password)

    if is_deletion_allowed:
        client.delete_live_report(live_report_id=lr_id)
        # Verify if the LR is deleted from the project
        verify_lr_not_in_project(ld_api_client, project_id=project_id, live_report_id=lr_id)
    else:
        with pytest.raises(HTTPError) as err_response:
            client.delete_live_report(live_report_id=lr_id)
        verify_error_response(err_response.value, '403', 'Permission denied')
        # Verify if the LR is not deleted from the project
        verify_lr_in_project(ld_api_client, project_id=project_id, live_report_id=lr_id)
