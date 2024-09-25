from helpers.api.actions.model import create_model_via_api, archive_models, update_protocol_via_api
from ldclient.models import ModelRecursive, ModelCommand
from library.utils import make_unique_name

# Protocol data
test_protocol_name = 'Protocol'
test_protocol_commands = [ModelCommand(command='${Hello:NUMERIC-INPUT}', driver_id='1')]
test_protocol_automatic_rerun = ModelRecursive(tag='DEFAULT', value=False)


def test_model_automatic_rerun(ld_api_client, new_protocol_via_api):
    """
    API test to test all configurations of Recalculate models(from the Admin panel GUI)

    a. Create a protocol with automatic_rerun set to false.
    b. Create a model out of the protocol.
    c. Ensure that the model created has automatic_rerun set to false.
    d. Update the protocol to automatic_rerun set to true and subsequently the model
    e. Ensure that the protocol and model has been updated accordingly.
    f. Create another model with automatic_rerun set to None - aka 'Defer to parent' from the same protocol.
    g. Verify the same.
    f. Archive the two models and protocol.


    :param ld_api_client: LDClient, a fixture which creates ldclient object
    :param new_protocol_via_api: ldclient.models.Model, fixture which creates protocol
    """

    # Creating a Model based on the protocol with manual_rerun type
    model_with_manual_rerun = create_model_via_api(ld_api_client,
                                                   make_unique_name('Model_manual_rerun'),
                                                   'description',
                                                   folder=new_protocol_via_api.folder,
                                                   parent=new_protocol_via_api.id,
                                                   automatic_rerun=ModelRecursive(tag='PASS'))

    # Verification that the manual_rerun return type for models and protocols are similar
    assert model_with_manual_rerun.as_merged.automatic_rerun == test_protocol_automatic_rerun.as_dict()

    # Updating the protocol to have automatic_rerun now
    new_protocol_automatic_rerun = ModelRecursive(tag='DEFAULT', value=True)
    new_protocol_via_api.automatic_rerun = new_protocol_automatic_rerun
    updated_protocol = update_protocol_via_api(ld_api_client, new_protocol_via_api.id, new_protocol_via_api)

    # Verification that the return types of both protocols and models have now automatic_rerun type
    model_with_automatic_rerun = ld_api_client.model(model_with_manual_rerun.id)
    assert updated_protocol.automatic_rerun == new_protocol_automatic_rerun.as_dict()
    assert model_with_automatic_rerun.as_merged.automatic_rerun == updated_protocol.automatic_rerun

    # Creating another Model based on the same protocol with rerun type set to "Defer to Parent". We identified via
    # several trials that (tag="PASS", value=None) serves that purpose.
    model_with_defer_to_parent = create_model_via_api(ld_api_client,
                                                      make_unique_name('Model_with_defer_to_parent'),
                                                      'description',
                                                      folder=new_protocol_via_api.folder,
                                                      parent=new_protocol_via_api.id,
                                                      automatic_rerun=ModelRecursive(tag='PASS', value=None))

    # Verification that the new model with rerun type set to "Defer to parent" points to the old protocol params.
    assert model_with_defer_to_parent.as_merged.automatic_rerun == new_protocol_automatic_rerun.as_dict()

    # Archiving the created models as the fixture also archives protocols and it cannot if there are dependent models
    archive_models(ld_api_client, [model_with_automatic_rerun, model_with_defer_to_parent])
