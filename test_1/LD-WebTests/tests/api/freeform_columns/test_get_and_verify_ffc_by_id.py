import pytest

from requests import RequestException
from ldclient.models import FreeformColumn
from helpers.api.verification.general import verify_error_response

# -- Expected FFC Objects -- #
text_ffc_object = FreeformColumn(id='3589',
                                 name='Text - unpublished',
                                 description=None,
                                 type='TEXT',
                                 value_type=None,
                                 published=False,
                                 live_report_id='1299',
                                 project_id='4',
                                 picklist=False,
                                 values=[],
                                 multiple_values_allowed=False)
attachment_ffc_object = FreeformColumn(id='83066',
                                       name='Test File',
                                       description=None,
                                       type='ATTACHMENT',
                                       value_type=None,
                                       published=False,
                                       live_report_id='2300',
                                       project_id='4',
                                       picklist=False,
                                       values=[],
                                       multiple_values_allowed=False)
# TODO:
# Add more variation of picklist FFC objects.


@pytest.mark.k8s_defect(reason='SS-37881 Expected message: Page Not Found')
@pytest.mark.parametrize(
    'ffc_id, expected_ffc_object, expected_status_code, expected_error_message',
    # Positive data
    [
        ('3589', text_ffc_object, None, None),
        ('83066', attachment_ffc_object, None, None),
        # Negative data
        ('0', None, '400', 'Freeform column with addable column ID 0 does not exist'),
        ('-1', None, '400', 'Freeform column with addable column ID -1 does not exist'),
        ('string', None, '404', 'Page Not Found'),
        (None, None, '404', 'Page Not Found')
    ])
def test_get_and_verify_ffc_by_id(ld_api_client, ffc_id, expected_ffc_object, expected_status_code,
                                  expected_error_message):
    """
    Gets FFC by id and verifies the attributes of the ffc_object.

    :param ld_api_client: LDClient, ldclient.
    :param ffc_id: str, ID for which the FFC to be obtained.
    :param expected_ffc_object: ldclient.models.FreeformColumn, Expected FFC object. None, for negative data.
    :param expected_status_code: str, status code for negative cases. None, for positive data.
    :param expected_error_message: str, expected error message for verification. None, for positive data and negative
                                        data with no expected error message.
    """
    if expected_status_code:
        with pytest.raises(RequestException) as error:
            ld_api_client.get_freeform_column_by_id(ffc_id)
        verify_error_response(error.value, expected_status_code, expected_error_message)
    else:
        actual_ffc_object = ld_api_client.get_freeform_column_by_id(ffc_id)
        assert actual_ffc_object.as_dict() == expected_ffc_object.as_dict()
