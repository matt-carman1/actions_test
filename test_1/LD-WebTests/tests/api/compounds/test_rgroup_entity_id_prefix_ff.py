import pytest

from helpers.api.actions.compound import create_compound_through_smiles

LD_PROPERTIES = {'RGROUP_ENTITY_ID_PREFIX': 'RGV'}


@pytest.mark.usefixtures('customized_server_config')
def test_rgroup_entity_id_prefix_ff(ld_api_client):
    """
    Test RGROUP_ENTITY_ID_PREFIX feature flag

    :param ld_api_client: LDClient, ld client object
    """
    compounds_created = create_compound_through_smiles(ld_api_client,
                                                       "resources/test_rgroup_entity_id_prefix_ff.sdf",
                                                       project_name='JS Testing')
    assert compounds_created[0].startswith('RGV')
