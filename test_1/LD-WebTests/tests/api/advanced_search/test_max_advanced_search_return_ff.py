import pytest

from helpers.api.actions.compound import compound_search_by_id

LD_PROPERTIES = {'MAX_ADVANCED_SEARCH_RETURN': 5}


@pytest.mark.usefixtures('customized_server_config')
def test_max_advanced_search_return_ff(ld_api_client):
    """
    API test to test the MAX_ADVANCED_SEARCH_RETURN Feature flag.
    Tested 3 use cases:

    1. Set the value of the FF to 5.
    2. Tested that
        a. A search supposed to yield >5 comps, gives only 5.
        b. A search supposed to yield 3 comps, gives 3.
        c. A search supposed to yield exactly 5 comps, gives 5.

    :param ld_api_client: Fixture that returns ldclient object for "demo:demo"
    """

    # search for compounds by id and result in excess results
    compound_ids_excess = compound_search_by_id(ld_api_client, query='CHEMBL*', project_id='0', database_names=['pri'])

    # Verification that only 5 compounds are returned
    assert len(compound_ids_excess) == 5, \
        "Mismatch. Expected {} but got {}".format(5, len(compound_ids_excess))

    # search for compounds by id and result in lesser compounds
    compound_ids_lack = compound_search_by_id(ld_api_client,
                                              query='CRA-03237*',
                                              project_id='0',
                                              database_names=['pri', 'non-pri'])
    # Verification that only 3 compounds are returned
    assert len(compound_ids_lack) == 3, \
        "Mismatch. Expected {} but got {}".format(3, len(compound_ids_lack))

    # search for compounds by id and result in exactly 5 compounds
    compound_ids_exact = compound_search_by_id(ld_api_client,
                                               query='CRA-031*',
                                               project_id='0',
                                               database_names=['pri', 'non-pri'])
    # Verification that exactly 5 compounds are returned.
    assert len(compound_ids_exact) == 5, \
        "Mismatch. Expected {} but got {}".format(5, len(compound_ids_exact))
