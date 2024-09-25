from functools import reduce
from operator import xor
from typing import Optional, List, Callable, NamedTuple, Dict

import pytest
from ldclient.models import LiveReport

from helpers.api.verification.enumeration import get_products_from_reaction_enumeration_preview, \
    get_products_from_reaction_enumeration_submit
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.enums import OrderType, ReactionInputSourceType, \
    ReactionProductFilterType
from library.api.extended_ldclient.models import Reaction
from library.api.extended_ldclient.requests import ReactionEnumerationData, \
    ReactionEnumerationRequest, Reactant, \
    ReactionProductFilter
from library.utils import make_unique_name, is_k8s

test_type = 'api'


def calc_expected_products_count(reactants: List[List[Reactant]]) -> int:
    """
    Calculates the expected products count, assuming:
     - all reactants are valid
     - each unique combination of reactants creates a unique product
    """
    return reduce(lambda x, y: x * y, [len(r) for r in reactants])


class ReactionParam(NamedTuple):
    """
    Used to construct test parameters for test_reaction_enumeration.
    We use a namedtuple instead of a regular tuple here so that we can set sane defaults for some parameters.
    """
    reaction_name: Optional[str] = None
    reaction_representation: Optional[str] = None
    reactants: List[List[Reactant]] = []
    expected_products_count: Optional[int] = None
    save_reaction: bool = False
    product_filters: List[ReactionProductFilter] = []
    reactant_columns: Dict[int, List[str]] = {}


REACTION_PARAM_NAMES = ReactionParam._fields

HAND_SKETCHED_REACTION_EXAMPLE = ReactionParam(
    reaction_representation="$RXN V3000\n"
    "\n"
    "      Mrv2114  091620211705\n"
    "\n"
    "M  V30 COUNTS 2 1\n"
    "M  V30 BEGIN REACTANT\n"
    "M  V30 BEGIN CTAB\n"
    "M  V30 COUNTS 2 1 0 0 0\n"
    "M  V30 BEGIN ATOM\n"
    "M  V30 1 Br -13.5703 0.2217 0 0\n"
    "M  V30 2 R# -14.904 -0.5483 0 0 RGROUPS=(1 1)\n"
    "M  V30 END ATOM\n"
    "M  V30 BEGIN BOND\n"
    "M  V30 1 1 1 2\n"
    "M  V30 END BOND\n"
    "M  V30 END CTAB\n"
    "M  V30 BEGIN CTAB\n"
    "M  V30 COUNTS 4 3 0 0 0\n"
    "M  V30 BEGIN ATOM\n"
    "M  V30 1 R# -1.044 -1.155 0 0 RGROUPS=(1 2)\n"
    "M  V30 2 B 0.2897 -0.385 0 0\n"
    "M  V30 3 O 0.2897 1.155 0 0\n"
    "M  V30 4 O 1.6232 -1.155 0 0\n"
    "M  V30 END ATOM\n"
    "M  V30 BEGIN BOND\n"
    "M  V30 1 1 2 3\n"
    "M  V30 2 1 1 2\n"
    "M  V30 3 1 2 4\n"
    "M  V30 END BOND\n"
    "M  V30 END CTAB\n"
    "M  V30 END REACTANT\n"
    "M  V30 BEGIN PRODUCT\n"
    "M  V30 BEGIN CTAB\n"
    "M  V30 COUNTS 2 1 0 0 0\n"
    "M  V30 BEGIN ATOM\n"
    "M  V30 1 R# 13.5705 -0.315 0 0 RGROUPS=(1 1)\n"
    "M  V30 2 R# 14.904 0.455 0 0 RGROUPS=(1 2)\n"
    "M  V30 END ATOM\n"
    "M  V30 BEGIN BOND\n"
    ""
    "M  V30 1 1 1 2\n"
    "M  V30 END BOND\n"
    "M  V30 END CTAB\n"
    "M  V30 END PRODUCT\n"
    "M  END",
    reactants=[[Reactant(structure="CBr"), Reactant(structure="CCCCCCCCCCBr")],
               [Reactant(structure="CCB(O)O"), Reactant(structure="CCCCCCCCCCCCCCB(O)O")]])

