import json
from requests import HTTPError
import pytest
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.project import verify_lr_in_project

test_type = 'api'
livereport_id = '1299'
test_user_one = ("demo", "demo")
test_user_two = ("userB", "userB")


@pytest.mark.parametrize('customized_server_config', [{
    'COPY_LIVE_REPORT_ROLE': 'ALL'
}, {
    'COPY_LIVE_REPORT_ROLE': 'ADMIN'
}, {
    'COPY_LIVE_REPORT_ROLE': 'NONE'
}],
                         indirect=True)
@pytest.mark.parametrize('ld_api_client', [test_user_one, test_user_two], indirect=True)
def test_copy_live_report_role(ld_api_client, customized_server_config):
    """
    Test to verify the feature flag(FF) COPY_LIVE_REPORT_ROLE is working as expected

    :param ld_api_client: Fixture which creates API Client
    :param customized_server_config: Fixture which sets value on FF(Feature Flag).
    """
    privileage = ld_api_client.get_privileges()
    report_role = customized_server_config['COPY_LIVE_REPORT_ROLE']
    if report_role == 'NONE' or (report_role == 'ADMIN' and privileage.get('username', '') == 'userB'):
        with pytest.raises(HTTPError) as err_response:
            ld_api_client.copy_live_report_to_project(live_report_id=livereport_id, destination_project_id='3')
        error_message = 'Forbidden' if report_role == 'NONE' else 'Permission denied'
        verify_error_response(err_response.value, 403, error_message)
    else:
        response = ld_api_client.copy_live_report_to_project(live_report_id=livereport_id, destination_project_id='3')
        live_report_id = json.loads(response.as_json()).get('live_report_id')
        project_id = json.loads(response.as_json()).get('project_id')
        verify_lr_in_project(ld_api_client, project_id, live_report_id)
