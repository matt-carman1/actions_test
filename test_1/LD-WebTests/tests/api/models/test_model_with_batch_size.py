from ldclient.models import ModelCommand, ModelRecursive, ModelTemplateVar
from helpers.api.actions.model import create_model_via_api, update_protocol_via_api, archive_models
from library.utils import make_unique_name

# Protocol data
test_protocol_name = 'Protocol with batch size 12'
test_protocol_commands = [ModelCommand(command='${Length:TEXT-INPUT}', driver_id='1')]
test_protocol_template_vars = [
    ModelTemplateVar(tag='DEFAULT', type='STRING', name='Length', is_optional=False, data="template var data")
]
test_protocol_command_type = ModelRecursive(tag='DEFAULT', value='NORMAL')
test_protocol_batch_size = ModelRecursive(tag='DEFAULT', value=12)


def test_model_with_batch_size(ld_api_client, new_protocol_via_api):
    """
    Test Create and Update model with batch size.

    1. Create Model with batch size same as protocol and verify batch size for protocol and model
    2. Update Protocol batch size and verify Model batch size changed as per Protocol batch size
    3. Update model with new batch size and verify model batch size changed properly

    :param ld_api_client: LDClient, ldclient object
    :param new_protocol_via_api: Model, protocol object
    """
    # ----- Create Model with batch size same as protocol and verify batch size for protocol and model ----- #
    model_obj = create_model_via_api(ld_api_client,
                                     make_unique_name('Model with batch size 12'),
                                     'description',
                                     folder=new_protocol_via_api.folder,
                                     parent=new_protocol_via_api.id,
                                     command_type=new_protocol_via_api.command_type,
                                     batch_size=ModelRecursive(tag='PASS'))

    # Verify Model batch size and protocol batch size is 12
    assert model_obj.as_merged.batch_size.as_dict() == test_protocol_batch_size.as_dict()

    # ----- Update Protocol batch size and verify Model batch size changed as per Protocol batch size ----- #
    # new batch size
    new_protocol_batch_size = ModelRecursive(tag='DEFAULT', value=13)
    # update protocol batch size with 13
    new_protocol_via_api.batch_size = new_protocol_batch_size
    new_protocol_obj = update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)

    # Verify protocol batch size and model batch size changed to updated value
    new_model_obj = ld_api_client.model(model_obj.id)
    assert new_protocol_obj.batch_size.as_dict() == new_protocol_batch_size.as_dict()
    assert new_model_obj.as_merged.batch_size.as_dict() == new_protocol_batch_size.as_dict()

    # ----- Update model with new batch size and verify model batch size changed properly ----- #
    model_batch_size = ModelRecursive(tag='DEFAULT', value=20)
    new_model_obj.batch_size = model_batch_size
    updated_model = ld_api_client.update_model(new_model_obj.id, new_model_obj)

    # verify model has batch size 20
    assert updated_model.batch_size.as_dict() == model_batch_size.as_dict()
    assert updated_model.as_merged.batch_size.as_dict() == model_batch_size.as_dict()
    # verify protocol batch size is not changed when I update mode batch size
    new_protocol_obj = ld_api_client.get_protocol_by_id(new_protocol_via_api.id)
    assert new_protocol_obj.batch_size.as_dict() == new_protocol_batch_size.as_dict()

    archive_models(ld_api_client, [model_obj])
