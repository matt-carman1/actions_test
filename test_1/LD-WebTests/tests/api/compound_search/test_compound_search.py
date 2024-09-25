from urllib.error import HTTPError

from library.api.extended_ldclient.client import ExtendedLDClient
from ldclient.enums import QueryConditionValueType
import pytest

BENZENE_SMILES = "C1=CC=CC=C1"

BENZENE_SDF = """
     RDKit          2D

  0  0  0  0  0  0  0  0  0  0999 V3000
M  V30 BEGIN CTAB
M  V30 COUNTS 6 6 0 0 0
M  V30 BEGIN ATOM
M  V30 1 C -0.866400 -0.499400 0.000000 0
M  V30 2 C -0.865600 0.500600 0.000000 0
M  V30 3 C 0.000800 1.000000 0.000000 0
M  V30 4 C 0.866400 0.499400 0.000000 0
M  V30 5 C 0.865600 -0.500600 0.000000 0
M  V30 6 C -0.000800 -1.000000 0.000000 0
M  V30 END ATOM
M  V30 BEGIN BOND
M  V30 1 2 1 2
M  V30 2 1 2 3
M  V30 3 2 3 4
M  V30 4 1 4 5
M  V30 5 2 5 6
M  V30 6 1 6 1
M  V30 END BOND
M  V30 END CTAB
M  END
$$$$
"""


@pytest.mark.parametrize("query_molecule", [BENZENE_SDF, BENZENE_SMILES])
@pytest.mark.parametrize(
    "search_type",
    [QueryConditionValueType.SIMILARITY, QueryConditionValueType.SUBSTRUCTURE, QueryConditionValueType.EXACT])
@pytest.mark.parametrize("ignore_stereospecific", [True, False])
def test_compound_search(ld_api_client: ExtendedLDClient, query_molecule: str, search_type: QueryConditionValueType,
                         ignore_stereospecific: bool):
    """
    Tests that compound searches can be run successfully with any combination the supported formats & search types.
    Does *not* test whether the results of these searches are scientifically correct.

    :param ld_api_client: LDClient
    :param query_molecule: The query molecule to search on. This could be a variety of formats
    :param search_type: Type of compound search: similarity substructure, exact, etc.
    :param ignore_stereospecific: Whether or not to take stereospecificity into account
    :return:
    """
    try:
        # NOTE(badlato): We really aren't interested in the output of this method.  We avoid
        #  scientific testing here, and just ensure that the search is run successfully.
        ld_api_client.compound_search(query_molecule, search_type)
    except HTTPError as e:
        pytest.fail(
            f"Server error when running {search_type} search with query molecule:\n {query_molecule}\n Stacktrace: {e}")
