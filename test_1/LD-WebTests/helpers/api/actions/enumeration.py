from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.extended_ldclient.models import Reaction


def create_new_rxn_via_api(ld_api_client,
                           rxn_name,
                           desc,
                           source_type,
                           rxn_representation,
                           project_id,
                           rxn_owner=None,
                           reaction_id=None,
                           reactant_classes=[],
                           keywords=[]):
    """
    Helper to create a new reaction using extended LDClient.

    :param ld_api_client: LiveDesign client
    :param rxn_name: str, The name of the reaction
    :param desc: str, the description of the reaction
    :param source_type: Optional[ReactionInputSourceType], The input source type of the reaction, i.e either it's
                        user defined or from Schrodinger collection
    :param rxn_representation: str, the reaction string in molv3000 format
    :param rxn_owner: Optional[str], the owner of the reaction.
    :param project_id: str, the project id for the reaction.
    :param reaction_id: Optional[str], the id for the reaction
    :param reactant_classes: List[str] = [], the list of reactant names
    :param keywords: List[str] = [], The keywords for the reaction.
    """

    new_reaction = Reaction(name=rxn_name,
                            description=desc,
                            input_source_type=source_type,
                            rxn_representation=rxn_representation,
                            project_id=project_id,
                            owner=rxn_owner,
                            id=reaction_id,
                            reactant_classes=reactant_classes,
                            keywords=keywords)

    return ExtendedLDClient.create_reaction(ld_api_client, reaction=new_reaction)
