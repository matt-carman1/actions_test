import pytest
from ldclient.models import ModelCommand, ModelTemplateVar

from helpers.api.actions.model import update_protocol_via_api
from helpers.api.verification.model import verify_template_vars

# data for creating models under newly created protocol
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Length:TEXT-INPUT}', driver_id='1')]
test_protocol_template_vars = [
    ModelTemplateVar(tag='DEFAULT', type='STRING', name='Length', is_optional=False, data="template var data")
]

# Commands and Expected template vars(as tuple) to update protocol
# ----- commands with different parameter type ----- #
data_with_file_input_command = ([ModelCommand(command='${file input command:FILE-INPUT}', driver_id='1')],
                                [ModelTemplateVar(name='file input command', type='FILE', tag=None)])

data_with_column_input_command = ([ModelCommand(command='${column input command:COLUMN-INPUT}', driver_id='1')],
                                  [ModelTemplateVar(name='column input command', type='COLUMN', tag=None)])

# NOTE (alajmi) With the changes for SS-32215 we return an empty string for any empty data fields
# belonging to template vars that allow multiple values
data_with_multi_columns_input_command = ([
    ModelCommand(command='${multi-column command:MULTI-COLUMN-INPUT}', driver_id='1')
], [ModelTemplateVar(name='multi-column command', type='MULTI_COLUMN', tag=None, data="")])

# ----- command has same name(but different parameter type) as old command ----- #
data_with_command_has_same_name_but_different_type = pytest.param(
    [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')],
    [ModelTemplateVar(name='Hello', type='INTEGER', tag=None)],
    marks=pytest.mark.app_defect(reason='SS-33173'))

# ----- multiple commands ----- #
data_with_multiple_commands = ([
    ModelCommand(command='${first command:TEXT-INPUT}', driver_id='1'),
    ModelCommand(command='${second command:NUMERIC-INPUT}', driver_id='1')
], [
    ModelTemplateVar(name='first command', type='STRING', tag=None),
    ModelTemplateVar(name='second command', type='INTEGER', tag=None)
])

# ----- command with incorrect parameter type ----- #
data_with_command_with_invalid_type = ([ModelCommand(command='${first command:NON-INPUT}', driver_id='1')], [])


@pytest.mark.parametrize('commands, expected_temp_vars', [
    data_with_command_has_same_name_but_different_type, data_with_column_input_command,
    data_with_command_with_invalid_type, data_with_file_input_command, data_with_multi_columns_input_command,
    data_with_multiple_commands
])
def test_update_protocol_changes_dependent_models(ld_api_client, create_models_under_protocol, commands,
                                                  expected_temp_vars):
    """
    Test changing parent protocol effects the dependent models.

    1. Create protocol
    2. Create models under protocol, by giving parent_id as protocol id
    3. Update Protocol command
    4. Verify dependent model template vars changed as per the protocol command change

    :param ld_api_client: LDClient, a fixture which creates ldclient object
    """
    protocol, first_model, second_model = create_models_under_protocol

    # ------ update protocol commands such that one command has same name(and different type) as old command ------ #
    protocol.commands = commands
    updated_protocol = update_protocol_via_api(ld_api_client, protocol.id, protocol)

    # ----- Verify dependent model template vars changed as per the protocol command change ----- #
    # Getting the template vars for updated models and protocol
    model1_temp_vars = ld_api_client.model(first_model.id).template_vars
    model2_temp_vars = ld_api_client.model(second_model.id).template_vars
    protocol_temp_vars = updated_protocol.template_vars

    # verify model data count for protocols and models
    assert len(model1_temp_vars) == len(expected_temp_vars)
    assert len(model2_temp_vars) == len(expected_temp_vars)
    assert len(protocol_temp_vars) == len(expected_temp_vars)

    # verify model data fields
    for i, temp_var in enumerate(expected_temp_vars):
        # verifying model data of protocol with expected model data(for first command)
        verify_template_vars(protocol_temp_vars[i], temp_var)
        # verifying model data of models with protocol model data(for first command)
        verify_template_vars(model1_temp_vars[i], model2_temp_vars[i])
        verify_template_vars(model2_temp_vars[i], protocol_temp_vars[i])
