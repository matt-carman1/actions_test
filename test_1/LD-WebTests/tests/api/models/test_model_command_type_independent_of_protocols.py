from ldclient.models import (ModelCommand, ModelRecursive, ModelTemplateVar)
from helpers.api.actions.model import create_model_via_api, archive_models, update_protocol_via_api
from library.utils import make_unique_name

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Length:TEXT-INPUT}', driver_id='1')]
test_protocol_template_vars = [
    ModelTemplateVar(tag='DEFAULT', type='STRING', name='Length', is_optional=False, data="template var data")
]
test_protocol_command_type = ModelRecursive(tag='DEFAULT', value='CLICK_TO_RUN')


def test_model_command_type_independent_of_protocols(ld_api_client, new_protocol_via_api):
    """
    API test to test that command type of models are independent of protocols

    a. Created a protocol to have command type CLICK_TO_RUN.
    b. Created a Model with command type NORMAL.
    c. Verified that Model command type and protocol command type is different.
    c. Updated the command type of the protocol to be REALTIME.
    d. Ensured that protocol command type is still different from the Model command type

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """

    # Creating a model based out a protocol with the same command type.
    normal_model_command_type = ModelRecursive(tag='DEFAULT', value='NORMAL')
    normal_model_from_ctr_protocol = create_model_via_api(ld_api_client,
                                                          make_unique_name('Normal_Model_from_'
                                                                           'CTR_Protocol'),
                                                          'description',
                                                          folder=new_protocol_via_api.folder,
                                                          parent=new_protocol_via_api.id,
                                                          command_type=normal_model_command_type)

    # Fetching command_type for the models and protocols
    created_model_command_type = normal_model_from_ctr_protocol.command_type
    protocol_command_type = new_protocol_via_api.command_type

    # Ensuring that the command_type for the models and protocols are as expected.
    assert str(protocol_command_type) != str(created_model_command_type)
    assert str(created_model_command_type) == str(normal_model_command_type)

    # Updating the command type of the protocol to be CLICK TO RUN
    new_protocol_via_api.command_type = ModelRecursive(tag='DEFAULT', value='REALTIME')
    new_protocol = update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)

    # Ensuring that the command_type for the models and protocols are as expected.
    new_protocol_command_type = ModelRecursive(tag='DEFAULT', value='REALTIME')
    updated_protocol_command_type = new_protocol.command_type

    # Ensuring that the command_type for the models and protocols are as expected.
    assert str(new_protocol_command_type) == str(updated_protocol_command_type)
    assert str(created_model_command_type) == str(normal_model_command_type)
    assert str(created_model_command_type) != str(updated_protocol_command_type)

    # Archiving the created models as the fixture also archives protocols and it cannot if there are dependent models
    archive_models(ld_api_client, [normal_model_from_ctr_protocol])
