import pytest
from ldclient.models import LiveReport
from requests import RequestException


class TestCreateLiveReport:
    """
    Test for Creating Livereport with positive test data and negative test data and Validation.
    """
    # Positive LR Test data(Live report should create)
    lr = LiveReport('PositiveLR', project_id='4', default_rationale='rationale', description='description', active=True)
    lr_with_owner = LiveReport('LR_with_owner', owner='userB')
    lr_with_null_owner = LiveReport('LR with null owner', owner=None)
    lr_with_True_template = LiveReport('LR with template as True', template=True)
    lr_with_non_default_project = LiveReport('LR with non default project', project_id='4')

    # Negative LR Test data (Livereport should not create)
    lr_with_non_user_owner = LiveReport('LR_with_negative_username', owner='invalid_uname')
    lr_with_empty_owner = LiveReport('LR with Empty owner', owner='')
    lr_with_invalid_project_id_int = LiveReport('LR_with_negative_project_id', project_id='-1')
    lr_with_invalid_project_id_str = LiveReport('LR_with_negative_project_id', project_id='invalid')

    @pytest.mark.parametrize("expected_live_report, status_code, expected_owner",
                             [(lr, 'NA', 'demo'), (lr_with_owner, 'NA', 'userB'), (lr_with_null_owner, 'NA', 'demo'),
                              (lr_with_True_template, 'NA', 'demo'), (lr_with_non_user_owner, '403', ''),
                              (lr_with_empty_owner, '403', ''), (lr_with_invalid_project_id_int, '400', ''),
                              (lr_with_invalid_project_id_str, '400', '')])
    def test_create_live_report(self, ld_client, expected_live_report, status_code, expected_owner):
        """
        Test create live report function.

        1. Create Livereport using ldclient.
        2. Verify Response not null and verify Livereport title.
        3. Verify status code if the test fails.
        """
        # ----- Create LiveReport using ldclient ----- #
        response = create_live_report(ld_client, expected_live_report)

        # verification of response code if the test fails
        expected_live_report.owner = expected_owner
        verify_created_live_report(expected_live_report, response, status_code)


def create_live_report(client, live_report):
    """
    Create Live Report using create_live_report function.

    :param client: ldclient
    :param live_report: ldclient.models.LiveReport to create in LD
    :return: ldclient.models.LiveReport and RequestException, LiveReport if successfully created or
                                                                RequestException if unsuccessful
    """
    try:
        response = client.create_live_report(live_report)
    except RequestException as e:
        response = e
    # passing error/Success response in the response
    return response


def verify_created_live_report(expected_livereport, actual_live_report_response, status_code):
    """
    Verifies the LiveReport and response with expected LiveReport

    :param expected_livereport: ldclient.models.LiveReport, expected livereport to be created
    :param actual_live_report_response: ldclient.models.LiveReport or RequestException, actual livereport response
    object for success response otherwise Exception
    :param status_code: string, status code for negative tests
    """
    if status_code != 'NA':
        # validating error for negative test data, should get RequestException for negative testdata.
        assert isinstance(actual_live_report_response, RequestException), \
            "Livereport is created with negative test data: {}".format(expected_livereport)
        # validating error response
        assert str(actual_live_report_response.response) == '<Response [{}]>'.format(status_code)
        return

    # Validating response for positive test data
    assert isinstance(actual_live_report_response, LiveReport), \
        "LR not created with test data: {}, and got error: {}".format(expected_livereport, actual_live_report_response)
    assert actual_live_report_response.title == expected_livereport.title,\
        "LR title is not matching with the response title "
    assert actual_live_report_response.active == expected_livereport.active,\
        "LR active state is not matching with the response active state"
    assert actual_live_report_response.template == expected_livereport.template, \
        "LR template is not matching with the response template "
    assert actual_live_report_response.default_rationale == expected_livereport.default_rationale, \
        "LR default rationale is not matching with the response default rationale "
    assert actual_live_report_response.owner == expected_livereport.owner, \
        "LR owner is not matching with the response owner"
    assert actual_live_report_response.description == expected_livereport.description, \
        "LR description is not matching with the response description "
    assert actual_live_report_response.project_id == expected_livereport.project_id, \
        "LR project id is not matching with the response project id "
