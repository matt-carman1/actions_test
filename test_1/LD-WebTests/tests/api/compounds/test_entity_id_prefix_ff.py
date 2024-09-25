import pytest

from helpers.api.actions.compound import create_compound_through_smiles

LD_PROPERTIES = {'ENTITY_ID_PREFIX': 'VC'}


@pytest.mark.usefixtures('customized_server_config')
def test_entity_id_prefix_ff(ld_api_client):
    """
    Test ENTITY_ID_PREFIX feature flag

    :param ld_api_client: LDClient, ld client object
    """
    compounds_created = create_compound_through_smiles(ld_api_client,
                                                       "resources/test_entity_id_prefix_ff.sdf",
                                                       project_name='JS Testing')
    assert compounds_created[0].startswith('VC')
