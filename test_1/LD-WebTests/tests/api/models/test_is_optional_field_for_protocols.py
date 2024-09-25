import pytest
from ldclient.models import ModelRecursive, ModelTemplateVar, ModelCommand

from helpers.api.actions.model import update_protocol_via_api
from helpers.api.verification.general import verify_error_response

test_protocol_name = 'Protocol with is_optional as False and data as empty initially'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]
test_protocol_automatic_rerun = ModelRecursive(tag='DEFAULT', value=False)
test_protocol_template_vars = [ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data='')]


def test_is_optional_field_for_protocols(ld_api_client, create_model_or_protocol_object):
    """
    Test create model template vars with is_optional as false i.e. mandatory data.

    1. create protocol with is_optional param False and empty data and verify model created.
    2. update protocol with data as None and verify error message.
    3. update protocol with data as None, is_optional as True and verify protocol updated without error.

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param create_model_or_protocol_object: ldclient.models.Model, fixture which creates protocol object
    """
    # ----- create protocol with is_optional param False and empty data and verify model created ----- #
    protocol = ld_api_client.create_protocol(create_model_or_protocol_object)
    assert protocol, "Protocol not created with is_optional as False and data as empty string."

    # ----- update protocol with data as None and verify error message ----- #
    protocol.template_vars = [
        ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data=None)
    ]
    with pytest.raises(Exception) as error_response:
        update_protocol_via_api(ld_api_client, protocol.id, protocol)
    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message="The field 'data' can't be empty as it isn't optional")

    # ----- update protocol with data as None, is_optional as True and verify protocol updated without error ----- #
    protocol.template_vars = [ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=True, data=None)]
    protocol = ld_api_client.create_or_update_protocol(protocol)
    assert protocol, "Protocol not updated with is_optional as true and data as None."


def test_create_protocol_with_is_optional_false_and_data_as_none(ld_api_client, create_model_or_protocol_object):
    """
    create protocol with is_optional param False and data as None and verify error message

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param create_model_or_protocol_object: ldclient.models.Model, fixture which creates protocol object
    """
    # ----- create protocol with is_optional param False and data as None and verify error message ----- #
    # change template vars for protocol
    create_model_or_protocol_object.template_vars = [
        ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data=None)
    ]
    # create protocol
    with pytest.raises(Exception) as error_response:
        ld_api_client.create_protocol(create_model_or_protocol_object)

    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message="The field 'data' can't be empty as it isn't optional")
