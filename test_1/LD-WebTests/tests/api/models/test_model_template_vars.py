from ldclient.models import ModelReturn, ModelCommand, ModelTemplateVar
from library.utils import make_unique_name
from helpers.api.actions.model import create_model_via_api, archive_models
from helpers.api.verification.model import verify_protocol_model_predictions, verify_template_vars

test_protocol_name = 'Protocol'
canvas_command = "/mnt/schrodinger/utilities/canvasMolDescriptors -isd ${ORIG-SDF-FILE} -fieldAsName Corporate ID " \
                 "-fill , -${Property Argument:TEXT-INPUT} | grep , | sed 's#Name,#Corporate ID,#'"
test_protocol_commands = [ModelCommand(command=canvas_command, driver_id='1')]
test_protocol_predictions = [
    ModelReturn(key="AlogP", type="REAL", display_name="AlogP", units="nm", precision=2, tag="DEFAULT")
]


def test_model_orig_sdf_to_lr(ld_api_client, new_protocol_via_api):
    """
    Testing model data (template_vars) and ORIG-SDF macro for protocols and models

    1. Create a protocol with a command and prediction.
    2. Create a model depending on a protocol.
    3. Update the model data (template_vars) of the model to include dat.
    4. Verify that model template_vars are updated.
    5. Verify that protocol predictions are carried forward to models.
    6. Verify that protocol command_type are carried forward to models.


    :param ld_api_client: LDClient, ldclient object
    :param new_protocol_via_api: Fixture for creating new new protocols
    """

    # ---- Creating a model depending on the protocol ---- #
    orig_sdf_model_with_template_vars = create_model_via_api(ld_api_client,
                                                             make_unique_name('Model_with_orig'),
                                                             'description',
                                                             folder=new_protocol_via_api.folder,
                                                             parent=new_protocol_via_api.id)

    # Updating the model with a new template var, tag= READ_ONLY equates to Set Fixed, and data is passed to the
    # property Argument text field
    test_model_template_vars = ModelTemplateVar(tag="READ_ONLY",
                                                type="STRING",
                                                name="Property Argument",
                                                data="AlogP",
                                                is_optional=False,
                                                optional_parameter_name=None)
    orig_sdf_model_with_template_vars.template_vars[1] = test_model_template_vars
    updated_orig_sdf_model_with_template_vars = ld_api_client.update_model(orig_sdf_model_with_template_vars.id,
                                                                           orig_sdf_model_with_template_vars)

    # Verification of template vars of the updated model
    expected_model_template_vars = orig_sdf_model_with_template_vars.template_vars
    verify_template_vars(test_model_template_vars, expected_model_template_vars[1])
    verify_template_vars(new_protocol_via_api.template_vars[0], expected_model_template_vars[0])

    # Verification that the protocol predictions are carried forward to the model
    verify_protocol_model_predictions(new_protocol_via_api.returns, updated_orig_sdf_model_with_template_vars.returns)

    # Archiving the created models as the fixture also archives protocols and it cannot if there are dependent models
    archive_models(ld_api_client, [updated_orig_sdf_model_with_template_vars])
