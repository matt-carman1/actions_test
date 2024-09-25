import pytest

from ldclient.models import ModelCommand, ModelRecursive, ModelTemplateVar

from helpers.api.actions.model import create_model_via_api, archive_models
from helpers.api.verification.general import verify_error_response
from library.utils import make_unique_name

test_protocol_name = 'Protocol with is_optional as False'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]
test_protocol_automatic_rerun = ModelRecursive(tag='DEFAULT', value=False)
test_protocol_template_vars = [
    ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data="data")
]


def test_is_optional_field_for_models(ld_api_client, new_protocol_via_api):
    """
    Test create model template vars with is_optional as false i.e. mandatory data.

    1. create model with is_optional param False and empty data and verify model created.
    2. update model with data as None using create_or_update model and verify the error message
    3. update model with data as None, is_optional as True and verify no error message

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """
    # ----- create model with is_optional param False and empty data and verify model created ----- #
    model = create_model_via_api(
        ld_api_client,
        make_unique_name('Model with is_optional False and data as Empty initially'),
        'description',
        folder=new_protocol_via_api.folder,
        parent=new_protocol_via_api.id,
        template_vars=[ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data='')])
    assert model, "Model Not created with empty data when is_optional set as False."

    # ----- update model with data as None using create_or_update model and verify the error message ----- #
    model.template_vars = [ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data=None)]
    with pytest.raises(Exception) as error_response:
        ld_api_client.create_or_update_model(model)
    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message="The field 'data' can't be empty as it isn't optional")

    # ----- Update model with data as None, is_optional as True and verify no error message ----- #
    model.template_vars = [ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=True, data=None)]
    model = ld_api_client.update_model(model.id, model)
    assert model, "Model is not updated with is_optional as True and data as None."
    archive_models(ld_api_client, [model])


def test_create_model_with_is_optional_false_and_data_as_none(ld_api_client, new_protocol_via_api):
    """
    create model with is_optional param False and data as None and verify error message

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """
    # ----- create model with is_optional param False and data as None and verify error message ----- #
    with pytest.raises(Exception) as error_response:
        create_model_via_api(
            ld_api_client,
            make_unique_name('Model with is_optional as False and data as None'),
            'description',
            folder=new_protocol_via_api.folder,
            parent=new_protocol_via_api.id,
            template_vars=[ModelTemplateVar(tag='DEFAULT', type='STRING', name='nonce', is_optional=False, data=None)])
    verify_error_response(error_response.value,
                          expected_status_code=400,
                          expected_error_message="The field 'data' can't be empty as it isn't optional")
