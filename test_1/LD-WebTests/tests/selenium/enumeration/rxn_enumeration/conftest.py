import pytest
from library.api.extended_ldclient.enums import ReactionInputSourceType
from helpers.api.actions.enumeration import create_new_rxn_via_api
from library.utils import make_unique_name


@pytest.fixture(scope='function')
def create_new_rxn(request, ld_api_client):
    """
    Fixture to create a new hand sketched reaction for reaction enumeration
    :param ld_api_client: LD API client
    :param request: request object with test metadata (from pytest fixture)
    """
    # defining variables used across the test
    rxn_representation = getattr(request.module, 'test_rxn_representation', '')
    rxn_name = getattr(request.module, 'test_rxn_name', 'test_rxn')
    rxn_desc = getattr(request.module, 'test_rxn_desc', '')
    rxn_owner = getattr(request.module, 'test_rxn_owner', 'demo')
    project_id = getattr(request.module, 'test_project_id', '4')
    reactant_classes = getattr(request.module, 'test_reactant_classes', [])
    reactant_keywords = getattr(request.module, 'test_reactant_keywords', [])

    # --------- Using an API method to create a new reaction. ---------- #
    new_rxn_name = make_unique_name(rxn_name)
    new_saved_reaction = create_new_rxn_via_api(ld_api_client,
                                                rxn_name=new_rxn_name,
                                                desc=rxn_desc,
                                                source_type=ReactionInputSourceType.USER_DEFINED,
                                                rxn_representation=rxn_representation,
                                                rxn_owner=rxn_owner,
                                                project_id=project_id,
                                                reactant_classes=reactant_classes,
                                                keywords=reactant_keywords)
    return new_saved_reaction
