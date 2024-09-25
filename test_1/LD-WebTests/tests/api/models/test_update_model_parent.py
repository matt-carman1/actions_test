from ldclient.models import ModelTemplateVar

from helpers.api.actions.model import create_model_via_api
from helpers.api.verification.model import verify_template_vars
from library import utils


def test_update_model_parent(ld_api_client):
    """
    Test to update parent protocol for model

    1. Create Model with parent protocol
    2. Verify template vars for model same as protocol template vars
    3. Change parent protocol for model
    4. Verify model updated with new parent
    5. Verify template vars for model updated with new parent protocol template vars

    :param ld_api_client: LDClient, ldclient object
    """
    # parent Protocol 'Glide 3D Builder'
    parent_id = 251
    # ----- Create Model with parent protocol ----- #
    model = create_model_via_api(ld_api_client,
                                 utils.make_unique_name('Model'),
                                 'description',
                                 folder='Folder',
                                 parent=parent_id)

    # ----- Verify template vars for model same as protocol template vars ----- #
    protocol_temp_vars = ld_api_client.get_protocol_by_id(parent_id).template_vars
    expected_temp_vars = [
        ModelTemplateVar(name='ligand0', type='FILE', tag=None),
        ModelTemplateVar(name='protein0', type='FILE', tag=None),
        ModelTemplateVar(name='python file', type='FILE', tag=None)
    ]
    model_temp_vars = model.template_vars
    # verify model data fields
    verify_protocol_and_model_temp_vars_with_expected(protocol_temp_vars, model_temp_vars, expected_temp_vars)

    # ----- Change parent protocol for model ----- #
    # Protocol id of 'JS Test Model Pending'
    new_parent_id = 3557

    model.parent = new_parent_id
    updated_model = ld_api_client.update_model(model.id, model)

    # ----- Verify model updated with new parent ----- #
    assert updated_model.parent == new_parent_id, "Parent not changed for model: {}, Expected parent protocol: {}, " \
                                                  "Actual Parent protocol:{} ".format(model.id, new_parent_id,
                                                                                      updated_model.parent)
    # verify model id not changed after update
    assert model.id == updated_model.id, "Model ID changed after model update, Expected Model ID: {}, Actual Model " \
                                         "ID: {}".format(model.id, updated_model.id)

    # ----- Verify template vars for model updated with new parent protocol template vars ----- #
    protocol_temp_vars = ld_api_client.get_protocol_by_id(new_parent_id).template_vars
    expected_temp_vars = [ModelTemplateVar(name='python_script', type='FILE', tag=None)]
    model_temp_vars = updated_model.template_vars
    # verify model data fields
    verify_protocol_and_model_temp_vars_with_expected(protocol_temp_vars, model_temp_vars, expected_temp_vars)


def verify_protocol_and_model_temp_vars_with_expected(protocol_temp_vars, model_temp_vars, expected_temp_vars):
    """
    Verify whether protocol template vars and model template vars match with expected template vars. template vars
    are model data

    :param  protocol_temp_vars: list of ModelTemplateVar, model data for protocol
    :param model_temp_vars: list of ModelTemplateVar, model data for model
    :param expected_temp_vars: list of ModelTemplateVar, expected mode data
    """
    for actual_model_temp_var, actual_protocol_temp_var, expected_temp_var in zip(model_temp_vars, protocol_temp_vars,
                                                                                  expected_temp_vars):
        # verifying model data of protocol with expected model data(for first command)
        verify_template_vars(actual_protocol_temp_var, expected_temp_var)
        # verifying model data of models with protocol model data(for first command)
        verify_template_vars(actual_model_temp_var, expected_temp_var)
