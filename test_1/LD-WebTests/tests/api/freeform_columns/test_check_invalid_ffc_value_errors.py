import pytest
from requests import RequestException

from helpers.api.actions.row import create_observation
from helpers.api.verification.general import verify_error_response


@pytest.mark.parametrize('ffc_id, ffc_value, expected_error_message',
                         [('3590', 'StringOnNumericalFFC', 'Observation value StringOnNumericalFFC is not a number'),
                          ('3590', '4k.5', 'Observation value 4k.5 is not a number'),
                          ('3597', 'StringOnDateFFC', 'Observation value StringOnDateFFC is not a valid date'),
                          ('3597', '1999-13-12', 'Observation value 1999-13-12 is not a valid date'),
                          ('3595', 'StringOnBooleanFFC', 'Observation value StringOnBooleanFFC is not a boolean'),
                          ('3595', 'true ', 'Observation value true  is not a boolean')])
def test_check_invalid_ffc_value_errors(ld_api_client, ffc_id, ffc_value, expected_error_message):
    """
    Test to check the error responses returned when passing invalid values for FFC with different datatypes
    Steps:
    (i) Creating the Observation for the FFC
    (ii) Adding the Observation to the FFC and catching the exception
    (iii) Verifying the returned error code and response

    :param ld_api_client: fixture which creates API Client
    :param ffc_id: str, FFC ID
    :param ffc_value: str, value to be added to the FFC
    :param expected_error_message: str, expected error message for verification
    :return:
    """
    # Creating the Observation for the FFC
    observation = create_observation(project_id='4',
                                     entity_id='CRA-031137',
                                     live_report_id='1299',
                                     addable_column_id=ffc_id,
                                     value=ffc_value)
    # Adding the Observation to the FFC and catching the exception
    with pytest.raises(RequestException) as error:
        ld_api_client.add_freeform_column_values(observations=[observation])
    # Verifying the returned error code and response
    verify_error_response(response=error.value,
                          expected_status_code='400',
                          expected_error_message=expected_error_message)
