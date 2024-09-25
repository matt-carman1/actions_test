from ldclient import LDClient

from helpers.api.actions.model import update_protocol_via_api
from helpers.api.verification.general import assert_dicts_equal_except


def test_update_model_with_no_changes(ld_api_client):
    """
    Tests that a no-op update to a model does not change the model
    (i.e. SS-30601 - a bug where we created new IDs for the ModelTemplateVars.)

    :param ld_api_client: LDClient, fixture that returns the ldclient object
    """
    model = ld_api_client.get_model_by_name('XKCD URL')
    ret_model = ld_api_client.update_model(model.id, model)
    assert_dicts_equal_except(model.as_dict(), ret_model.as_dict(), ['updated_at', 'as_merged'])


def test_update_protocol_with_no_changes(ld_api_client):
    """
    Tests that a no-op update to a protocol does not change the protocol
    (i.e. SS-30601 - a bug where we created new IDs for the ModelTemplateVars.)

    :param ld_api_client:  LDClient, fixture that returns the ldclient object
    """

    protocol = ld_api_client.get_protocol_by_id('151')
    ret_protocol = update_protocol_via_api(ld_api_client, protocol.id, protocol_object=protocol)
    assert_dicts_equal_except(protocol.as_dict(), ret_protocol.as_dict(), ['updated_at', 'as_merged'])
