from library.api.extended_ldclient.base import BaseModel
from typing import List, Optional

from library.api.extended_ldclient.enums import ReactionInputSourceType


class Reaction(BaseModel):
    id: Optional[str]
    name: str
    description: str
    input_source_type: Optional[ReactionInputSourceType]
    rxn_representation: str
    owner: Optional[str]
    project_id: str
    reactant_classes: List[str] = []
    keywords: List[str] = []
