import pytest
from requests import HTTPError
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.project import verify_lr_in_project
from library.api.ldclient import get_api_client

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}
test_type = 'api'


def test_verify_readonly_lr(ld_api_client, duplicate_live_report):
    """
    API Test to make an LR readonly by demo user and verify error message when LR is updated by non-demo user

    :param ld_api_client: LDClient, ldclient object
    :param duplicate_live_report: fixture which duplicates livereport
    """
    duplicate_live_report.shared_editable = False
    ld_api_client.update_live_report(live_report_id=duplicate_live_report.id, live_report=duplicate_live_report)
    # Non-demo user ldclient object
    user_a_client = get_api_client(username='userA', password='userA')
    # Update LR Title
    duplicate_lr_id = duplicate_live_report.id
    duplicate_live_report.title = 'test'
    with pytest.raises(HTTPError) as err_response:
        user_a_client.update_live_report(live_report_id=duplicate_lr_id, live_report=duplicate_live_report)
    verify_error_response(err_response.value, '403', 'Permission denied')

    # Add a new column (3595 -> Boolean - published)
    with pytest.raises(HTTPError) as err_response:
        user_a_client.add_columns(live_report_id=duplicate_lr_id, addable_columns=[3595])
    verify_error_response(err_response.value, '403', 'Permission denied')

    # Remove an existing column (3937 -> Test RPE Formula)
    with pytest.raises(HTTPError) as err_response:
        user_a_client.remove_columns(live_report_id=duplicate_lr_id, addable_columns=[3937])
    verify_error_response(err_response.value, '403', 'Permission denied')

    # Add a new compound
    with pytest.raises(HTTPError) as err_response:
        user_a_client.add_rows(live_report_id=duplicate_lr_id, rows=['V035625'])
    verify_error_response(err_response.value, '403', 'Permission denied')

    # Remove an existing compound
    with pytest.raises(HTTPError) as err_response:
        user_a_client.remove_rows(live_report_id=duplicate_lr_id, rows=['V055682'])
    verify_error_response(err_response.value, '403', 'Permission denied')

    # Delete the LR
    with pytest.raises(HTTPError) as err_response:
        user_a_client.delete_live_report(live_report_id=duplicate_lr_id)
    verify_error_response(err_response.value, '403', 'Permission denied')
    # Verify if the LR still in the project
    verify_lr_in_project(ld_api_client, project_id='4', live_report_id=duplicate_lr_id)
