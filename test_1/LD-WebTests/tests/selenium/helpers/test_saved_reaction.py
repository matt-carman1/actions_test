from helpers.api.actions.enumeration import create_new_rxn_via_api
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.enums import ReactionInputSourceType


def test_saved_reaction(ld_api_client, new_live_report):
    """
    Test to verify that the create_new_rxn_via_api is creating a reaction which is present in the list of reactions
    fetched via the list_reactions method.

    :param ld_api_client: LiveDesign client
    """
    reaction_representation = "$RXN V3000\n\n      " \
                              "Mrv1908  010520221746\n\nM  V30 COUNTS 1 1\nM  V30 BEGIN REACTANT\nM  V30 BEGIN CTAB\nM  " \
                              "V30 COUNTS 6 6 0 0 1\nM  V30 BEGIN ATOM\nM  V30 1 C -4.4137 1.54 0 0\nM  V30 2 C -3.08 " \
                              "0.77 0 0\nM  V30 3 C -3.08 -0.77 0 0\nM  V30 4 C -4.4137 -1.54 0 0\nM  V30 5 C -5.7474 " \
                              "-0.77 0 0\nM  V30 6 C -5.7474 0.77 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  " \
                              "V30 1 2 1 2\nM  V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  " \
                              "V30 6 1 6 1\nM  V30 END BOND\nM  V30 END CTAB\nM  V30 END REACTANT\nM  " \
                              "V30 BEGIN PRODUCT\nM  V30 BEGIN CTAB\nM  V30 COUNTS 7 7 0 0 0\nM  V30 BEGIN ATOM\nM  " \
                              "V30 1 C 6.3937 0.77 0 0\nM  V30 2 C 7.7274 -0 0 0\nM  V30 3 C 7.7274 -1.54 0 0\nM  " \
                              "V30 4 C 6.3937 -2.31 0 0\nM  V30 5 C 5.06 -1.54 0 0\nM  V30 6 C 5.06 0 0 0\nM  " \
                              "V30 7 C 6.3937 2.31 0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  " \
                              "V30 2 1 2 3\nM  V30 3 2 3 4\nM  V30 4 1 4 5\nM  V30 5 2 5 6\nM  V30 6 1 6 1\nM  " \
                              "V30 7 1 1 7\nM  V30 END BOND\nM  V30 END CTAB\nM  V30 END PRODUCT\nM  END\n"

    new_saved_rxn = create_new_rxn_via_api(ld_api_client,
                                           rxn_name="Friedel crafts Alkylation",
                                           desc="Alkylation of benzene",
                                           source_type=ReactionInputSourceType.USER_DEFINED,
                                           rxn_representation=reaction_representation,
                                           rxn_owner="gdas",
                                           project_id="4",
                                           reactant_classes=["benzene"],
                                           keywords=["Aromatic comp"])

    reaction_list = ExtendedLDClient.list_reactions(ld_api_client)
    assert new_saved_rxn in reaction_list, \
        "The saved reaction named {} is not in the list of available reactions".format(new_saved_rxn.name)