LOT_SCIENTIST_COLUMN_ID = "28"
LOT_DATE_REGISTERED_COLUMN_ID = "29"
ID_COLUMN_ID = "1226"
TEST_REACTANTS_HALIDES_LIVE_REPORT_ID = "2554"
TEST_REACTANTS_NITRILES_LIVE_REPORT_ID = "2553"
REACTION_PARAMS: Dict[str, ReactionParam] = {
    "user_sketched_not_saved":
        HAND_SKETCHED_REACTION_EXAMPLE,
    "user_sketched_saved":
        ReactionParam(**dict(HAND_SKETCHED_REACTION_EXAMPLE._asdict(), save_reaction=True)),
    "schrodinger_library":
        ReactionParam(reaction_name="Alkylation of amines using alkyl halides",
                      reactants=[[Reactant(structure="CCCCl"),
                                  Reactant(structure="CCCCCBr")],
                                 [Reactant(structure="CCCCN"),
                                  Reactant(structure="CCCCCCCCN")]]),
    "product_filters":
        ReactionParam(
            **dict(HAND_SKETCHED_REACTION_EXAMPLE._asdict(),
                   product_filters=[
                       ReactionProductFilter(type=ReactionProductFilterType.MOLECULAR_WEIGHT, minimum=0.0, maximum=55.0)
                   ],
                   expected_products_count=1)),
    "reactants_from_live_report":
        ReactionParam(reaction_name="2,5-disubstituted tetrazole synthesis",
                      reactants=[[
                          Reactant(id="V055820",
                                   live_report_ids=[TEST_REACTANTS_NITRILES_LIVE_REPORT_ID],
                                   entity_ids=["V055820"],
                                   structure="CC#N")
                      ],
                                 [
                                     Reactant(id="V055828",
                                              live_report_ids=[TEST_REACTANTS_HALIDES_LIVE_REPORT_ID],
                                              entity_ids=["V055828"],
                                              structure="CC(Br)C1=CC=CC=C1O |c:5,7,t:3|")
                                 ]],
                      reactant_columns={
                          0: [LOT_SCIENTIST_COLUMN_ID, LOT_DATE_REGISTERED_COLUMN_ID, ID_COLUMN_ID],
                          1: [LOT_SCIENTIST_COLUMN_ID, LOT_DATE_REGISTERED_COLUMN_ID, ID_COLUMN_ID]
                      })
}


# NOTE(badlato): pytest takes the cartesian product of these
@pytest.mark.xfail(not is_k8s(), reason="SS-40265: RMQ issues in Old Jenkins")
@pytest.mark.parametrize("order_type", [OrderType.SEQUENTIAL, OrderType.RANDOM],
                         ids=["sequential_order", "random_order"])
@pytest.mark.parametrize(
    "test_method", [get_products_from_reaction_enumeration_preview, get_products_from_reaction_enumeration_submit],
    ids=["preview", "async_submit"])
@pytest.mark.parametrize(REACTION_PARAM_NAMES, REACTION_PARAMS.values(), ids=REACTION_PARAMS.keys())
def test_reaction_enumeration(ld_api_client: ExtendedLDClient, new_live_report: LiveReport, test_method: Callable,
                              order_type: OrderType, reaction_name: Optional[str],
                              reaction_representation: Optional[str], reactants: List[List[Reactant]],
                              save_reaction: bool, expected_products_count: Optional[int],
                              product_filters: List[ReactionProductFilter], reactant_columns: Dict[int, List[str]]):
    """
    Tests reaction enumeration workflow - both the preview and the actual submission.
    Also tests different ways of creating the reaction - hand sketched, saved, etc.

    :param ld_api_client: ldclient
    :param new_live_report: The new LiveReport created for this test
    :param test_method: The method to call that hits endpoints under test. Returns the number of products
    :param order_type: The ordering of the enumeration products
    :param reaction_name: The ID of the saved reaction_representation. None if
    :param reaction_representation: The reaction string
    :param reactants: the reactant strings
    :param save_reaction: Whether or not a user-sketched reaction should be saved
    :param expected_products_count: The number of expected products. Calculaated if not specified.
    """
    assert xor(reaction_name is None,
               reaction_representation is None), "Test parameters invalid! Exactly one of (" \
                                                 "reaction_name, reaction_representation) should be " \
                                                 "None"
    reaction_id: Optional[str] = None
    if reaction_name is not None:
        reaction_id = ld_api_client.get_reaction_from_name(reaction_name=reaction_name).id
    elif save_reaction:
        reaction_id = ld_api_client.create_reaction(
            Reaction(rxn_representation=reaction_representation,
                     name=make_unique_name("Test Reaction "),
                     description="Some description",
                     project_id=new_live_report.project_id,
                     input_source_type=ReactionInputSourceType.USER_DEFINED)).id
    enumeration_data = ReactionEnumerationData(reactants=reactants,
                                               max_compounds=10,
                                               result_order=order_type,
                                               filters=product_filters,
                                               reactant_columns=reactant_columns)
    enumeration_request: ReactionEnumerationRequest = ReactionEnumerationRequest(
        reaction_id=reaction_id,
        reaction_representation=reaction_representation if reaction_id is None else None,
        enumeration_data=enumeration_data)
    if expected_products_count is None:
        expected_products_count = calc_expected_products_count(reactants)
    test_method(ld_api_client=ld_api_client,
                new_live_report=new_live_report,
                enumeration_request=enumeration_request,
                expected_products_count=expected_products_count)
