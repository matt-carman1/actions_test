from typing import Dict, List, Optional

from library.api.extended_ldclient.base import BaseModel
from library.api.extended_ldclient.enums import OrderType, ReactionProductFilterType


class RGroup(BaseModel):
    """
    :param structure: RGroup structure represented by CXSMILES
    """
    structure: str


class RGroupEnumerationData(BaseModel):
    live_report_id: Optional[str]
    r_groups: Dict[int, List[RGroup]]
    max_compounds: int
    result_order: OrderType


class RGroupEnumerationRequest(BaseModel):
    """
    :param scaffold_representation: Scaffold structure represented by mol V3000
    """
    scaffold_representation: Optional[str]
    enumeration_data: RGroupEnumerationData


class ReactantMetadata(BaseModel):
    file_name: str
    file_id: str
    title: str
    index: str
    properties: Dict[str, List[str]]
    additional_all_ids: List[str]


class Reactant(BaseModel):
    id: Optional[str]
    live_report_ids: Optional[List[str]]
    entity_ids: Optional[List[str]]
    structure: str
    metadata: Optional[List[ReactantMetadata]]


class ReactionProductFilter(BaseModel):
    type: ReactionProductFilterType
    minimum: float
    maximum: float


class ReactionEnumerationData(BaseModel):
    live_report_id: Optional[str]
    reactants: List[List[Reactant]]
    max_compounds: int
    result_order: OrderType
    filters: List[ReactionProductFilter] = []
    reactant_columns: Dict[int, List[str]] = {}


class ReactionEnumerationRequest(BaseModel):
    reaction_id: Optional[str]
    reaction_representation: Optional[str]
    enumeration_data: ReactionEnumerationData
